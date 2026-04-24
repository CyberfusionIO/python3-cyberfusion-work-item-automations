from cyberfusion.WorkItemAutomations.automations.create_issue import (
    CreateIssueAutomation,
)


def test_create_issue_interpolate_title() -> None:
    title = "{next_week_number} {current_month_number} {current_year}"

    next_week_number, current_month_number, current_year = (
        CreateIssueAutomation.interpolate_title(title).split(" ")
    )

    assert next_week_number.isdigit()
    assert current_month_number.isdigit()
    assert current_year.isdigit()


def test_create_issue_interpolate_description() -> None:
    description = "{year} {month}"

    year, month = CreateIssueAutomation.interpolate_description(description).split(" ")

    assert year.isdigit()
    assert month.isalpha()
