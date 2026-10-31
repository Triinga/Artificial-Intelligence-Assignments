"""Generate a Latin Square using IDDFS and backtracking."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import permutations
from time import perf_counter


Row = tuple[int, ...]
Square = list[Row]


@dataclass
class SearchStats:
    """Measurements collected across all IDDFS iterations."""

    iterations: int = 0
    nodes_generated: int = 0
    nodes_visited: int = 0
    backtracks: int = 0
    maximum_depth: int = 0
    solution_depth: int | None = None
    execution_time_seconds: float = 0.0


@dataclass
class SearchResult:
    """The Latin Square found by IDDFS and its measurements."""

    square: Square | None
    stats: SearchStats


def solve_latin_square_iddfs(n: int) -> SearchResult:
    """Find an n x n Latin Square with IDDFS and row backtracking."""

    if n < 1:
        raise ValueError("n must be at least 1")

    started_at = perf_counter()
    stats = SearchStats()
    symbols = tuple(range(1, n + 1))
    candidate_rows = tuple(permutations(symbols))

    # Symmetry breaking: every Latin Square can be relabeled so its first row
    # has this canonical order.
    first_row = symbols

    def depth_limited_search(square: Square, limit: int) -> bool:
        """Run recursive DFS without crossing the current row-depth limit."""

        stats.nodes_visited += 1
        stats.maximum_depth = max(stats.maximum_depth, len(square))

        if len(square) == n:
            return True
        if len(square) == limit:
            return False

        for candidate in candidate_rows:
            stats.nodes_generated += 1
            if not is_compatible_row(candidate, square):
                continue

            square.append(candidate)

            if depth_limited_search(square, limit):
                return True

            # The candidate did not lead to a solution: undo it.
            square.pop()
            stats.backtracks += 1

        return False

    for limit in range(1, n + 1):
        stats.iterations += 1
        current_square: Square = [first_row]

        if depth_limited_search(current_square, limit):
            stats.solution_depth = len(current_square)
            stats.execution_time_seconds = perf_counter() - started_at
            return SearchResult(square=current_square, stats=stats)

    stats.execution_time_seconds = perf_counter() - started_at
    return SearchResult(square=None, stats=stats)


def is_compatible_row(candidate: Row, square: Square) -> bool:
    """Return True when candidate adds no duplicate value to any column."""

    return all(
        all(existing_row[column] != value for existing_row in square)
        for column, value in enumerate(candidate)
    )


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
    """Read n, run IDDFS, and print the square and statistics."""

    parser = argparse.ArgumentParser(
        description="Generate a Latin Square with IDDFS + Backtracking."
    )
    parser.add_argument("n", type=int, help="Latin Square size")
    args = parser.parse_args()

    result = solve_latin_square_iddfs(args.n)

    if result.square is None:
        print("No Latin Square was found.")
    else:
        print(format_square(result.square))
        print(f"\nValidation: {is_valid_latin_square(result.square, args.n)}")

    print("\nSearch statistics:")
    print(f"  IDDFS iterations: {result.stats.iterations}")
    print(f"  Nodes generated: {result.stats.nodes_generated}")
    print(f"  Nodes visited: {result.stats.nodes_visited}")
    print(f"  Backtracks: {result.stats.backtracks}")
    print(f"  Maximum depth: {result.stats.maximum_depth}")
    print(f"  Solution depth: {result.stats.solution_depth}")
    print(f"  Execution time: {result.stats.execution_time_seconds:.6f} seconds")


if __name__ == "__main__":
    main()
