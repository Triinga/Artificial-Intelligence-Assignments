"""Validate the published optimal 8-4-10 schedule."""

from detyra1.social_golfers.known_solution_8_4_10 import KNOWN_SOLUTION_8_4_10
from detyra1.social_golfers.social_golfers import (
    theoretical_week_upper_bound,
    validate_schedule,
)


def main() -> None:
    """Print whether the known 10-week schedule satisfies every constraint."""

    is_valid, message = validate_schedule(KNOWN_SOLUTION_8_4_10, 8, 4, 10)
    upper_bound = theoretical_week_upper_bound(8, 4)

    print(f"Validation: {message}")
    print(f"Theoretical upper bound: {upper_bound} weeks")

    if not is_valid:
        raise SystemExit(1)

    print("Conclusion: 10 weeks are possible and optimal.")


if __name__ == "__main__":
    main()
