# Social Golfers – DFS with Backtracking

## Model

For `g` groups, `p` players per group, and `w` weeks, the total number of
players is `n = g * p`. Every player must appear exactly once per week and no
pair of players may share a group more than once.

The DFS state contains:

- the completed weeks;
- the groups currently selected for this week;
- the players still unassigned this week;
- `used_pairs`, the pairs that have already played together.

## Important functions

- `solve_social_golfers(...)` prepares the state and starts DFS.
- `dfs_groups(...)` recursively adds one valid group at a time.
- `theoretical_week_upper_bound(...)` calculates
  `floor((n - 1) / (p - 1))` when `p > 1`.
- `validate_schedule(...)` independently checks every solution constraint.

Backtracking happens inside `dfs_groups(...)`: when the recursive call fails,
the last group and its pairs are removed before the next candidate is tried.

## Run

From the repository root:

```bash
python -m detyra1.social_golfers.social_golfers 2 2 3
python -m unittest discover -s detyra1/tests -v
```

To make DFS search the first week instead of fixing a symmetric first week:

```bash
python -m detyra1.social_golfers.social_golfers 2 3 2 --search-first-week
```

## Verified results

- `2 x 2 x 3`: valid schedule found.
- `2 x 3 x 2`: correctly reported impossible; 20 backtracks when the first
  week is searched.
- `8 x 4 x 2` through `8 x 4 x 5`: valid schedules found and independently
  validated.
- `8 x 4`: theoretical upper bound is 10 weeks.

Finding or disproving the full `8 x 4 x 10` instance is still pending. The
current code is the clear core algorithm; any later optimization will be
documented separately.
