from cyberfusion.WorkItemAutomations.automations.base import Automation
from cyberfusion.WorkItemAutomations.config import NOPAutomationConfig


class NOPAutomation(Automation):
    """Do nothing."""

    def __init__(self, config: NOPAutomationConfig) -> None:
        """Set attributes."""
        super().__init__(config)

        self.config: NOPAutomationConfig = config

    def execute(self) -> None:
        """Execute automation."""
        self.save_last_execution()
