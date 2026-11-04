"""Tests for the DFS + backtracking Social Golfers solver."""

import unittest

from detyra1.social_golfers.known_solution_8_4_10 import KNOWN_SOLUTION_8_4_10
from detyra1.social_golfers.max_weeks import (
    NO_SCHEDULE,
    REACHED_BOUND,
    TIME_LIMIT,
    find_max_weeks_with_dfs,
)
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

    def test_demo_instance_5_5_6_backtracks_and_is_valid(self) -> None:
        result = solve_social_golfers(5, 5, 6)

        schedule = result.schedule
        assert schedule is not None
        is_valid, message = validate_schedule(schedule, 5, 5, 6)
        self.assertTrue(is_valid, message)
        self.assertEqual(result.stats.backtracks, 53)

    def test_eight_four_five_is_found_by_dfs(self) -> None:
        result = solve_social_golfers(8, 4, 5)

        schedule = result.schedule
        assert schedule is not None
        is_valid, message = validate_schedule(schedule, 8, 4, 5)
        self.assertTrue(is_valid, message)

    def test_time_limit_stops_search_without_an_answer(self) -> None:
        result = solve_social_golfers(8, 4, 6, time_limit_seconds=0.2)

        self.assertTrue(result.timed_out)
        self.assertIsNone(result.schedule)
        self.assertLess(result.stats.execution_time_seconds, 2)

    def test_max_weeks_reaches_upper_bound(self) -> None:
        result = find_max_weeks_with_dfs(5, 5, time_limit_seconds=20)

        self.assertEqual(result.stopped_because, REACHED_BOUND)
        self.assertEqual(result.dfs_best_weeks, 6)
        self.assertEqual(result.upper_bound, 6)

    def test_max_weeks_proves_impossibility(self) -> None:
        result = find_max_weeks_with_dfs(2, 3, time_limit_seconds=20)

        self.assertEqual(result.stopped_because, NO_SCHEDULE)
        self.assertEqual(result.dfs_best_weeks, 1)

    def test_max_weeks_for_assignment_stops_at_time_limit(self) -> None:
        result = find_max_weeks_with_dfs(8, 4, time_limit_seconds=0.2)

        self.assertEqual(result.stopped_because, TIME_LIMIT)
        self.assertEqual(result.dfs_best_weeks, 5)
        self.assertEqual(result.upper_bound, 10)

    def test_assignment_upper_bound_is_ten(self) -> None:
        self.assertEqual(theoretical_week_upper_bound(8, 4), 10)

    def test_known_ten_week_schedule_is_valid(self) -> None:
        is_valid, message = validate_schedule(KNOWN_SOLUTION_8_4_10, 8, 4, 10)

        self.assertTrue(is_valid, message)

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
