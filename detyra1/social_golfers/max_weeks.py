"""Answer "for how many weeks can they play?" for g groups of p players.

The DFS is run for w = 1, 2, 3, ... until one of three things happens:

1. w reaches the theoretical upper bound -> the bound is the maximum (proved).
2. DFS searches everything and finds no schedule -> w - 1 is the maximum
   (proved, because DFS with backtracking is complete).
3. The time limit is reached -> DFS only gives a lower bound. For 8-4 the
   published 10-week schedule is then verified to close the gap.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field

from detyra1.social_golfers.known_solution_8_4_10 import KNOWN_SOLUTION_8_4_10
from detyra1.social_golfers.social_golfers import (
    solve_social_golfers,
    theoretical_week_upper_bound,
    validate_schedule,
)


REACHED_BOUND = "upper bound reached"
NO_SCHEDULE = "no schedule exists"
TIME_LIMIT = "time limit reached"


@dataclass
class MaxWeeksResult:
    """What DFS proved about the maximum number of weeks."""

    upper_bound: int
    dfs_best_weeks: int
    stopped_because: str
    # One entry per DFS run: (weeks, outcome, seconds).
    attempts: list[tuple[int, str, float]] = field(default_factory=list)


def find_max_weeks_with_dfs(
    groups: int, players_per_group: int, time_limit_seconds: float | None
) -> MaxWeeksResult:
    """Run DFS for w = 1, 2, ... and stop at the bound, a failure or a timeout."""

    upper_bound = theoretical_week_upper_bound(groups, players_per_group)
    if upper_bound is None:
        raise ValueError("with 1 player per group no pairs exist: weeks are unlimited")

    result = MaxWeeksResult(upper_bound, dfs_best_weeks=0, stopped_because=REACHED_BOUND)

    for weeks in range(1, upper_bound + 1):
        search = solve_social_golfers(
            groups, players_per_group, weeks, time_limit_seconds=time_limit_seconds
        )
        seconds = search.stats.execution_time_seconds

        if search.timed_out:
            result.attempts.append((weeks, "time limit", seconds))
            result.stopped_because = TIME_LIMIT
            return result
        if search.schedule is None:
            result.attempts.append((weeks, "no schedule", seconds))
            result.stopped_because = NO_SCHEDULE
            return result

        result.attempts.append((weeks, "found", seconds))
        result.dfs_best_weeks = weeks

    return result


def main() -> None:
    """Print the upper bound, the DFS results and the final answer."""

    parser = argparse.ArgumentParser(
        description="Find the maximum number of weeks for g groups of p players."
    )
    parser.add_argument("groups", type=int, help="number of groups per week")
    parser.add_argument("players_per_group", type=int, help="players in each group")
    parser.add_argument(
        "--time-limit",
        type=float,
        default=20.0,
        metavar="SECONDS",
        help="time limit for each DFS run (default: 20)",
    )
    args = parser.parse_args()

    g, p = args.groups, args.players_per_group
    result = find_max_weeks_with_dfs(g, p, args.time_limit)
    n = g * p

    print(f"Instance: {n} players, {g} groups of {p}")
    print(f"Upper bound: floor({n - 1}/{p - 1}) = {result.upper_bound} weeks")
    print("\nDFS runs:")
    for weeks, outcome, seconds in result.attempts:
        print(f"  w={weeks}: {outcome} ({seconds:.3f} s)")

    if result.stopped_because == REACHED_BOUND:
        answer = result.upper_bound
        reason = "DFS found a schedule for the upper bound itself"
    elif result.stopped_because == NO_SCHEDULE:
        answer = result.dfs_best_weeks
        reason = f"DFS proved that {answer + 1} weeks are impossible"
    else:
        print(f"\nDFS found schedules up to {result.dfs_best_weeks} weeks, then hit the time limit.")
        answer = None
        if (g, p) == (8, 4):
            is_valid, message = validate_schedule(KNOWN_SOLUTION_8_4_10, 8, 4, 10)
            print(f"Published 8-4-10 schedule (Aguado): {message}")
            if is_valid:
                answer = result.upper_bound
                reason = "the upper bound is reached by the verified published schedule"

    if answer is None:
        print(
            f"\nAnswer: unknown, between {result.dfs_best_weeks} and "
            f"{result.upper_bound} weeks."
        )
    else:
        unit = "week" if answer == 1 else "weeks"
        print(f"\nAnswer: maximum = {answer} {unit} ({reason}).")


if __name__ == "__main__":
    main()
