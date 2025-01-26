from gitlab.v4.objects.issues import Issue
from tabulate import tabulate
from datetime import datetime, timedelta
from cyberfusion.WorkItemAutomations.automations.base import Automation
from cyberfusion.WorkItemAutomations.config import SummariseIssuesAutomationConfig
import logging

logger = logging.getLogger(__name__)


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
    def generate_description(description: str, issues: list[Issue]) -> str:
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
                [issue.web_url, issue.title, ", ".join(assignees), " ".join(labels)]
            )

        table = tabulate(rows, headers, tablefmt="pipe")

        return description + "\n\n" + table

    def execute(self) -> None:
        """Execute automation."""
        summary_issue_title = "Issues summary '" + self.config.name + "'"

        # Get open issues

        all_open_issues = self.gitlab_connector.issues.list(
            scope="all", get_all=True, state="opened"
        )

        logger.info("Got %s open issues", len(all_open_issues))

        # Filter on iteration

        if self.config.iteration_date_range:
            iteration_date_range = self.interpolate_iteration_date_range(
                self.config.iteration_date_range
            )

            summary_issue_title += " (" + iteration_date_range + ")"

            summarise_issues = []

            for issue in all_open_issues:
                start_date = datetime.strptime(
                    iteration_date_range.split("/")[0], "%Y-%m-%d"
                )
                end_date = datetime.strptime(
                    iteration_date_range.split("/")[1], "%Y-%m-%d"
                )

                if not issue.iteration:
                    logger.info('Issue "%s" has no iteration', issue.title)

                    continue

                if (
                    datetime.strptime(issue.iteration["start_date"], "%Y-%m-%d")
                    < start_date
                ):
                    logger.info(
                        'Issue "%s" has an iteration with an earlier start date than %s, skipping',
                        issue.title,
                        start_date,
                    )

                    continue

                if (
                    datetime.strptime(issue.iteration["due_date"], "%Y-%m-%d")
                    > end_date
                ):
                    logger.info(
                        'Issue "%s" has an iteration with a later end date than %s, skipping',
                        issue.title,
                        end_date,
                    )

                    continue

                summarise_issues.append(issue)
        else:
            summarise_issues = all_open_issues

        logger.info("Got %s issues to summarise", len(summarise_issues))

        # Create summary issue

        payload = {
            "title": summary_issue_title,
            "description": self.generate_description(
                self.config.description, summarise_issues
            ),
        }

        project = self.gitlab_connector.projects.get(self.config.project)

        project.issues.create(payload)

        self.save_last_execution()
