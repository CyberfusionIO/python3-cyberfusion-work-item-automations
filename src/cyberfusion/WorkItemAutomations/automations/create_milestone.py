from datetime import datetime

from cyberfusion.WorkItemAutomations.automations.base import Automation
from cyberfusion.WorkItemAutomations.config import CreateMilestoneAutomationConfig


class CreateMilestoneAutomation(Automation):
    """Create milestone."""

    def __init__(self, config: CreateMilestoneAutomationConfig) -> None:
        """Set attributes."""
        super().__init__(config)

        self.config: CreateMilestoneAutomationConfig = config

    @staticmethod
    def interpolate_title(title: str) -> str:
        """Get title with replaced variables."""
        return title.format(
            year=datetime.utcnow().year,
            month=datetime.utcnow().strftime("%B"),
        )

    def execute(self) -> None:
        """Execute automation."""
        project = self.gitlab_connector.projects.get(self.config.project)

        payload = {
            "title": self.interpolate_title(self.config.title),
        }

        if self.config.description:
            payload["description"] = self.config.description

        project.milestones.create(payload)

        self.save_last_execution()
