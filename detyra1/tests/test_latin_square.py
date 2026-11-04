"""Tests for the Latin Square IDDFS + Backtracking solver."""

import unittest

from detyra1.latin_square.latin_square import (
    compatible_rows,
    is_valid_latin_square,
    solve_latin_square_dfs,
    solve_latin_square_iddfs,
)


class LatinSquareTests(unittest.TestCase):
    def test_iddfs_sizes_one_to_six(self) -> None:
        for n in (1, 2, 3, 4, 5, 6):
            with self.subTest(n=n):
                result = solve_latin_square_iddfs(n)

                self.assertIsNotNone(result.square)
                assert result.square is not None
                self.assertTrue(is_valid_latin_square(result.square, n))
                self.assertEqual(result.stats.solution_depth, n)
                # IDDFS can only succeed in the last iteration (limit = n).
                self.assertEqual(result.stats.iterations, n)

    def test_iddfs_n6_is_fast_and_matches_known_counts(self) -> None:
        result = solve_latin_square_iddfs(6)

        self.assertEqual(result.stats.nodes_visited, 25927)
        self.assertLess(result.stats.execution_time_seconds, 10)

    def test_solution_is_in_reduced_form(self) -> None:
        result = solve_latin_square_iddfs(5)
        assert result.square is not None

        self.assertEqual(result.square[0], (1, 2, 3, 4, 5))
        self.assertEqual([row[0] for row in result.square], [1, 2, 3, 4, 5])

    def test_generated_rows_never_break_a_column(self) -> None:
        square = [(1, 2, 3, 4), (2, 1, 4, 3)]

        rows = list(compatible_rows(square, 4))

        self.assertEqual(rows, [(3, 4, 1, 2), (3, 4, 2, 1)])
        for row in rows:
            self.assertEqual(row[0], 3)
            for column, value in enumerate(row):
                self.assertNotIn(value, [existing[column] for existing in square])

    def test_dfs_finds_same_square_with_less_work(self) -> None:
        iddfs = solve_latin_square_iddfs(6)
        dfs = solve_latin_square_dfs(6)

        self.assertEqual(dfs.square, iddfs.square)
        self.assertEqual(dfs.stats.iterations, 1)
        self.assertLess(dfs.stats.nodes_visited, iddfs.stats.nodes_visited)

    def test_invalid_size_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            solve_latin_square_iddfs(0)
        with self.assertRaises(ValueError):
            solve_latin_square_dfs(0)


if __name__ == "__main__":
    unittest.main()
