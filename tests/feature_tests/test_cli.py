from pytest_mock import MockerFixture
import docopt
import pytest
from cyberfusion.WorkItemAutomations import cli
from _pytest.logging import LogCaptureFixture
import logging
from dataclasses import asdict

from tests.factories import (
    NOPAutomationConfigFactory,
    CreateIssueAutomationConfigFactory,
)
from tests.helpers import create_config


def test_cli_get_args() -> None:
    with pytest.raises(SystemExit):
        cli.get_args()


def test_cli_executes_automations(
    mocker: MockerFixture,
    caplog: LogCaptureFixture,
) -> None:
    automations = {
        "create_issue": [asdict(CreateIssueAutomationConfigFactory.build())],
        "nop": [asdict(NOPAutomationConfigFactory.build())],
    }

    config = create_config(automations)

    mocker.patch(
        "cyberfusion.WorkItemAutomations.cli.get_args",
        return_value=docopt.docopt(
            cli.__doc__,
            ["--config-file-path", config.path],
        ),
    )

    mocker.patch(
        "cyberfusion.WorkItemAutomations.automations.base.Automation.should_execute",
        new=mocker.PropertyMock(return_value=True),
    )
    mocker.patch(
        "cyberfusion.WorkItemAutomations.automations.create_issue.CreateIssueAutomation.execute",
        return_value=None,
    )
    mocker.patch(
        "cyberfusion.WorkItemAutomations.automations.nop.NOPAutomation.execute",
        return_value=None,
    )

    with caplog.at_level(logging.INFO):
        cli.main()

    for automation in config.automations:
        assert "Handling automation: " + automation.name in caplog.text
        assert "Executing automation: " + automation.name in caplog.text
        assert "Executed automation: " + automation.name in caplog.text


def test_cli_skips_automations(
    mocker: MockerFixture,
    caplog: LogCaptureFixture,
) -> None:
    automations = {
        "create_issue": [asdict(CreateIssueAutomationConfigFactory.build())],
        "nop": [asdict(NOPAutomationConfigFactory.build())],
    }

    config = create_config(automations)

    mocker.patch(
        "cyberfusion.WorkItemAutomations.cli.get_args",
        return_value=docopt.docopt(
            cli.__doc__,
            ["--config-file-path", config.path],
        ),
    )

    mocker.patch(
        "cyberfusion.WorkItemAutomations.automations.base.Automation.should_execute",
        new=mocker.PropertyMock(return_value=False),
    )

    with caplog.at_level(logging.INFO):
        cli.main()

    for automation in config.automations:
        assert "Handling automation: " + automation.name in caplog.text
        assert "Automation should not run: " + automation.name in caplog.text
