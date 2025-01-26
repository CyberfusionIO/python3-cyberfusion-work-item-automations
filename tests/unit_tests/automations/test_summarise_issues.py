from cyberfusion.WorkItemAutomations.automations.summarise_issues import (
    SummariseIssuesAutomation,
)
from datetime import timedelta
from dateutil.parser import parse


def test_summarise_issues_interpolate_iteration_date_range() -> None:
    iteration_date_range = "{today} {today_plus_7_days} {today_minus_7_days}"

    today, today_plus_7_days, today_minus_7_days = (
        SummariseIssuesAutomation.interpolate_iteration_date_range(
            iteration_date_range
        ).split(" ")
    )

    # Test valid dates

    today = parse(today)
    today_plus_7_days = parse(today_plus_7_days)
    today_minus_7_days = parse(today_minus_7_days)

    # Valid date range

    assert today_plus_7_days.day == (today + timedelta(days=6)).day, (
        today_plus_7_days.day,
        today.day,
    )
    assert today_minus_7_days.day == (today - timedelta(days=6)).day, (
        today_minus_7_days.day,
        today.day,
    )
