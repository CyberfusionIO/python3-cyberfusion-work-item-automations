import os
from abc import ABCMeta, abstractmethod
from datetime import datetime

import gitlab
from functools import cached_property
from croniter import croniter

from cyberfusion.WorkItemAutomations.config import BaseAutomationConfig
from cyberfusion.WorkItemAutomations.gitlab import get_gitlab_connector
import logging

logger = logging.getLogger(__name__)


class AutomationInterface(metaclass=ABCMeta):
    """Automation interface."""

    def __init__(self, config: BaseAutomationConfig) -> None:
        """Set attributes."""

    @abstractmethod
    def execute(self) -> None:
        """Execute automation."""


class Automation(AutomationInterface):
    """Automation."""

    def __init__(self, config: BaseAutomationConfig) -> None:
        """Set attributes."""
        super().__init__(config)

        self.config = config

    @cached_property
    def gitlab_connector(self) -> gitlab.client.Gitlab:
        """Get GitLab connector."""
        logger.info("Connecting to GitLab at %s", self.config.url)

        return get_gitlab_connector(self.config.url, self.config.private_token)

    @property
    def _metadata_file_path(self) -> str:
        """Get path to metadata file."""
        return os.path.join(
            self.config.state_directory_path,
            self.config.name.replace(" ", "_").lower() + ".txt",
        )

    def save_last_execution(self) -> None:
        """Save when automation was executed last time."""
        with open(self._metadata_file_path, "w") as f:
            f.write(str(int(datetime.utcnow().timestamp())))

    @property
    def last_execution_time(self) -> datetime | None:
        """Get when automation was last executed."""
        if not os.path.exists(self._metadata_file_path):  # Not executed before
            return None

        with open(self._metadata_file_path, "r") as f:
            contents = f.read()

        return datetime.fromtimestamp(int(contents))

    @property
    def should_execute(self) -> bool:
        """Determine if automation should run based on schedule."""
        if not self.last_execution_time:  # Not executed before
            return True

        cron = croniter(self.config.schedule, self.last_execution_time)

        next_run = cron.get_next(datetime)

        return datetime.utcnow() >= next_run
