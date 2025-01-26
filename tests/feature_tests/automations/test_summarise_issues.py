from requests_mock import Mocker
from datetime import datetime, timedelta
import json
from cyberfusion.WorkItemAutomations.automations.summarise_issues import (
    SummariseIssuesAutomation,
)
from tests.factories import SummariseIssuesAutomationConfigFactory

from faker import Faker

from tests.helpers import mock_project_api, convert_markdown_table_to_dict

faker = Faker()


def test_summarise_issues_without_iteration_date_range(
    requests_mock: Mocker,
):
    automation_config = SummariseIssuesAutomationConfigFactory.build(
        iteration_date_range=None
    )
    namespace, project_name = automation_config.project.split("/")

    project_id = mock_project_api(
        automation_config, requests_mock, namespace, project_name
    )

    open_issue = {
        "id": 4169,
        "iid": 834,
        "project_id": 109,
        "title": faker.sentence(),
        "description": faker.sentence(),
        "state": "opened",
        "created_at": "2025-01-26T00:08:34.447+01:00",
        "updated_at": "2025-01-26T14:10:00.402+01:00",
        "closed_at": None,
        "closed_by": None,
        "labels": ["status::functional review", "type::usability improvement"],
        "milestone": None,
        "assignees": [
            {
                "id": 2,
                "username": "example-user-1",
                "name": "example-user-1",
                "state": "active",
                "locked": False,
                "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
                "web_url": f"https://{automation_config.url}/example-user-1",
            },
            {
                "id": 3,
                "username": "example-user-2",
                "name": "example-user-2",
                "state": "active",
                "locked": False,
                "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/3/avatar.png",
                "web_url": f"https://{automation_config.url}/example-user-2",
            },
        ],
        "author": {
            "id": 2,
            "username": "example-user-1",
            "name": "example-user-1",
            "state": "active",
            "locked": False,
            "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
            "web_url": f"https://{automation_config.url}/example-user-1",
        },
        "type": "ISSUE",
        "assignee": {
            "id": 2,
            "username": "example-user-1",
            "name": "example-user-1",
            "state": "active",
            "locked": False,
            "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
            "web_url": f"https://{automation_config.url}/example-user-1",
        },
        "user_notes_count": 0,
        "merge_requests_count": 1,
        "upvotes": 0,
        "downvotes": 0,
        "due_date": None,
        "confidential": False,
        "discussion_locked": None,
        "issue_type": "issue",
        "web_url": f"https://{automation_config.url}/example-group/example-project-2/-/issues/834",
        "time_stats": {
            "time_estimate": 0,
            "total_time_spent": 0,
            "human_time_estimate": None,
            "human_total_time_spent": None,
        },
        "task_completion_status": {"count": 0, "completed_count": 0},
        "weight": None,
        "blocking_issues_count": 0,
        "has_tasks": True,
        "task_status": "0 of 0 checklist items completed",
        "_links": {
            "self": f"https://{automation_config.url}/api/v4/projects/109/issues/834",
            "notes": f"https://{automation_config.url}/api/v4/projects/109/issues/834/notes",
            "award_emoji": f"https://{automation_config.url}/api/v4/projects/109/issues/834/award_emoji",
            "project": f"https://{automation_config.url}/api/v4/projects/109",
            "closed_as_duplicate_of": None,
        },
        "references": {
            "short": "#834",
            "relative": "#834",
            "full": "example-group/example-project-2#834",
        },
        "severity": "UNKNOWN",
        "moved_to_id": None,
        "imported": False,
        "imported_from": "none",
        "service_desk_reply_to": None,
        "epic_iid": None,
        "epic": None,
        "iteration": None,
    }

    issue_create_mock = requests_mock.post(
        automation_config.url + "/api/v4/projects/" + str(project_id) + "/issues",
        status_code=201,
        json={
            "id": 4123,
            "iid": 102,
            "project_id": project_id,
            "title": "",
            "description": "",
            "state": "opened",
            "created_at": "2025-01-25T16:14:34.946+01:00",
            "updated_at": "2025-01-25T16:14:34.946+01:00",
            "closed_at": None,
            "closed_by": None,
            "labels": [],
            "milestone": None,
            "assignees": [],
            "author": {
                "id": 2,
                "username": "example",
                "name": "example",
                "state": "active",
                "locked": False,
                "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
                "web_url": f"https://{automation_config.url}/example",
            },
            "type": "ISSUE",
            "assignee": None,
            "user_notes_count": 0,
            "merge_requests_count": 0,
            "upvotes": 0,
            "downvotes": 0,
            "due_date": None,
            "confidential": False,
            "discussion_locked": None,
            "issue_type": "issue",
            "web_url": f"https://{automation_config.url}/{namespace}/{project_name}/-/issues/102",
            "time_stats": {
                "time_estimate": 0,
                "total_time_spent": 0,
                "human_time_estimate": None,
                "human_total_time_spent": None,
            },
            "task_completion_status": {"count": 0, "completed_count": 0},
            "weight": None,
            "blocking_issues_count": 0,
            f"has_{project_name}": True,
            "task_status": "0 of 0 checklist items completed",
            "_links": {
                "self": f"https://{automation_config.url}/api/v4/projects/"
                + str(project_id)
                + "/issues/102",
                "notes": f"https://{automation_config.url}/api/v4/projects/"
                + str(project_id)
                + "/issues/102/notes",
                "award_emoji": f"https://{automation_config.url}/api/v4/projects/"
                + str(project_id)
                + "/issues/102/award_emoji",
                "project": f"https://{automation_config.url}/api/v4/projects/"
                + str(project_id),
                "closed_as_duplicate_of": None,
            },
            "references": {
                "short": "#102",
                "relative": "#102",
                "full": f"{namespace}/{project_name}#102",
            },
            "severity": "UNKNOWN",
            "subscribed": True,
            "moved_to_id": None,
            "imported": False,
            "imported_from": "none",
            "service_desk_reply_to": None,
            "epic_iid": None,
            "epic": None,
            "iteration": None,
        },
        headers={
            "content-type": "application/json",
            "x-content-type-options": "nosniff",
            "x-frame-options": "SAMEORIGIN",
            "x-gitlab-meta": json.dumps(
                {"correlation_id": "EPXXHF7KVW6MZWEL43VXMFHKBH", "version": "1"}
            ),
            "x-request-id": "EPXXHF7KVW6MZWEL43VXMFHKBH",
            "x-runtime": "0.248834",
            "strict-transport-security": "max-age=63072000",
            "referrer-policy": "strict-origin-when-cross-origin",
        },
    )

    requests_mock.get(
        automation_config.url + "/api/v4/issues?state=opened&scope=all",
        status_code=200,
        json=[open_issue],
        headers={
            "content-type": "application/json",
            "x-content-type-options": "nosniff",
            "x-frame-options": "SAMEORIGIN",
            "x-gitlab-meta": json.dumps(
                {"correlation_id": "EPXXHF7KVW6MZWEL43VXMFHKBH", "version": "1"}
            ),
            "x-request-id": "EPXXHF7KVW6MZWEL43VXMFHKBH",
            "x-runtime": "0.248834",
            "strict-transport-security": "max-age=63072000",
            "referrer-policy": "strict-origin-when-cross-origin",
        },
    )

    automation = SummariseIssuesAutomation(automation_config)

    automation.execute()

    # Test body

    last_request = issue_create_mock.last_request.json()

    assert last_request["title"] == f"Issues summary '{automation_config.name}'"

    table = convert_markdown_table_to_dict(
        "|"
        + last_request["description"].split("|", 1)[1]  # Remove everything before table
    )

    assert all(
        row["Issue"]
        in [
            open_issue["web_url"],
        ]
        for row in table
    )
    assert "Title" in table[0]
    assert "Assignees" in table[0]
    assert "Labels" in table[0]


def test_summarise_issues_with_iteration_date_range(
    requests_mock: Mocker,
):
    iteration_date_range = "{today}/{today_plus_7_days}"

    automation_config = SummariseIssuesAutomationConfigFactory.build(
        iteration_date_range=iteration_date_range
    )
    namespace, project_name = automation_config.project.split("/")

    project_id = mock_project_api(
        automation_config, requests_mock, namespace, project_name
    )

    today = datetime.today()

    issues = [
        # Start date doesn't match, end date does
        {
            "id": 4106,
            "iid": 96,
            "project_id": 182,
            "title": faker.sentence(),
            "description": faker.sentence(),
            "state": "opened",
            "created_at": "2025-01-24T11:37:43.860+01:00",
            "updated_at": "2025-01-24T14:27:01.242+01:00",
            "closed_at": None,
            "closed_by": None,
            "labels": ["area::tech", "state::draft", "status::to do"],
            "milestone": None,
            "assignees": [
                {
                    "id": 2,
                    "username": "example-user-1",
                    "name": "example-user-1",
                    "state": "active",
                    "locked": False,
                    "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
                    "web_url": f"https://{automation_config.url}/example-user-1",
                },
                {
                    "id": 3,
                    "username": "example-user-2",
                    "name": "example-user-2",
                    "state": "active",
                    "locked": False,
                    "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/3/avatar.png",
                    "web_url": f"https://{automation_config.url}/example-user-2",
                },
            ],
            "author": {
                "id": 2,
                "username": "example-user-1",
                "name": "example-user-1",
                "state": "active",
                "locked": False,
                "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
                "web_url": f"https://{automation_config.url}/example-user-1",
            },
            "type": "ISSUE",
            "assignee": {
                "id": 2,
                "username": "example-user-1",
                "name": "example-user-1",
                "state": "active",
                "locked": False,
                "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
                "web_url": f"https://{automation_config.url}/example-user-1",
            },
            "user_notes_count": 0,
            "merge_requests_count": 0,
            "upvotes": 0,
            "downvotes": 0,
            "due_date": None,
            "confidential": True,
            "discussion_locked": None,
            "issue_type": "issue",
            "web_url": f"https://{automation_config.url}/example-group/example-project/-/issues/96",
            "time_stats": {
                "time_estimate": 0,
                "total_time_spent": 0,
                "human_time_estimate": None,
                "human_total_time_spent": None,
            },
            "task_completion_status": {"count": 8, "completed_count": 5},
            "weight": None,
            "blocking_issues_count": 0,
            "has_tasks": False,
            "_links": {
                "self": f"https://{automation_config.url}/api/v4/projects/182/issues/96",
                "notes": f"https://{automation_config.url}/api/v4/projects/182/issues/96/notes",
                "award_emoji": f"https://{automation_config.url}/api/v4/projects/182/issues/96/award_emoji",
                "project": f"https://{automation_config.url}/api/v4/projects/182",
                "closed_as_duplicate_of": None,
            },
            "references": {
                "short": "#96",
                "relative": "#96",
                "full": "example-group/example-project#96",
            },
            "severity": "UNKNOWN",
            "moved_to_id": None,
            "imported": False,
            "imported_from": "none",
            "service_desk_reply_to": None,
            "epic_iid": None,
            "epic": None,
            "iteration": {
                "id": 13,
                "iid": 2,
                "sequence": 2,
                "group_id": 272,
                "title": None,
                "description": None,
                "state": 2,
                "created_at": "2025-01-13T11:32:02.925+01:00",
                "updated_at": "2025-01-20T00:05:07.072+01:00",
                "start_date": (today - timedelta(days=1)).strftime(
                    "%Y-%m-%d"
                ),  # Before start date (today)
                "due_date": today.strftime("%Y-%m-%d"),
                "web_url": f"https://{automation_config.url}/groups/example-group/-/iterations/13",
            },
        },
        # Start date matches, end date doesn't
        {
            "id": 3881,
            "iid": 50,
            "project_id": 182,
            "title": faker.sentence(),
            "description": faker.sentence(),
            "state": "opened",
            "created_at": "2025-01-02T21:23:54.130+01:00",
            "updated_at": "2025-01-13T13:16:50.750+01:00",
            "closed_at": None,
            "closed_by": None,
            "labels": ["area::productivity", "state::complete", "status::doing"],
            "milestone": None,
            "assignees": [
                {
                    "id": 2,
                    "username": "example-user-1",
                    "name": "example-user-1",
                    "state": "active",
                    "locked": False,
                    "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
                    "web_url": f"https://{automation_config.url}/example-user-1",
                },
                {
                    "id": 3,
                    "username": "example-user-2",
                    "name": "example-user-2",
                    "state": "active",
                    "locked": False,
                    "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/3/avatar.png",
                    "web_url": f"https://{automation_config.url}/example-user-2",
                },
            ],
            "author": {
                "id": 2,
                "username": "example-user-1",
                "name": "example-user-1",
                "state": "active",
                "locked": False,
                "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
                "web_url": f"https://{automation_config.url}/example-user-1",
            },
            "type": "ISSUE",
            "assignee": {
                "id": 2,
                "username": "example-user-1",
                "name": "example-user-1",
                "state": "active",
                "locked": False,
                "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
                "web_url": f"https://{automation_config.url}/example-user-1",
            },
            "user_notes_count": 4,
            "merge_requests_count": 0,
            "upvotes": 0,
            "downvotes": 0,
            "due_date": None,
            "confidential": False,
            "discussion_locked": None,
            "issue_type": "issue",
            "web_url": f"https://{automation_config.url}/example-group/example-project/-/issues/50",
            "time_stats": {
                "time_estimate": 0,
                "total_time_spent": 0,
                "human_time_estimate": None,
                "human_total_time_spent": None,
            },
            "task_completion_status": {"count": 0, "completed_count": 0},
            "weight": None,
            "blocking_issues_count": 0,
            "has_tasks": True,
            "task_status": "0 of 0 checklist items completed",
            "_links": {
                "self": f"https://{automation_config.url}/api/v4/projects/182/issues/50",
                "notes": f"https://{automation_config.url}/api/v4/projects/182/issues/50/notes",
                "award_emoji": f"https://{automation_config.url}/api/v4/projects/182/issues/50/award_emoji",
                "project": f"https://{automation_config.url}/api/v4/projects/182",
                "closed_as_duplicate_of": None,
            },
            "references": {
                "short": "#50",
                "relative": "#50",
                "full": "example-group/example-project#50",
            },
            "severity": "UNKNOWN",
            "moved_to_id": None,
            "imported": False,
            "imported_from": "none",
            "service_desk_reply_to": None,
            "epic_iid": None,
            "epic": None,
            "iteration": {
                "id": 12,
                "iid": 1,
                "sequence": 1,
                "group_id": 272,
                "title": None,
                "description": None,
                "state": 3,
                "created_at": "2025-01-13T11:32:02.921+01:00",
                "updated_at": "2025-01-20T00:05:07.136+01:00",
                "start_date": today.strftime("%Y-%m-%d"),
                "due_date": (today + timedelta(days=8)).strftime(
                    "%Y-%m-%d"
                ),  # Longer than 7 days
                "web_url": f"https://{automation_config.url}/groups/example-group/-/iterations/12",
            },
        },
        # Start date matches, end date matches
        {
            "id": 3882,
            "iid": 51,
            "project_id": 182,
            "title": faker.sentence(),
            "description": faker.sentence(),
            "state": "opened",
            "created_at": "2025-01-02T21:23:54.130+01:00",
            "updated_at": "2025-01-13T13:16:50.750+01:00",
            "closed_at": None,
            "closed_by": None,
            "labels": ["area::productivity", "state::complete", "status::doing"],
            "milestone": None,
            "assignees": [
                {
                    "id": 2,
                    "username": "example-user-1",
                    "name": "example-user-1",
                    "state": "active",
                    "locked": False,
                    "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
                    "web_url": f"https://{automation_config.url}/example-user-1",
                },
                {
                    "id": 3,
                    "username": "example-user-2",
                    "name": "example-user-2",
                    "state": "active",
                    "locked": False,
                    "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/3/avatar.png",
                    "web_url": f"https://{automation_config.url}/example-user-2",
                },
            ],
            "author": {
                "id": 2,
                "username": "example-user-1",
                "name": "example-user-1",
                "state": "active",
                "locked": False,
                "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
                "web_url": f"https://{automation_config.url}/example-user-1",
            },
            "type": "ISSUE",
            "assignee": {
                "id": 2,
                "username": "example-user-1",
                "name": "example-user-1",
                "state": "active",
                "locked": False,
                "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
                "web_url": f"https://{automation_config.url}/example-user-1",
            },
            "user_notes_count": 4,
            "merge_requests_count": 0,
            "upvotes": 0,
            "downvotes": 0,
            "due_date": None,
            "confidential": False,
            "discussion_locked": None,
            "issue_type": "issue",
            "web_url": f"https://{automation_config.url}/example-group/example-project/-/issues/51",
            "time_stats": {
                "time_estimate": 0,
                "total_time_spent": 0,
                "human_time_estimate": None,
                "human_total_time_spent": None,
            },
            "task_completion_status": {"count": 0, "completed_count": 0},
            "weight": None,
            "blocking_issues_count": 0,
            "has_tasks": True,
            "task_status": "0 of 0 checklist items completed",
            "_links": {
                "self": f"https://{automation_config.url}/api/v4/projects/182/issues/51",
                "notes": f"https://{automation_config.url}/api/v4/projects/182/issues/51/notes",
                "award_emoji": f"https://{automation_config.url}/api/v4/projects/182/issues/51/award_emoji",
                "project": f"https://{automation_config.url}/api/v4/projects/182",
                "closed_as_duplicate_of": None,
            },
            "references": {
                "short": "#51",
                "relative": "#51",
                "full": "example-group/example-project#51",
            },
            "severity": "UNKNOWN",
            "moved_to_id": None,
            "imported": False,
            "imported_from": "none",
            "service_desk_reply_to": None,
            "epic_iid": None,
            "epic": None,
            "iteration": {
                "id": 12,
                "iid": 1,
                "sequence": 1,
                "group_id": 272,
                "title": None,
                "description": None,
                "state": 3,
                "created_at": "2025-01-13T11:32:02.921+01:00",
                "updated_at": "2025-01-20T00:05:07.136+01:00",
                "start_date": today.strftime("%Y-%m-%d"),
                "due_date": (today + timedelta(days=2)).strftime(
                    "%Y-%m-%d"
                ),  # Shorter than 7 days
                "web_url": f"https://{automation_config.url}/groups/example-group/-/iterations/12",
            },
        },
        # No iteration
        {
            "id": 3883,
            "iid": 52,
            "project_id": 182,
            "title": faker.sentence(),
            "description": faker.sentence(),
            "state": "opened",
            "created_at": "2025-01-02T21:23:54.130+01:00",
            "updated_at": "2025-01-13T13:16:50.750+01:00",
            "closed_at": None,
            "closed_by": None,
            "labels": ["area::productivity", "state::complete", "status::doing"],
            "milestone": None,
            "assignees": [
                {
                    "id": 2,
                    "username": "example-user-1",
                    "name": "example-user-1",
                    "state": "active",
                    "locked": False,
                    "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
                    "web_url": f"https://{automation_config.url}/example-user-1",
                },
                {
                    "id": 3,
                    "username": "example-user-2",
                    "name": "example-user-2",
                    "state": "active",
                    "locked": False,
                    "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/3/avatar.png",
                    "web_url": f"https://{automation_config.url}/example-user-2",
                },
            ],
            "author": {
                "id": 2,
                "username": "example-user-1",
                "name": "example-user-1",
                "state": "active",
                "locked": False,
                "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
                "web_url": f"https://{automation_config.url}/example-user-1",
            },
            "type": "ISSUE",
            "assignee": {
                "id": 2,
                "username": "example-user-1",
                "name": "example-user-1",
                "state": "active",
                "locked": False,
                "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
                "web_url": f"https://{automation_config.url}/example-user-1",
            },
            "user_notes_count": 4,
            "merge_requests_count": 0,
            "upvotes": 0,
            "downvotes": 0,
            "due_date": None,
            "confidential": False,
            "discussion_locked": None,
            "issue_type": "issue",
            "web_url": f"https://{automation_config.url}/example-group/example-project/-/issues/52",
            "time_stats": {
                "time_estimate": 0,
                "total_time_spent": 0,
                "human_time_estimate": None,
                "human_total_time_spent": None,
            },
            "task_completion_status": {"count": 0, "completed_count": 0},
            "weight": None,
            "blocking_issues_count": 0,
            "has_tasks": True,
            "task_status": "0 of 0 checklist items completed",
            "_links": {
                "self": f"https://{automation_config.url}/api/v4/projects/182/issues/52",
                "notes": f"https://{automation_config.url}/api/v4/projects/182/issues/52/notes",
                "award_emoji": f"https://{automation_config.url}/api/v4/projects/182/issues/52/award_emoji",
                "project": f"https://{automation_config.url}/api/v4/projects/182",
                "closed_as_duplicate_of": None,
            },
            "references": {
                "short": "#52",
                "relative": "#52",
                "full": "example-group/example-project#52",
            },
            "severity": "UNKNOWN",
            "moved_to_id": None,
            "imported": False,
            "imported_from": "none",
            "service_desk_reply_to": None,
            "epic_iid": None,
            "epic": None,
            "iteration": None,
        },
    ]

    issue_create_mock = requests_mock.post(
        automation_config.url + "/api/v4/projects/" + str(project_id) + "/issues",
        status_code=201,
        json={
            "id": 4123,
            "iid": 102,
            "project_id": project_id,
            "title": "",
            "description": "",
            "state": "opened",
            "created_at": "2025-01-25T16:14:34.946+01:00",
            "updated_at": "2025-01-25T16:14:34.946+01:00",
            "closed_at": None,
            "closed_by": None,
            "labels": [],
            "milestone": None,
            "assignees": [],
            "author": {
                "id": 2,
                "username": "example",
                "name": "example",
                "state": "active",
                "locked": False,
                "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
                "web_url": f"https://{automation_config.url}/example",
            },
            "type": "ISSUE",
            "assignee": None,
            "user_notes_count": 0,
            "merge_requests_count": 0,
            "upvotes": 0,
            "downvotes": 0,
            "due_date": None,
            "confidential": False,
            "discussion_locked": None,
            "issue_type": "issue",
            "web_url": f"https://{automation_config.url}/{namespace}/{project_name}/-/issues/102",
            "time_stats": {
                "time_estimate": 0,
                "total_time_spent": 0,
                "human_time_estimate": None,
                "human_total_time_spent": None,
            },
            "task_completion_status": {"count": 0, "completed_count": 0},
            "weight": None,
            "blocking_issues_count": 0,
            f"has_{project_name}": True,
            "task_status": "0 of 0 checklist items completed",
            "_links": {
                "self": f"https://{automation_config.url}/api/v4/projects/"
                + str(project_id)
                + "/issues/102",
                "notes": f"https://{automation_config.url}/api/v4/projects/"
                + str(project_id)
                + "/issues/102/notes",
                "award_emoji": f"https://{automation_config.url}/api/v4/projects/"
                + str(project_id)
                + "/issues/102/award_emoji",
                "project": f"https://{automation_config.url}/api/v4/projects/"
                + str(project_id),
                "closed_as_duplicate_of": None,
            },
            "references": {
                "short": "#102",
                "relative": "#102",
                "full": f"{namespace}/{project_name}#102",
            },
            "severity": "UNKNOWN",
            "subscribed": True,
            "moved_to_id": None,
            "imported": False,
            "imported_from": "none",
            "service_desk_reply_to": None,
            "epic_iid": None,
            "epic": None,
            "iteration": None,
        },
        headers={
            "content-type": "application/json",
            "x-content-type-options": "nosniff",
            "x-frame-options": "SAMEORIGIN",
            "x-gitlab-meta": json.dumps(
                {"correlation_id": "EPXXHF7KVW6MZWEL43VXMFHKBH", "version": "1"}
            ),
            "x-request-id": "EPXXHF7KVW6MZWEL43VXMFHKBH",
            "x-runtime": "0.248834",
            "strict-transport-security": "max-age=63072000",
            "referrer-policy": "strict-origin-when-cross-origin",
        },
    )

    requests_mock.get(
        automation_config.url + "/api/v4/issues?state=opened&scope=all",
        status_code=200,
        json=issues,
        headers={
            "content-type": "application/json",
            "x-content-type-options": "nosniff",
            "x-frame-options": "SAMEORIGIN",
            "x-gitlab-meta": json.dumps(
                {"correlation_id": "EPXXHF7KVW6MZWEL43VXMFHKBH", "version": "1"}
            ),
            "x-request-id": "EPXXHF7KVW6MZWEL43VXMFHKBH",
            "x-runtime": "0.248834",
            "strict-transport-security": "max-age=63072000",
            "referrer-policy": "strict-origin-when-cross-origin",
        },
    )

    automation = SummariseIssuesAutomation(automation_config)

    automation.execute()

    # Test body

    last_request = issue_create_mock.last_request.json()

    assert (
        last_request["title"]
        == f"Issues summary '{automation_config.name}' ("
        + SummariseIssuesAutomation.interpolate_iteration_date_range(
            iteration_date_range
        )
        + ")"
    )

    table = convert_markdown_table_to_dict(
        "|"
        + last_request["description"].split("|", 1)[1]  # Remove everything before table
    )

    assert not any(
        row["Issue"]
        in [issues[0]["web_url"], issues[1]["web_url"], issues[3]["web_url"]]
        for row in table
    )
    assert any(row["Issue"] in [issues[2]["web_url"]] for row in table)

    assert "Title" in table[0]
    assert "Assignees" in table[0]
    assert "Labels" in table[0]
