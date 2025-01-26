import random
from datetime import datetime, timedelta

from cyberfusion.WorkItemAutomations.automations.base import Automation
from cyberfusion.WorkItemAutomations.config import CreateIssueAutomationConfig


class CreateIssueAutomation(Automation):
    """Create issue."""

    def __init__(self, config: CreateIssueAutomationConfig) -> None:
        """Set attributes."""
        super().__init__(config)

        self.config: CreateIssueAutomationConfig = config

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
