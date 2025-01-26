import os
from datetime import datetime, timedelta

from pytest_mock import MockerFixture

from cyberfusion.WorkItemAutomations.automations.nop import (
    NOPAutomation,
)

import pytest

from tests.factories import NOPAutomationConfigFactory
from tests.helpers import create_config
from dataclasses import asdict


def test_automation_never_executed() -> None:
    """Test automation was never executed."""
    config = create_config({"nop": [asdict(NOPAutomationConfigFactory.build())]})

    automation = NOPAutomation(config.automations[0])

    assert os.path.exists(automation._metadata_file_path) is False

    assert automation.last_execution_time is None


def test_automation_saves_last_execution_time() -> None:
    """Test executing automation saves last execution time."""
    config = create_config({"nop": [asdict(NOPAutomationConfigFactory.build())]})

    automation = NOPAutomation(config.automations[0])

    assert automation.last_execution_time is None

    automation.execute()

    assert os.path.exists(automation._metadata_file_path)
    assert automation.last_execution_time is not None


def test_automation_too_early() -> None:
    """Test it being too early to execute the automation."""
    config = create_config({"nop": [asdict(NOPAutomationConfigFactory.build())]})

    automation = NOPAutomation(config.automations[0])

    assert automation.should_execute is True

    automation.execute()

    assert automation.should_execute is False


def test_automation_due(
    mocker: MockerFixture,
) -> None:
    """Test it being time to execute the automation."""
    config = create_config({"nop": [asdict(NOPAutomationConfigFactory.build())]})

    automation = NOPAutomation(config.automations[0])

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


@pytest.mark.no_metadata_file_base_path_mock
def test_metadata_file_base_path() -> None:
    config = create_config({"nop": [asdict(NOPAutomationConfigFactory.build())]})

    automation = NOPAutomation(config.automations[0])

    assert automation._metadata_file_base_path == "/run/glwia"
