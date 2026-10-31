"""Tests for the Latin Square IDDFS + Backtracking solver."""

import unittest

from detyra1.latin_square.latin_square import (
    is_valid_latin_square,
    solve_latin_square_iddfs,
)


class LatinSquareTests(unittest.TestCase):
    def test_sizes_one_three_and_five(self) -> None:
        for n in (1, 3, 5):
            with self.subTest(n=n):
                result = solve_latin_square_iddfs(n)

                self.assertIsNotNone(result.square)
                assert result.square is not None
                self.assertTrue(is_valid_latin_square(result.square, n))
                self.assertEqual(result.stats.solution_depth, n)
                self.assertEqual(result.stats.iterations, n)

    def test_invalid_size_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            solve_latin_square_iddfs(0)


if __name__ == "__main__":
    unittest.main()
