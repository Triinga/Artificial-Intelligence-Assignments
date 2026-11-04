"""Solve the Social Golfers Problem with DFS and backtracking.

The search builds one group at a time. A candidate group is accepted only if
none of its player pairs has appeared in an earlier group.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations
from time import perf_counter


Group = tuple[int, ...]
Week = list[Group]
Schedule = list[Week]
Pair = tuple[int, int]


@dataclass
class SearchStats:
    """Measurements collected while DFS is running."""

    nodes_generated: int = 0
    nodes_visited: int = 0
    backtracks: int = 0
    pruned_by_pair_constraint: int = 0
    maximum_depth: int = 0
    solution_depth: int | None = None
    execution_time_seconds: float = 0.0


@dataclass
class SearchResult:
    """The schedule found by DFS, together with its search measurements."""

    schedule: Schedule | None
    stats: SearchStats
    # True when the search was stopped by the time limit. In that case
    # schedule is None, but this does NOT prove that no schedule exists.
    timed_out: bool = False


class _TimeLimitReached(Exception):
    """Raised inside DFS to stop the whole recursion when time runs out."""


def theoretical_week_upper_bound(
    groups: int, players_per_group: int
) -> int | None:
    """Return the pair-count upper bound for the number of weeks.

    For p > 1, every player meets p - 1 new players per week and has only
    n - 1 possible partners. For p = 1 no pairs are formed, so this particular
    bound is not finite and the function returns None.
    """

    _validate_dimensions(groups, players_per_group)
    if players_per_group == 1:
        return None

    player_count = groups * players_per_group
    return (player_count - 1) // (players_per_group - 1)


def solve_social_golfers(
    groups: int,
    players_per_group: int,
    weeks: int,
    *,
    fix_first_week: bool = True,
    time_limit_seconds: float | None = None,
) -> SearchResult:
    """Find a valid schedule using depth-first search with backtracking.

    Args:
        groups: Number of groups in every week (g).
        players_per_group: Number of players in every group (p).
        weeks: Number of weeks requested (w).
        fix_first_week: Fix a canonical first week to remove symmetric states.
        time_limit_seconds: Stop the search after this many seconds
            (None means no limit).

    Returns:
        SearchResult whose schedule is None when no solution exists or when
        the time limit was reached (then timed_out is True).
    """

    _validate_dimensions(groups, players_per_group)
    if weeks < 0:
        raise ValueError("weeks must be at least 0")

    stats = SearchStats()
    started_at = perf_counter()
    deadline = None if time_limit_seconds is None else started_at + time_limit_seconds
    player_count = groups * players_per_group

    upper_bound = theoretical_week_upper_bound(groups, players_per_group)
    if upper_bound is not None and weeks > upper_bound:
        stats.execution_time_seconds = perf_counter() - started_at
        return SearchResult(schedule=None, stats=stats)

    schedule: Schedule = []
    used_pairs: set[Pair] = set()

    # Optional symmetry breaking: any first week can be renamed into this form.
    if fix_first_week and weeks > 0:
        first_week = [
            tuple(range(start, start + players_per_group))
            for start in range(0, player_count, players_per_group)
        ]
        schedule.append(first_week)
        for group in first_week:
            used_pairs.update(combinations(group, 2))

    def dfs_week(week_index: int) -> bool:
        """Start or finish the DFS search for one week."""

        if week_index == weeks:
            stats.solution_depth = groups * weeks
            return True

        current_week: Week = []
        remaining_players = set(range(player_count))
        return dfs_groups(week_index, current_week, remaining_players)

    def dfs_groups(
        week_index: int,
        current_week: Week,
        remaining_players: set[int],
    ) -> bool:
        """Recursively choose groups for the current week.

        Backtracking occurs after a recursive call fails: the chosen group and
        all pairs introduced by it are removed before the next group is tried.
        """

        if deadline is not None and perf_counter() > deadline:
            raise _TimeLimitReached

        stats.nodes_visited += 1
        depth = week_index * groups + len(current_week)
        stats.maximum_depth = max(stats.maximum_depth, depth)

        if len(current_week) == groups:
            schedule.append(current_week.copy())
            if dfs_week(week_index + 1):
                return True
            schedule.pop()
            return False

        # Groups are unordered. Anchoring the smallest remaining player avoids
        # generating the same weekly partition in different group orders.
        anchor = min(remaining_players)
        possible_companions = sorted(remaining_players - {anchor})

        for companions in combinations(possible_companions, players_per_group - 1):
            group = (anchor, *companions)
            group_pairs = tuple(combinations(group, 2))
            stats.nodes_generated += 1

            if not used_pairs.isdisjoint(group_pairs):
                stats.pruned_by_pair_constraint += 1
                continue

            current_week.append(group)
            remaining_players.difference_update(group)
            used_pairs.update(group_pairs)

            if dfs_groups(week_index, current_week, remaining_players):
                return True

            # This is the exact backtracking step.
            used_pairs.difference_update(group_pairs)
            remaining_players.update(group)
            current_week.pop()
            stats.backtracks += 1

        return False

    first_week_to_search = len(schedule)
    try:
        solved = dfs_week(first_week_to_search)
    except _TimeLimitReached:
        stats.execution_time_seconds = perf_counter() - started_at
        return SearchResult(schedule=None, stats=stats, timed_out=True)

    stats.execution_time_seconds = perf_counter() - started_at
    return SearchResult(schedule=schedule if solved else None, stats=stats)


def validate_schedule(
    schedule: Schedule,
    groups: int,
    players_per_group: int,
    weeks: int,
) -> tuple[bool, str]:
    """Independently verify all constraints of a completed schedule."""

    _validate_dimensions(groups, players_per_group)
    player_count = groups * players_per_group
    expected_players = set(range(player_count))

    if len(schedule) != weeks:
        return False, f"expected {weeks} weeks, found {len(schedule)}"

    used_pairs: set[Pair] = set()

    for week_number, week in enumerate(schedule, start=1):
        if len(week) != groups:
            return False, f"week {week_number} does not contain {groups} groups"

        players_in_week: list[int] = []
        for group_number, group in enumerate(week, start=1):
            if len(group) != players_per_group:
                return False, (
                    f"week {week_number}, group {group_number} does not contain "
                    f"{players_per_group} players"
                )
            players_in_week.extend(group)

            for pair in combinations(sorted(group), 2):
                if pair in used_pairs:
                    return False, f"pair {pair} appears more than once"
                used_pairs.add(pair)

        if len(players_in_week) != player_count or set(players_in_week) != expected_players:
            return False, f"week {week_number} does not use every player exactly once"

    return True, "schedule is valid"


def _validate_dimensions(groups: int, players_per_group: int) -> None:
    """Reject dimensions that cannot describe a Social Golfers instance."""

    if groups < 1:
        raise ValueError("groups must be at least 1")
    if players_per_group < 1:
        raise ValueError("players_per_group must be at least 1")


def _print_schedule(schedule: Schedule) -> None:
    """Print a completed schedule in a readable form."""

    for week_number, week in enumerate(schedule, start=1):
        formatted_groups = " | ".join(",".join(map(str, group)) for group in week)
        print(f"Week {week_number}: {formatted_groups}")


def main() -> None:
    """Read command-line parameters, run DFS, and show the result."""

    parser = argparse.ArgumentParser(
        description="Solve the Social Golfers Problem with DFS and backtracking."
    )
    parser.add_argument("groups", type=int, help="number of groups per week")
    parser.add_argument("players_per_group", type=int, help="players in each group")
    parser.add_argument("weeks", type=int, help="requested number of weeks")
    parser.add_argument(
        "--search-first-week",
        action="store_true",
        help="let DFS search the first week instead of fixing a symmetric one",
    )
    parser.add_argument(
        "--time-limit",
        type=float,
        default=None,
        metavar="SECONDS",
        help="stop the search after this many seconds",
    )
    args = parser.parse_args()

    result = solve_social_golfers(
        args.groups,
        args.players_per_group,
        args.weeks,
        fix_first_week=not args.search_first_week,
        time_limit_seconds=args.time_limit,
    )

    if result.timed_out:
        print(
            f"Time limit of {args.time_limit} seconds reached. "
            "No schedule found yet (this does not prove that none exists)."
        )
    elif result.schedule is None:
        print("No valid schedule was found.")
    else:
        _print_schedule(result.schedule)
        is_valid, message = validate_schedule(
            result.schedule,
            args.groups,
            args.players_per_group,
            args.weeks,
        )
        print(f"Validation: {message}")
        if not is_valid:
            raise RuntimeError("DFS returned an invalid schedule")

    print("\nSearch statistics:")
    print(f"  Nodes generated: {result.stats.nodes_generated}")
    print(f"  Nodes visited: {result.stats.nodes_visited}")
    print(f"  Pruned by pair constraint: {result.stats.pruned_by_pair_constraint}")
    print(f"  Backtracks: {result.stats.backtracks}")
    print(f"  Maximum depth: {result.stats.maximum_depth}")
    print(f"  Solution depth: {result.stats.solution_depth}")
    print(f"  Execution time: {result.stats.execution_time_seconds:.6f} seconds")


if __name__ == "__main__":
    main()
