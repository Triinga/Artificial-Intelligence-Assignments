"""Tests for the Sudoku BFS + Backtracking solver."""

import unittest
from pathlib import Path

from detyra1.sudoku.sudoku_solver import (
    is_valid_solution,
    parse_puzzle,
    solve_sudoku_bfs,
)


EXAMPLES = Path(__file__).parents[1] / "sudoku" / "examples"


def load(difficulty: str):
    return parse_puzzle((EXAMPLES / f"{difficulty}.txt").read_text(encoding="utf-8"))


class SudokuTests(unittest.TestCase):
    def test_easy_medium_and_hard_examples(self) -> None:
        for difficulty in ("easy", "medium", "hard"):
            for use_mrv in (True, False):
                with self.subTest(difficulty=difficulty, use_mrv=use_mrv):
                    puzzle = load(difficulty)
                    result = solve_sudoku_bfs(puzzle, use_mrv=use_mrv)

                    self.assertIsNotNone(result.solution)
                    assert result.solution is not None
                    self.assertTrue(is_valid_solution(result.solution))
                    self.assertEqual(len(result.path), puzzle.count(0) + 1)

    def test_difficulty_labels_follow_number_of_givens(self) -> None:
        givens = {name: 81 - load(name).count(0) for name in ("easy", "medium", "hard")}

        self.assertEqual(givens, {"easy": 36, "medium": 30, "hard": 28})

    def test_default_is_plain_bfs_without_mrv(self) -> None:
        default = solve_sudoku_bfs(load("hard"))
        without_mrv = solve_sudoku_bfs(load("hard"), use_mrv=False)

        self.assertEqual(default.stats.nodes_generated, without_mrv.stats.nodes_generated)

    def test_mrv_reduces_the_search(self) -> None:
        result = solve_sudoku_bfs(load("hard"), use_mrv=True)

        self.assertEqual(result.stats.nodes_generated, 205)
        self.assertEqual(result.stats.maximum_frontier, 9)

    def test_without_mrv_bfs_keeps_many_alternatives(self) -> None:
        expected = {
            # difficulty: (nodes generated, maximum frontier)
            "easy": (68, 5),
            "medium": (4631, 738),
            "hard": (22918, 3616),
        }
        for difficulty, (generated, frontier) in expected.items():
            with self.subTest(difficulty=difficulty):
                result = solve_sudoku_bfs(load(difficulty), use_mrv=False)

                self.assertEqual(result.stats.nodes_generated, generated)
                self.assertEqual(result.stats.maximum_frontier, frontier)
                self.assertGreater(result.stats.dead_ends, 0)

    def test_path_follows_parent_links_one_cell_per_step(self) -> None:
        puzzle = load("easy")
        result = solve_sudoku_bfs(puzzle, use_mrv=False)

        self.assertEqual(result.path[0], puzzle)
        for parent, child in zip(result.path, result.path[1:]):
            changed = [i for i in range(81) if parent[i] != child[i]]
            self.assertEqual(len(changed), 1)
            self.assertEqual(parent[changed[0]], 0)

    def test_invalid_initial_board_is_rejected(self) -> None:
        invalid = "550000000" + "000000000" * 8

        with self.assertRaises(ValueError):
            parse_puzzle(invalid)


if __name__ == "__main__":
    unittest.main()
