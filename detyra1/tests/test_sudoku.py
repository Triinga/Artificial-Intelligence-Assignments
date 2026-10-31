"""Tests for the Sudoku BFS + Backtracking solver."""

import unittest
from pathlib import Path

from detyra1.sudoku.sudoku_solver import (
    is_valid_solution,
    parse_puzzle,
    solve_sudoku_bfs,
)


EXAMPLES = Path(__file__).parents[1] / "sudoku" / "examples"


class SudokuTests(unittest.TestCase):
    def test_easy_medium_and_hard_examples(self) -> None:
        for difficulty in ("easy", "medium", "hard"):
            with self.subTest(difficulty=difficulty):
                puzzle = parse_puzzle(
                    (EXAMPLES / f"{difficulty}.txt").read_text(encoding="utf-8")
                )
                result = solve_sudoku_bfs(puzzle)

                self.assertIsNotNone(result.solution)
                assert result.solution is not None
                self.assertTrue(is_valid_solution(result.solution))
                self.assertEqual(len(result.path), puzzle.count(0) + 1)

    def test_invalid_initial_board_is_rejected(self) -> None:
        invalid = "550000000" + "000000000" * 8

        with self.assertRaises(ValueError):
            parse_puzzle(invalid)


if __name__ == "__main__":
    unittest.main()
