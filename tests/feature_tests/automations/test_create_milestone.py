from requests_mock import Mocker
import json
from cyberfusion.WorkItemAutomations.automations.create_milestone import (
    CreateMilestoneAutomation,
)
from tests.factories import CreateMilestoneAutomationConfigFactory

from faker import Faker

from tests.helpers import mock_project_api

faker = Faker()


def test_create_milestone_with_description(
    requests_mock: Mocker,
):
    automation_config = CreateMilestoneAutomationConfigFactory.create()
    namespace, project_name = automation_config.project.split("/")

    project_id = mock_project_api(
        automation_config, requests_mock, namespace, project_name
    )

    milestone_mock = requests_mock.post(
        automation_config.url + "/api/v4/projects/" + str(project_id) + "/milestones",
        status_code=201,
        json={
            "id": 1,
            "iid": 1,
            "project_id": project_id,
            "title": automation_config.title,
            "description": automation_config.description,
            "state": "active",
            "created_at": "2025-01-25T16:14:34.946+01:00",
            "updated_at": "2025-01-25T16:14:34.946+01:00",
            "due_date": None,
            "start_date": None,
            "expired": False,
            "web_url": f"https://{automation_config.url}/{namespace}/{project_name}/-/milestones/1",
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

    automation = CreateMilestoneAutomation(automation_config)

    automation.execute()

    # Test body

    last_request = milestone_mock.last_request.json()

    assert last_request["title"] == CreateMilestoneAutomation.interpolate_title(
        automation_config.title
    )
    assert last_request["description"] == automation_config.description


def test_create_milestone_without_description(
    requests_mock: Mocker,
):
    automation_config = CreateMilestoneAutomationConfigFactory.create(description=None)
    namespace, project_name = automation_config.project.split("/")

    project_id = mock_project_api(
        automation_config, requests_mock, namespace, project_name
    )

    milestone_mock = requests_mock.post(
        automation_config.url + "/api/v4/projects/" + str(project_id) + "/milestones",
        status_code=201,
        json={
            "id": 1,
            "iid": 1,
            "project_id": project_id,
            "title": automation_config.title,
            "description": None,
            "state": "active",
            "created_at": "2025-01-25T16:14:34.946+01:00",
            "updated_at": "2025-01-25T16:14:34.946+01:00",
            "due_date": None,
            "start_date": None,
            "expired": False,
            "web_url": f"https://{automation_config.url}/{namespace}/{project_name}/-/milestones/1",
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

    automation = CreateMilestoneAutomation(automation_config)

    automation.execute()

    # Test body

    last_request = milestone_mock.last_request.json()

    assert last_request["title"] == CreateMilestoneAutomation.interpolate_title(
        automation_config.title
    )
    assert "description" not in last_request
