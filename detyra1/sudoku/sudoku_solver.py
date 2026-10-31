"""Solve Sudoku with Breadth-First Search and parent backtracking."""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter


Board = tuple[int, ...]
ALL_DIGITS = set(range(1, 10))


@dataclass
class SearchStats:
    """Measurements collected while BFS is running."""

    nodes_generated: int = 0
    nodes_visited: int = 0
    dead_ends: int = 0
    maximum_frontier: int = 0
    maximum_depth: int = 0
    solution_depth: int | None = None
    backtrack_steps: int = 0
    execution_time_seconds: float = 0.0


@dataclass
class SearchResult:
    """The solved board, its parent path, and BFS statistics."""

    solution: Board | None
    path: list[Board]
    stats: SearchStats


def parse_puzzle(text: str) -> Board:
    """Convert 81 digits (0 or . for empty cells) into an immutable board."""

    symbols = [character for character in text if character.isdigit() or character == "."]
    if len(symbols) != 81:
        raise ValueError("a Sudoku puzzle must contain exactly 81 cells")

    board = tuple(0 if symbol in {"0", "."} else int(symbol) for symbol in symbols)
    validate_initial_board(board)
    return board


def validate_initial_board(board: Board) -> None:
    """Reject an incorrectly sized board or duplicate initial values."""

    if len(board) != 81:
        raise ValueError("a Sudoku board must contain exactly 81 cells")
    if any(value < 0 or value > 9 for value in board):
        raise ValueError("Sudoku values must be between 0 and 9")

    for row in range(9):
        _reject_duplicates(board[row * 9 : row * 9 + 9], f"row {row + 1}")

    for column in range(9):
        _reject_duplicates(
            tuple(board[row * 9 + column] for row in range(9)),
            f"column {column + 1}",
        )

    for box_row in range(0, 9, 3):
        for box_column in range(0, 9, 3):
            box = tuple(
                board[(box_row + row_offset) * 9 + box_column + column_offset]
                for row_offset in range(3)
                for column_offset in range(3)
            )
            _reject_duplicates(box, f"box ({box_row // 3 + 1}, {box_column // 3 + 1})")


def valid_values(board: Board, index: int) -> tuple[int, ...]:
    """Return values that satisfy row, column, and 3x3 box constraints."""

    if board[index] != 0:
        return ()

    row, column = divmod(index, 9)
    used = set(board[row * 9 : row * 9 + 9])
    used.update(board[row_number * 9 + column] for row_number in range(9))

    box_row = (row // 3) * 3
    box_column = (column // 3) * 3
    used.update(
        board[(box_row + row_offset) * 9 + box_column + column_offset]
        for row_offset in range(3)
        for column_offset in range(3)
    )

    return tuple(sorted(ALL_DIGITS - used))


def choose_empty_cell(board: Board) -> tuple[int, tuple[int, ...]] | None:
    """Choose the empty cell with the fewest valid values (MRV optimization)."""

    best: tuple[int, tuple[int, ...]] | None = None

    for index, value in enumerate(board):
        if value != 0:
            continue

        candidates = valid_values(board, index)
        if not candidates:
            return index, candidates
        if best is None or len(candidates) < len(best[1]):
            best = index, candidates
            if len(candidates) == 1:
                return best

    return best


def solve_sudoku_bfs(initial_board: Board) -> SearchResult:
    """Solve a Sudoku using a FIFO queue and backtrack through parent links."""

    validate_initial_board(initial_board)
    started_at = perf_counter()
    stats = SearchStats(maximum_frontier=1)
    initial_empty_cells = initial_board.count(0)

    queue: deque[Board] = deque([initial_board])
    parents: dict[Board, Board | None] = {initial_board: None}

    while queue:
        current = queue.popleft()
        stats.nodes_visited += 1
        current_depth = initial_empty_cells - current.count(0)
        stats.maximum_depth = max(stats.maximum_depth, current_depth)

        if 0 not in current:
            path = reconstruct_path(current, parents)
            stats.solution_depth = current_depth
            stats.backtrack_steps = len(path) - 1
            stats.execution_time_seconds = perf_counter() - started_at
            return SearchResult(solution=current, path=path, stats=stats)

        choice = choose_empty_cell(current)
        if choice is None or not choice[1]:
            stats.dead_ends += 1
            continue

        index, candidates = choice
        for candidate in candidates:
            child = current[:index] + (candidate,) + current[index + 1 :]
            stats.nodes_generated += 1

            if child in parents:
                continue

            parents[child] = current
            queue.append(child)

        stats.maximum_frontier = max(stats.maximum_frontier, len(queue))

    stats.execution_time_seconds = perf_counter() - started_at
    return SearchResult(solution=None, path=[], stats=stats)


def reconstruct_path(goal: Board, parents: dict[Board, Board | None]) -> list[Board]:
    """Backtrack from the goal board to the initial board using parent links."""

    path: list[Board] = []
    current: Board | None = goal

    while current is not None:
        path.append(current)
        current = parents[current]

    path.reverse()
    return path


def is_valid_solution(board: Board) -> bool:
    """Return True only for a complete board satisfying all Sudoku constraints."""

    if len(board) != 81 or 0 in board:
        return False

    rows = [set(board[row * 9 : row * 9 + 9]) for row in range(9)]
    columns = [set(board[row * 9 + column] for row in range(9)) for column in range(9)]
    boxes = [
        {
            board[(box_row + row_offset) * 9 + box_column + column_offset]
            for row_offset in range(3)
            for column_offset in range(3)
        }
        for box_row in range(0, 9, 3)
        for box_column in range(0, 9, 3)
    ]
    return all(unit == ALL_DIGITS for unit in rows + columns + boxes)


def format_board(board: Board) -> str:
    """Format a Sudoku board for terminal output."""

    lines: list[str] = []
    for row in range(9):
        values = [str(value) if value else "." for value in board[row * 9 : row * 9 + 9]]
        lines.append(" ".join(values[0:3]) + " | " + " ".join(values[3:6]) + " | " + " ".join(values[6:9]))
        if row in {2, 5}:
            lines.append("------+-------+------")
    return "\n".join(lines)


def _reject_duplicates(values: tuple[int, ...], location: str) -> None:
    """Raise ValueError when nonzero values repeat inside one Sudoku unit."""

    nonzero_values = [value for value in values if value != 0]
    if len(nonzero_values) != len(set(nonzero_values)):
        raise ValueError(f"duplicate initial value in {location}")


def main() -> None:
    """Load a puzzle file, solve it, and print the solution and statistics."""

    parser = argparse.ArgumentParser(description="Solve Sudoku with BFS + Backtracking.")
    parser.add_argument("puzzle", type=Path, help="path to a Sudoku text file")
    args = parser.parse_args()

    initial_board = parse_puzzle(args.puzzle.read_text(encoding="utf-8"))
    result = solve_sudoku_bfs(initial_board)

    print("Initial board:")
    print(format_board(initial_board))

    if result.solution is None:
        print("\nNo solution was found.")
    else:
        print("\nSolved board:")
        print(format_board(result.solution))
        print(f"\nValidation: {is_valid_solution(result.solution)}")

    print("\nSearch statistics:")
    print(f"  Nodes generated: {result.stats.nodes_generated}")
    print(f"  Nodes visited: {result.stats.nodes_visited}")
    print(f"  Dead ends: {result.stats.dead_ends}")
    print(f"  Maximum frontier: {result.stats.maximum_frontier}")
    print(f"  Maximum depth: {result.stats.maximum_depth}")
    print(f"  Solution depth: {result.stats.solution_depth}")
    print(f"  Backtrack steps: {result.stats.backtrack_steps}")
    print(f"  Execution time: {result.stats.execution_time_seconds:.6f} seconds")


if __name__ == "__main__":
    main()
