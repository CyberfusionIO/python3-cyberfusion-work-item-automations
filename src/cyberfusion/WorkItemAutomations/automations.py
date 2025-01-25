from abc import ABCMeta, abstractmethod
import gitlab
import os
from cached_property import cached_property
from datetime import datetime
from cyberfusion.WorkItemAutomations.config import (
    CreateIssueAutomationConfig,
    NOPAutomationConfig,
)
from croniter import croniter
from datetime import timedelta
from cyberfusion.WorkItemAutomations.config import AutomationConfig
from cyberfusion.WorkItemAutomations.gitlab import get_gitlab_connector
import random


class AutomationInterface(metaclass=ABCMeta):
    """Automation interface."""

    def __init__(self, config: AutomationConfig) -> None:
        """Set attributes."""

    @abstractmethod
    def execute(self) -> None:
        """Execute automation."""


class Automation(AutomationInterface):
    """Automation."""

    def __init__(self, config: AutomationConfig) -> None:
        """Set attributes."""
        super().__init__(config)

        self.config = config

    @cached_property  # type: ignore[misc]
    def gitlab_connector(self) -> gitlab.client.Gitlab:
        """Get GitLab connector."""
        return get_gitlab_connector(
            self.config.base.url, self.config.base.private_token
        )

    @property
    def _metadata_file_base_path(self) -> str:
        """Get base path in which metadata files are stored."""
        return os.path.join(
            os.path.sep,
            "var",
            "run",
        )

    @property
    def _metadata_file_path(self) -> str:
        """Get path to metadata file."""
        return os.path.join(
            self._metadata_file_base_path,
            "glwia-" + self.config.name.replace(" ", "_").lower() + ".txt",
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


class NOPAutomation(Automation):
    """Do nothing."""

    def __init__(self, config: NOPAutomationConfig) -> None:
        """Set attributes."""
        super().__init__(config)

        self.config = config

    def execute(self) -> None:
        """Execute automation."""
        self.save_last_execution()


class CreateIssueAutomation(Automation):
    """Create issue."""

    def __init__(self, config: CreateIssueAutomationConfig) -> None:
        """Set attributes."""
        super().__init__(config)

        self.config = config

    @staticmethod
    def interpolate_title(title: str) -> str:
        """Get title with replaced variables."""
        return title.format(
            next_week_number=(datetime.utcnow() + timedelta(weeks=1))
            .isocalendar()
            .week,
            current_month_number=datetime.utcnow().month,
            current_year=datetime.utcnow().year,
        )

    def execute(self) -> None:
        """Execute automation."""
        project = self.gitlab_connector.projects.get(self.config.project)

        payload = {
            "title": self.interpolate_title(self.config.title),
            "description": self.config.description,
        }

        if self.config.assignee_group:
            group = self.gitlab_connector.groups.get(self.config.assignee_group)

            all_members = group.members.list(get_all=True)

            payload["assignee_id"] = random.choice(all_members).id

        project.issues.create(payload)

        self.save_last_execution()
