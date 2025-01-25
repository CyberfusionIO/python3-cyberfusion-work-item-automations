import os
from datetime import datetime, timedelta

from pytest_mock import MockerFixture

from cyberfusion.WorkItemAutomations.automations import (
    NOPAutomation,
    CreateIssueAutomation,
)
from cyberfusion.WorkItemAutomations.config import Config, NOPAutomationConfig


def test_automation_never_executed(
    config: Config, metadata_file_base_path_mock: None
) -> None:
    """Test automation was never executed."""
    automation = NOPAutomation(
        NOPAutomationConfig(base=config, name="test", schedule="* * * * *")
    )

    assert os.path.exists(automation._metadata_file_path) is False

    assert automation.last_execution_time is None


def test_automation_saves_last_execution_time(
    config: Config, metadata_file_base_path_mock: None
) -> None:
    """Test executing automation saves last execution time."""
    automation = NOPAutomation(
        NOPAutomationConfig(base=config, name="test", schedule="* * * * *")
    )

    assert automation.last_execution_time is None

    automation.execute()

    assert os.path.exists(automation._metadata_file_path)
    assert automation.last_execution_time is not None


def test_automation_too_early(
    config: Config, metadata_file_base_path_mock: None
) -> None:
    """Test it being too early to execute the automation."""
    automation = NOPAutomation(
        NOPAutomationConfig(base=config, name="test", schedule="* * * * *")
    )

    assert automation.should_execute is True

    automation.execute()

    assert automation.should_execute is False


def test_automation_due(
    config: Config, mocker: MockerFixture, metadata_file_base_path_mock: None
) -> None:
    """Test it being time to execute the automation."""
    automation = NOPAutomation(
        NOPAutomationConfig(base=config, name="test", schedule="* * * * *")
    )

    assert automation.should_execute is True

    automation.execute()

    assert automation.should_execute is False  # Under normal circumstances

    # The next run is one minute from now, so pretend it's 1 minute ago - making
    # the next run *now*.

    current_time = datetime.utcnow() - timedelta(minutes=1)

    mocker.patch("croniter.croniter.croniter.get_next", return_value=current_time)

    assert automation.should_execute is True, (
        current_time,
        automation.last_execution_time,
    )


def test_metadata_file_base_path(config: Config) -> None:
    automation = NOPAutomation(
        NOPAutomationConfig(base=config, name="test", schedule="* * * * *")
    )

    assert automation._metadata_file_base_path == "/var/run"


def test_create_issue_interpolate_title() -> None:
    title = "{next_week_number} {current_month_number} {current_year}"

    next_week_number, current_month_number, current_year = (
        CreateIssueAutomation.interpolate_title(title).split(" ")
    )

    assert next_week_number.isdigit()
    assert current_month_number.isdigit()
    assert current_year.isdigit()
