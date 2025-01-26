from pytest_mock import MockerFixture
import uuid
from requests_mock import Mocker
import pytest
import json
import os
import shutil
from typing import Generator


@pytest.fixture
def metadata_base_directory() -> Generator[str, None, None]:
    path = os.path.join(os.path.sep, "tmp", str(uuid.uuid4()))

    os.mkdir(path)

    yield path

    shutil.rmtree(path)


@pytest.fixture(autouse=True)
def metadata_file_base_path_mock(
    mocker: MockerFixture,
    metadata_base_directory: Generator[str, None, None],
    request: pytest.FixtureRequest,
) -> None:
    if "no_metadata_file_base_path_mock" in request.keywords:
        return

    mocker.patch(
        "cyberfusion.WorkItemAutomations.automations.base.Automation._metadata_file_base_path",
        new=mocker.PropertyMock(return_value=metadata_base_directory),
    )


@pytest.fixture(autouse=True)
def auth_mock(
    requests_mock: Mocker,
) -> None:
    requests_mock.get(
        "/api/v4/user",
        status_code=200,
        json={
            "id": 2,
            "username": "example",
            "name": "example",
            "state": "active",
            "locked": False,
            "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/2/avatar.png",
            "web_url": "https://gitlab.example.com/example",
            "created_at": "2018-12-09T22:59:27.676+01:00",
            "bio": "",
            "location": "",
            "public_email": "example@example.com",
            "skype": "",
            "linkedin": "",
            "twitter": "",
            "discord": "",
            "website_url": "",
            "organization": "",
            "job_title": "",
            "pronouns": "",
            "bot": False,
            "work_information": None,
            "local_time": None,
            "last_sign_in_at": "2025-01-25T14:16:57.963+01:00",
            "confirmed_at": "2018-12-09T22:59:27.500+01:00",
            "last_activity_on": "2025-01-25",
            "email": "example@example.com",
            "theme_id": 1,
            "color_scheme_id": 1,
            "projects_limit": 100000,
            "current_sign_in_at": "2025-01-25T15:56:44.939+01:00",
            "identities": [
                {
                    "provider": "ldapmain",
                    "extern_uid": "cn=example,cn=users,dc=cyberfusion,dc=cloud",
                    "saml_provider_id": None,
                }
            ],
            "can_create_group": True,
            "can_create_project": True,
            "two_factor_enabled": True,
            "external": False,
            "private_profile": False,
            "commit_email": "example@example.com",
            "shared_runners_minutes_limit": None,
            "extra_shared_runners_minutes_limit": None,
            "scim_identities": [],
            "is_admin": True,
            "note": None,
            "namespace_id": 2,
            "created_by": None,
            "email_reset_offered_at": None,
            "using_license_seat": True,
            "is_auditor": False,
            "provisioned_by_group_id": None,
            "enterprise_group_id": None,
            "enterprise_group_associated_at": None,
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
