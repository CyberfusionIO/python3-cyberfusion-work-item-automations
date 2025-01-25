"""CLI for GitLab work item automations.

Usage:
   glwia --config-file-path=<config-file-path>

Options:
  --config-file-path=<config-file-path>     Path to config file.
  -h --help                                 Show this screen.
"""

import logging

import docopt
from schema import Schema

from cyberfusion.WorkItemAutomations.config import Config
from cyberfusion.WorkItemAutomations.automations import CreateIssueAutomation

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
        class_ = CreateIssueAutomation

        logger.info("Handling automation: %s", automation_config.name)

        automation_class = class_(automation_config)

        if not automation_class.should_execute:
            logger.info("Automation should not run: %s", automation_config.name)

            continue

        logger.info("Executing automation: %s", automation_config.name)

        automation_class.execute()

        logger.info("Executed automation: %s", automation_config.name)
