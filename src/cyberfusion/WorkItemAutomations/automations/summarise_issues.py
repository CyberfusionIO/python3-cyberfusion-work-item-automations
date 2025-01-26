from gitlab.v4.objects.issues import Issue
from tabulate import tabulate
from datetime import datetime, timedelta
from cyberfusion.WorkItemAutomations.automations.base import Automation
from cyberfusion.WorkItemAutomations.config import SummariseIssuesAutomationConfig


class SummariseIssuesAutomation(Automation):
    """Summarise issues."""

    def __init__(self, config: SummariseIssuesAutomationConfig) -> None:
        """Set attributes."""
        super().__init__(config)

        self.config = config

    @staticmethod
    def interpolate_iteration_date_range(iteration_date_range: str) -> str:
        """Get iteration date range with replaced variables."""
        today = datetime.today().strftime("%Y-%m-%d")
        today_plus_7_days = datetime.today().date() + timedelta(days=6)
        today_minus_7_days = datetime.today().date() - timedelta(days=6)

        return iteration_date_range.format(
            today=today,
            today_plus_7_days=today_plus_7_days,
            today_minus_7_days=today_minus_7_days,
        )

    @staticmethod
    def generate_description(issues: list[Issue]) -> str:
        """Generate summary issue description containing Markdown table with filtered on issues."""
        rows = []

        headers = ["Issue", "Title", "Assignees", "Labels"]

        for issue in issues:
            # Set assignees

            assignees = []

            for assignee in issue.assignees:
                assignees.append("@" + assignee["username"])

            # Set labels

            labels = []

            for label in issue.labels:
                labels.append('~"' + label + '"')

            # Add row

            rows.append(
                [issue.web_url, issue.title, ", ".join(assignees), ", ".join(labels)]
            )

        return tabulate(rows, headers, tablefmt="pipe")

    def execute(self) -> None:
        """Execute automation."""
        summary_issue_title = "Issues summary '" + self.config.name + "'"

        # Get open issues

        all_open_issues = self.gitlab_connector.issues.list(
            scope="all", get_all=True, state="opened"
        )

        # Filter on iteration

        if self.config.iteration_date_range:
            iteration_date_range = self.interpolate_iteration_date_range(
                self.config.iteration_date_range
            )

            summary_issue_title += " (" + iteration_date_range + ")"

            summarise_issues = []

            for issue in all_open_issues:
                start_date, end_date = iteration_date_range.split("/")

                if not issue.iteration:
                    continue

                if issue.iteration["start_date"] < start_date:
                    continue

                if issue.iteration["due_date"] > end_date:
                    continue

                summarise_issues.append(issue)
        else:
            summarise_issues = all_open_issues

        # Create summary issue

        payload = {
            "title": summary_issue_title,
            "description": self.generate_description(summarise_issues),
        }

        project = self.gitlab_connector.projects.get(self.config.project)

        project.issues.create(payload)

        self.save_last_execution()
