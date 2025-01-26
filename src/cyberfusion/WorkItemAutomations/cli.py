"""CLI for GitLab work item automations.

Usage:
   glwia --config-file-path=<config-file-path>

Options:
  --config-file-path=<config-file-path>     Path to config file.
  -h --help                                 Show this screen.
"""

import logging

import docopt
import sys
from schema import Schema

from cyberfusion.WorkItemAutomations.automations.nop import NOPAutomation
from cyberfusion.WorkItemAutomations.automations.summarise_issues import (
    SummariseIssuesAutomation,
)
from cyberfusion.WorkItemAutomations.config import (
    Config,
    CreateIssueAutomationConfig,
    NOPAutomationConfig,
)
from cyberfusion.WorkItemAutomations.automations.create_issue import (
    CreateIssueAutomation,
)

root_logger = logging.getLogger()
root_logger.propagate = False
root_logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

root_logger.addHandler(stream_handler)

logger = logging.getLogger(__name__)


def get_args() -> docopt.Dict:
    """Get docopt args."""
    return docopt.docopt(__doc__)


def main() -> None:
    """Spawn relevant class for CLI function."""

    # Validate input

    args = get_args()
    schema = Schema(
        {
            "--config-file-path": str,
        }
    )
    args = schema.validate(args)

    # Get config

    config_file_path = args["--config-file-path"]

    config = Config(config_file_path)

    # Execute automations

    for automation_config in config.automations:
        if isinstance(automation_config, CreateIssueAutomationConfig):
            class_ = CreateIssueAutomation
        elif isinstance(automation_config, NOPAutomationConfig):
            class_ = NOPAutomation
        else:
            class_ = SummariseIssuesAutomation

        logger.info("Handling automation: %s", automation_config.name)

        automation_class = class_(automation_config)

        if not automation_class.should_execute:
            logger.info("Automation should not run: %s", automation_config.name)

            continue

        logger.info("Executing automation: %s", automation_config.name)

        automation_class.execute()

        logger.info("Executed automation: %s", automation_config.name)
