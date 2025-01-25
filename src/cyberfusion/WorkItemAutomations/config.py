"""Config."""

from __future__ import annotations
from dataclasses import dataclass
from typing import List

import yaml
from cached_property import cached_property


@dataclass
class AutomationConfig:
    """Automation config."""

    base: "Config"
    name: str
    schedule: str


@dataclass
class CreateIssueAutomationConfig(AutomationConfig):
    """Automation config."""

    project: str
    title: str
    assignee_group: str | None
    description: str


@dataclass
class NOPAutomationConfig(AutomationConfig):
    """Automation config."""


class Config:
    """Base config."""

    def __init__(self, path: str) -> None:
        """Path to config file."""
        self.path = path

    @cached_property  # type: ignore[misc]
    def _contents(self) -> dict:
        """Set config from YAML file."""
        with open(self.path, "rb") as fh:
            return yaml.load(fh.read(), Loader=yaml.SafeLoader)

    @property
    def url(self) -> str:
        """Get GitLab API URL."""
        return self._contents["url"]

    @property
    def private_token(self) -> str:
        """Get GitLab private token."""
        return self._contents["private_token"]

    @property
    def automations(self) -> List[AutomationConfig]:
        """Get automations."""
        automations: List[AutomationConfig] = []

        seen_names = []

        for automation in self._contents["automations"]["create_issue"]:
            if automation["name"] in seen_names:
                raise ValueError("Duplicate automation name: " + automation["name"])

            automations.append(
                CreateIssueAutomationConfig(
                    base=self,
                    name=automation["name"],
                    project=automation["project"],
                    title=automation["title"],
                    assignee_group=automation["assignee_group"]
                    if "assignee_group" in automation
                    else None,
                    description=automation["description"],
                    schedule=automation["schedule"],
                )
            )

            seen_names.append(automation["name"])

        return automations
