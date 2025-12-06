"""Config."""

from __future__ import annotations
from dataclasses import dataclass
from typing import List

import yaml
from functools import cached_property


@dataclass
class BaseAutomationConfig:
    """Automation config."""

    name: str
    schedule: str
    url: str
    private_token: str
    state_directory_path: str


@dataclass
class SummariseIssuesAutomationConfig(BaseAutomationConfig):
    """Automation config."""

    iteration_date_range: str | None
    project: str
    description: str


@dataclass
class CreateIssueAutomationConfig(BaseAutomationConfig):
    """Automation config."""

    project: str
    title: str
    assignee_group: str | None
    description: str | None = None
    template: str | None = None


@dataclass
class NOPAutomationConfig(BaseAutomationConfig):
    """Automation config."""


class Config:
    """Base config."""

    def __init__(self, path: str) -> None:
        """Path to config file."""
        self.path = path

    @cached_property
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
    def state_directory_path(self) -> str:
        """Get path to state directory."""
        return self._contents["state_directory_path"]

    @property
    def automations(self) -> List[BaseAutomationConfig]:
        """Get automations."""
        automations: List[BaseAutomationConfig] = []

        # Construct automation classes

        for automation in self._contents["automations"].get("create_issue", []):
            automations.append(
                CreateIssueAutomationConfig(
                    url=self.url,
                    private_token=self.private_token,
                    state_directory_path=self.state_directory_path,
                    name=automation["name"],
                    project=automation["project"],
                    title=automation["title"],
                    assignee_group=automation.get("assignee_group", None),
                    description=automation.get("description", None),
                    template=automation.get("template", None),
                    schedule=automation["schedule"],
                )
            )

        for automation in self._contents["automations"].get("nop", []):
            automations.append(
                NOPAutomationConfig(
                    url=self.url,
                    private_token=self.private_token,
                    state_directory_path=self.state_directory_path,
                    name=automation["name"],
                    schedule=automation["schedule"],
                )
            )

        for automation in self._contents["automations"].get("summarise_issues", []):
            automations.append(
                SummariseIssuesAutomationConfig(
                    url=self.url,
                    private_token=self.private_token,
                    state_directory_path=self.state_directory_path,
                    name=automation["name"],
                    schedule=automation["schedule"],
                    project=automation["project"],
                    iteration_date_range=automation["iteration_date_range"],
                    description=automation["description"],
                )
            )

        # Find duplicate names

        seen_names = []

        for automation in automations:
            if automation.name in seen_names:
                raise ValueError("Duplicate automation name: " + automation.name)

            seen_names.append(automation.name)

        return automations
