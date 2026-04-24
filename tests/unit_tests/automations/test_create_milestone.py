from cyberfusion.WorkItemAutomations.automations.create_milestone import (
    CreateMilestoneAutomation,
)


def test_create_milestone_interpolate_title() -> None:
    title = "{year} {month}"

    year, month = CreateMilestoneAutomation.interpolate_title(title).split(" ")

    assert year.isdigit()
    assert month.isalpha()
