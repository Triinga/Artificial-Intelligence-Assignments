"""Generate a Latin Square using IDDFS and backtracking.

A state is the list of rows filled so far. A successor adds one complete row.
Rows are generated one at a time by a small backtracking generator, so only
rows that are compatible with the columns are ever created.
"""

from __future__ import annotations

import argparse
from collections.abc import Iterator
from dataclasses import dataclass
from time import perf_counter


Row = tuple[int, ...]
Square = list[Row]


@dataclass
class SearchStats:
    """Measurements collected across all search iterations."""

    iterations: int = 0
    nodes_generated: int = 0
    nodes_visited: int = 0
    backtracks: int = 0
    maximum_depth: int = 0
    solution_depth: int | None = None
    execution_time_seconds: float = 0.0


@dataclass
class SearchResult:
    """The Latin Square found by the search and its measurements."""

    square: Square | None
    stats: SearchStats


def compatible_rows(square: Square, n: int) -> Iterator[Row]:
    """Yield, one at a time, every row that can be added to square.

    Reduced form (symmetry breaking): the new row with index r starts with the
    value r + 1. The other cells are filled from left to right; a value is
    tried only if it is not already used in this row or in this column.
    When a cell has no possible value, the generator undoes the last cell and
    tries the next value (backtracking inside the row).
    """

    first_value = len(square) + 1
    row = [first_value]
    used_in_row = {first_value}

    def fill(column: int) -> Iterator[Row]:
        if column == n:
            yield tuple(row)
            return

        for value in range(1, n + 1):
            if value in used_in_row:
                continue
            if any(existing[column] == value for existing in square):
                continue

            row.append(value)
            used_in_row.add(value)
            yield from fill(column + 1)
            row.pop()                    # backtracking inside the row
            used_in_row.remove(value)

    yield from fill(1)


def depth_limited_search(
    square: Square, n: int, limit: int, stats: SearchStats
) -> bool:
    """Recursive DFS that never goes deeper than limit rows."""

    stats.nodes_visited += 1
    stats.maximum_depth = max(stats.maximum_depth, len(square))

    if len(square) == n:          # goal test: n valid rows
        return True
    if len(square) == limit:      # depth limit reached: do not expand
        return False

    for candidate in compatible_rows(square, n):
        stats.nodes_generated += 1
        square.append(candidate)

        if depth_limited_search(square, n, limit, stats):
            return True

        # The candidate did not lead to a solution: undo it.
        square.pop()
        stats.backtracks += 1

    return False


def _initial_square(n: int) -> Square:
    """Reduced form: the first row is always (1, 2, ..., n)."""

    return [tuple(range(1, n + 1))]


def solve_latin_square_iddfs(n: int) -> SearchResult:
    """Find an n x n Latin Square with IDDFS (limits 1, 2, ..., n)."""

    if n < 1:
        raise ValueError("n must be at least 1")

    started_at = perf_counter()
    stats = SearchStats()

    for limit in range(1, n + 1):
        stats.iterations += 1
        square = _initial_square(n)   # every iteration starts from scratch

        if depth_limited_search(square, n, limit, stats):
            stats.solution_depth = len(square)
            stats.execution_time_seconds = perf_counter() - started_at
            return SearchResult(square=square, stats=stats)

    stats.execution_time_seconds = perf_counter() - started_at
    return SearchResult(square=None, stats=stats)


def solve_latin_square_dfs(n: int) -> SearchResult:
    """Plain DFS (one iteration with limit n), used only for comparison."""

    if n < 1:
        raise ValueError("n must be at least 1")

    started_at = perf_counter()
    stats = SearchStats(iterations=1)
    square = _initial_square(n)

    solved = depth_limited_search(square, n, n, stats)
    if solved:
        stats.solution_depth = len(square)
    stats.execution_time_seconds = perf_counter() - started_at
    return SearchResult(square=square if solved else None, stats=stats)


def is_valid_latin_square(square: Square, n: int) -> bool:
    """Independently verify row and column constraints."""

    if len(square) != n or any(len(row) != n for row in square):
        return False

    expected = set(range(1, n + 1))
    rows_valid = all(set(row) == expected for row in square)
    columns_valid = all(
        {square[row][column] for row in range(n)} == expected
        for column in range(n)
    )
    return rows_valid and columns_valid


def format_square(square: Square) -> str:
    """Format a Latin Square for terminal output."""

    return "\n".join(" ".join(map(str, row)) for row in square)


def main() -> None:
    """Read n, run IDDFS (or plain DFS), and print the square and statistics."""

    parser = argparse.ArgumentParser(
        description="Generate a Latin Square with IDDFS + Backtracking."
    )
    parser.add_argument("n", type=int, help="Latin Square size")
    parser.add_argument(
        "--dfs",
        action="store_true",
        help="run plain DFS (single limit n) instead of IDDFS, for comparison",
    )
    args = parser.parse_args()

    if args.dfs:
        result = solve_latin_square_dfs(args.n)
        algorithm = "DFS"
    else:
        result = solve_latin_square_iddfs(args.n)
        algorithm = "IDDFS"

    if result.square is None:
        print("No Latin Square was found.")
    else:
        print(format_square(result.square))
        print(f"\nValidation: {is_valid_latin_square(result.square, args.n)}")

    print(f"\nSearch statistics ({algorithm}):")
    print(f"  Iterations: {result.stats.iterations}")
    print(f"  Nodes generated: {result.stats.nodes_generated}")
    print(f"  Nodes visited: {result.stats.nodes_visited}")
    print(f"  Backtracks: {result.stats.backtracks}")
    print(f"  Maximum depth: {result.stats.maximum_depth}")
    print(f"  Solution depth: {result.stats.solution_depth}")
    print(f"  Execution time: {result.stats.execution_time_seconds:.6f} seconds")


if __name__ == "__main__":
    main()
