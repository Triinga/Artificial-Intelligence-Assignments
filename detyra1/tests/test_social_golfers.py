"""Tests for the DFS + backtracking Social Golfers solver."""

import unittest

from detyra1.social_golfers.social_golfers import (
    solve_social_golfers,
    theoretical_week_upper_bound,
    validate_schedule,
)


class SocialGolfersTests(unittest.TestCase):
    def test_valid_two_groups_of_two_for_three_weeks(self) -> None:
        result = solve_social_golfers(2, 2, 3)

        self.assertIsNotNone(result.schedule)
        schedule = result.schedule
        assert schedule is not None
        is_valid, message = validate_schedule(schedule, 2, 2, 3)
        self.assertTrue(is_valid, message)
        self.assertEqual(result.stats.solution_depth, 6)

    def test_dfs_can_search_the_first_week_too(self) -> None:
        result = solve_social_golfers(2, 2, 3, fix_first_week=False)

        self.assertIsNotNone(result.schedule)
        schedule = result.schedule
        assert schedule is not None
        is_valid, message = validate_schedule(schedule, 2, 2, 3)
        self.assertTrue(is_valid, message)
        self.assertGreater(result.stats.nodes_generated, 0)

    def test_request_above_upper_bound_is_impossible(self) -> None:
        result = solve_social_golfers(2, 2, 4)

        self.assertIsNone(result.schedule)
        self.assertEqual(result.stats.nodes_visited, 0)

    def test_unsatisfiable_instance_really_backtracks(self) -> None:
        result = solve_social_golfers(2, 3, 2, fix_first_week=False)

        self.assertIsNone(result.schedule)
        self.assertGreater(result.stats.nodes_visited, 0)
        self.assertGreater(result.stats.backtracks, 0)

    def test_assignment_upper_bound_is_ten(self) -> None:
        self.assertEqual(theoretical_week_upper_bound(8, 4), 10)

    def test_validator_rejects_a_repeated_pair(self) -> None:
        invalid_schedule = [
            [(0, 1), (2, 3)],
            [(0, 1), (2, 3)],
        ]

        is_valid, message = validate_schedule(invalid_schedule, 2, 2, 2)

        self.assertFalse(is_valid)
        self.assertIn("appears more than once", message)

    def test_invalid_dimensions_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            solve_social_golfers(0, 4, 1)


if __name__ == "__main__":
    unittest.main()
