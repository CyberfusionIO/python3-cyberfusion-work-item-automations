from requests_mock import Mocker
import json
from cyberfusion.WorkItemAutomations.automations.create_issue import (
    CreateIssueAutomation,
)
from tests.factories import CreateIssueAutomationConfigFactory

from faker import Faker

from tests.helpers import mock_project_api, mock_group_api
import base64

faker = Faker()


def test_create_issue_with_assignee_group(
    requests_mock: Mocker,
):
    automation_config = CreateIssueAutomationConfigFactory.build()
    namespace, project_name = automation_config.project.split("/")

    project_id = mock_project_api(
        automation_config, requests_mock, namespace, project_name
    )

    _, members = mock_group_api(
        automation_config, requests_mock, automation_config.assignee_group
    )

    issue_mock = requests_mock.post(
        automation_config.url + "/api/v4/projects/" + str(project_id) + "/issues",
        status_code=201,
        json={
            "id": 4123,
            "iid": 102,
            "project_id": project_id,
            "title": automation_config.title,
            "description": automation_config.description,
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

    automation = CreateIssueAutomation(automation_config)

    # Test random selection

    assignee_ids = []

    for _ in range(60):
        automation.execute()

        assignee_ids.append(issue_mock.last_request.json()["assignee_id"])

    for member in members:
        assert member["id"] in assignee_ids

    # Test body

    last_request = issue_mock.last_request.json()

    assert "assignee_id" in last_request


def test_create_issue_without_assignee_group(
    requests_mock: Mocker,
):
    automation_config = CreateIssueAutomationConfigFactory.build(assignee_group=None)
    namespace, project_name = automation_config.project.split("/")

    project_id = mock_project_api(
        automation_config, requests_mock, namespace, project_name
    )

    issue_mock = requests_mock.post(
        automation_config.url + "/api/v4/projects/" + str(project_id) + "/issues",
        status_code=201,
        json={
            "id": 4123,
            "iid": 102,
            "project_id": project_id,
            "title": automation_config.title,
            "description": automation_config.description,
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
            "web_url": f"https://{automation_config.url}/example-group/example-project/-/issues/102",
            "time_stats": {
                "time_estimate": 0,
                "total_time_spent": 0,
                "human_time_estimate": None,
                "human_total_time_spent": None,
            },
            "task_completion_status": {"count": 0, "completed_count": 0},
            "weight": None,
            "blocking_issues_count": 0,
            "has_example-project": True,
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
                "full": "example-group/example-project#102",
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

    automation = CreateIssueAutomation(automation_config)

    automation.execute()

    # Test body

    last_request = issue_mock.last_request.json()

    assert "assignee_id" not in last_request


def test_create_issue_template(
    requests_mock: Mocker,
):
    template_name = faker.word()
    contents = faker.word()

    automation_config = CreateIssueAutomationConfigFactory.build(
        template=template_name, description=None
    )
    namespace, project_name = automation_config.project.split("/")

    project_id = mock_project_api(
        automation_config, requests_mock, namespace, project_name
    )

    mock_group_api(automation_config, requests_mock, automation_config.assignee_group)

    requests_mock.get(
        automation_config.url
        + "/api/v4/projects/"
        + str(project_id)
        + f"/repository/files/.gitlab%2Fissue_templates%2F{template_name}",
        status_code=200,
        json={
            "file_name": f"{template_name}.md",
            "file_path": f".gitlab/issue_templates/{template_name}.md",
            "size": 6208,
            "encoding": "base64",
            "content_sha256": "3e4e6201c5fc0dbaeed3dca2f15755ea7967a7f2791bb0c916933705e4cdb948",
            "ref": "HEAD",
            "blob_id": "919cf30d1ceb7c0f13090f3de0a5c6ea24752134",
            "commit_id": "b68c3a7c06b35e758614bc9d17a86531fe1b1dfd",
            "last_commit_id": "b68c3a7c06b35e758614bc9d17a86531fe1b1dfd",
            "execute_filemode": False,
            "content": base64.b64encode(contents.encode()).decode(),
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

    issue_mock = requests_mock.post(
        automation_config.url + "/api/v4/projects/" + str(project_id) + "/issues",
        status_code=201,
        json={
            "id": 4123,
            "iid": 102,
            "project_id": project_id,
            "title": automation_config.title,
            "description": contents,
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
            "web_url": f"https://{automation_config.url}/example-group/example-project/-/issues/102",
            "time_stats": {
                "time_estimate": 0,
                "total_time_spent": 0,
                "human_time_estimate": None,
                "human_total_time_spent": None,
            },
            "task_completion_status": {"count": 0, "completed_count": 0},
            "weight": None,
            "blocking_issues_count": 0,
            "has_example-project": True,
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
                "full": "example-group/example-project#102",
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

    automation = CreateIssueAutomation(automation_config)

    automation.execute()

    # Test body

    last_request = issue_mock.last_request.json()

    assert last_request["title"] == automation_config.title
    assert last_request["description"] == contents


def test_create_issue_description(
    requests_mock: Mocker,
):
    description = faker.word()

    automation_config = CreateIssueAutomationConfigFactory.build(
        template=None, description=description
    )
    namespace, project_name = automation_config.project.split("/")

    project_id = mock_project_api(
        automation_config, requests_mock, namespace, project_name
    )

    mock_group_api(automation_config, requests_mock, automation_config.assignee_group)

    issue_mock = requests_mock.post(
        automation_config.url + "/api/v4/projects/" + str(project_id) + "/issues",
        status_code=201,
        json={
            "id": 4123,
            "iid": 102,
            "project_id": project_id,
            "title": automation_config.title,
            "description": description,
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
            "web_url": f"https://{automation_config.url}/example-group/example-project/-/issues/102",
            "time_stats": {
                "time_estimate": 0,
                "total_time_spent": 0,
                "human_time_estimate": None,
                "human_total_time_spent": None,
            },
            "task_completion_status": {"count": 0, "completed_count": 0},
            "weight": None,
            "blocking_issues_count": 0,
            "has_example-project": True,
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
                "full": "example-group/example-project#102",
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

    automation = CreateIssueAutomation(automation_config)

    automation.execute()

    # Test body

    last_request = issue_mock.last_request.json()

    assert last_request["title"] == automation_config.title
    assert last_request["description"] == description
