from requests_mock import Mocker
import json
from cyberfusion.WorkItemAutomations.automations.create_issue import (
    CreateIssueAutomation,
)
from tests.factories import CreateIssueAutomationConfigFactory

from faker import Faker

faker = Faker()


def test_create_issue_with_assignee_group(
    requests_mock: Mocker,
):
    ID_PROJECT = faker.random_int()
    ID_GROUP_ASSIGNEE = faker.random_int()

    automation_config = CreateIssueAutomationConfigFactory.build()
    namespace, project_name = automation_config.project.split("/")

    requests_mock.get(
        automation_config.url + "/api/v4/projects/" + namespace + "%2F" + project_name,
        status_code=200,
        json={
            "id": ID_PROJECT,
            "description": "",
            "name": "Example Project",
            "name_with_namespace": "Example Group / Example Project",
            "path": "example-project",
            "path_with_namespace": "example-group/example-project",
            "created_at": "2024-12-19T15:00:55.841+01:00",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": f"git@{automation_config.url}:example-group/example-project.git",
            "http_url_to_repo": f"https://{automation_config.url}/example-group/example-project.git",
            "web_url": f"https://{automation_config.url}/example-group/example-project",
            "readme_url": f"https://{automation_config.url}/example-group/example-project/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": f"https://{automation_config.url}/uploads/-/system/project/avatar/"
            + str(ID_PROJECT)
            + "/1080x1080_c.png",
            "star_count": 0,
            "last_activity_at": "2025-01-24T21:01:51.150+01:00",
            "namespace": {
                "id": 272,
                "name": "Example Group",
                "path": "example-group",
                "kind": "group",
                "full_path": "example-group",
                "parent_id": None,
                "avatar_url": "/uploads/-/system/group/avatar/272/1080x1080_c.png",
                "web_url": f"https://{automation_config.url}/groups/example-group",
            },
            "repository_storage": "default",
            "_links": {
                "self": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT),
                "issues": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/issues",
                "merge_requests": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/merge_requests",
                "repo_branches": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/repository/branches",
                "labels": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/labels",
                "events": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/events",
                "members": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/members",
                "cluster_agents": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/cluster_agents",
            },
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "internal",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2024-12-20T15:00:55.951+01:00",
            },
            "repository_object_format": "sha1",
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": False,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "disabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": False,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_url": None,
            "import_type": None,
            "import_status": "none",
            "import_error": None,
            "open_issues_count": 1,
            "description_html": "",
            "updated_at": "2025-01-24T21:01:51.150+01:00",
            "ci_default_git_depth": 20,
            "ci_delete_pipelines_in_seconds": None,
            "ci_forward_deployment_enabled": True,
            "ci_forward_deployment_rollback_allowed": True,
            "ci_job_token_scope_enabled": False,
            "ci_separated_caches": True,
            "ci_allow_fork_pipelines_to_run_in_parent_project": True,
            "ci_id_token_sub_claim_components": ["project_path", "ref_type", "ref"],
            "build_git_strategy": "fetch",
            "keep_latest_artifact": True,
            "restrict_user_defined_variables": False,
            "ci_pipeline_variables_minimum_override_role": "maintainer",
            "runners_token": None,
            "runner_token_expiration_interval": None,
            "group_runners_enabled": True,
            "auto_cancel_pending_pipelines": "enabled",
            "build_timeout": 3600,
            "auto_devops_enabled": False,
            "auto_devops_deploy_strategy": "continuous",
            "ci_push_repository_for_job_token_allowed": False,
            "ci_config_path": "",
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "warn_about_potentially_unwanted_characters": True,
            "autoclose_referenced_issues": True,
            "approvals_before_merge": 0,
            "mirror": False,
            "external_authorization_classification_label": None,
            "marked_for_deletion_at": None,
            "marked_for_deletion_on": None,
            "requirements_enabled": False,
            "requirements_access_level": "enabled",
            "security_and_compliance_enabled": True,
            "compliance_frameworks": [],
            "issues_template": None,
            "merge_requests_template": None,
            "ci_restrict_pipeline_cancellation_role": "developer",
            "merge_pipelines_enabled": False,
            "merge_trains_enabled": False,
            "merge_trains_skip_train_allowed": False,
            "allow_pipeline_trigger_approve_deployment": False,
            "permissions": {
                "project_access": None,
                "group_access": {"access_level": 50, "notification_level": 3},
            },
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
        automation_config.url + "/api/v4/groups/" + automation_config.assignee_group,
        status_code=200,
        json={
            "id": ID_GROUP_ASSIGNEE,
            "web_url": f"https://{automation_config.url}/groups/"
            + automation_config.assignee_group,
            "name": "Example Assignee Group",
            "path": automation_config.assignee_group,
            "description": "User group",
            "visibility": "internal",
            "share_with_group_lock": False,
            "require_two_factor_authentication": False,
            "two_factor_grace_period": 48,
            "project_creation_level": "noone",
            "auto_devops_enabled": None,
            "subgroup_creation_level": "maintainer",
            "emails_disabled": False,
            "emails_enabled": True,
            "mentions_disabled": None,
            "lfs_enabled": True,
            "math_rendering_limits_enabled": True,
            "lock_math_rendering_limits_enabled": False,
            "default_branch": None,
            "default_branch_protection": 2,
            "default_branch_protection_defaults": {
                "allowed_to_push": [{"access_level": 40}],
                "allow_force_push": False,
                "allowed_to_merge": [{"access_level": 40}],
            },
            "avatar_url": None,
            "request_access_enabled": True,
            "full_name": "Example Assignee Group",
            "full_path": automation_config.assignee_group,
            "created_at": "2025-01-15T11:54:58.014+01:00",
            "parent_id": None,
            "organization_id": 1,
            "shared_runners_setting": "enabled",
            "ldap_cn": "Example Assignee Group",
            "ldap_access": 5,
            "ldap_group_links": [
                {
                    "cn": "Example Assignee Group",
                    "group_access": 5,
                    "provider": "ldapmain",
                    "filter": None,
                }
            ],
            "marked_for_deletion_on": None,
            "wiki_access_level": "enabled",
            "repository_storage": None,
            "duo_features_enabled": True,
            "lock_duo_features_enabled": False,
            "shared_with_groups": [],
            "runners_token": None,
            "enabled_git_access_protocol": "all",
            "prevent_sharing_groups_outside_hierarchy": False,
            "projects": [],
            "shared_projects": [],
            "shared_runners_minutes_limit": None,
            "extra_shared_runners_minutes_limit": None,
            "prevent_forking_outside_group": False,
            "service_access_tokens_expiration_enforced": True,
            "membership_lock": False,
            "ip_restriction_ranges": None,
            "allowed_email_domains_list": None,
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

    members = [
        {
            "id": 1,
            "username": "owner",
            "name": "owner",
            "state": "active",
            "locked": False,
            "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/1/avatar.png",
            "web_url": f"https://{automation_config.url}/owner",
            "access_level": 50,
            "created_at": "2025-01-15T11:54:58.083+01:00",
            "expires_at": None,
            "email": "owner@example.com",
            "override": False,
            "membership_state": "active",
        },
        {
            "id": 2,
            "username": "maintainer",
            "name": "maintainer",
            "state": "active",
            "locked": False,
            "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/2/avatar.png",
            "web_url": f"https://{automation_config.url}/maintainer",
            "access_level": 40,
            "created_at": "2025-01-15T11:54:58.083+01:00",
            "expires_at": None,
            "email": "maintainer@example.com",
            "override": False,
            "membership_state": "active",
        },
        {
            "id": 3,
            "username": "developer",
            "name": "developer",
            "state": "active",
            "locked": False,
            "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/3/avatar.png",
            "web_url": f"https://{automation_config.url}/developer",
            "access_level": 30,
            "created_at": "2025-01-15T11:54:58.083+01:00",
            "expires_at": None,
            "email": "developer@example.com",
            "override": False,
            "membership_state": "active",
        },
        {
            "id": 4,
            "username": "reporter",
            "name": "reporter",
            "state": "active",
            "locked": False,
            "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/4/avatar.png",
            "web_url": f"https://{automation_config.url}/reporter",
            "access_level": 20,
            "created_at": "2025-01-15T11:54:58.083+01:00",
            "expires_at": None,
            "email": "reporter@example.com",
            "override": False,
            "membership_state": "active",
        },
        {
            "id": 5,
            "username": "guest",
            "name": "guest",
            "state": "active",
            "locked": False,
            "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/5/avatar.png",
            "web_url": f"https://{automation_config.url}/guest",
            "access_level": 10,
            "created_at": "2025-01-15T11:54:58.083+01:00",
            "expires_at": None,
            "email": "guest@example.com",
            "override": False,
            "membership_state": "active",
        },
        {
            "id": 6,
            "username": "minimal-access",
            "name": "minimal-access",
            "state": "active",
            "locked": False,
            "avatar_url": f"https://{automation_config.url}/uploads/-/system/user/avatar/6/avatar.png",
            "web_url": f"https://{automation_config.url}/minimal-access",
            "access_level": 5,
            "created_at": "2025-01-15T11:54:58.083+01:00",
            "expires_at": None,
            "email": "minimal-access@example.com",
            "override": False,
            "membership_state": "active",
        },
    ]

    requests_mock.get(
        automation_config.url + "/api/v4/groups/" + str(ID_GROUP_ASSIGNEE) + "/members",
        status_code=200,
        json=members,
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
        automation_config.url + "/api/v4/projects/" + str(ID_PROJECT) + "/issues",
        status_code=201,
        json={
            "id": 4123,
            "iid": 102,
            "project_id": ID_PROJECT,
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
                + str(ID_PROJECT)
                + "/issues/102",
                "notes": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/issues/102/notes",
                "award_emoji": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/issues/102/award_emoji",
                "project": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT),
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

    # Test random selection

    assignee_ids = []

    for _ in range(30):
        automation.execute()

        assignee_ids.append(issue_mock.last_request.json()["assignee_id"])

    for member in members:
        assert member["id"] in assignee_ids

    # Test body

    last_request = issue_mock.last_request.json()

    assert last_request["title"] == automation_config.title
    assert last_request["description"] == automation_config.description
    assert "assignee_id" in last_request


def test_create_issue_without_assignee_group(
    requests_mock: Mocker,
):
    ID_PROJECT = faker.random_int()

    automation_config = CreateIssueAutomationConfigFactory.build(assignee_group=None)
    namespace, project_name = automation_config.project.split("/")

    requests_mock.get(
        automation_config.url + "/api/v4/projects/" + namespace + "%2F" + project_name,
        status_code=200,
        json={
            "id": ID_PROJECT,
            "description": "",
            "name": "Example Project",
            "name_with_namespace": "Example Group / Example Project",
            "path": "example-project",
            "path_with_namespace": "example-group/example-project",
            "created_at": "2024-12-19T15:00:55.841+01:00",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": f"git@{automation_config.url}:example-group/example-project.git",
            "http_url_to_repo": f"https://{automation_config.url}/example-group/example-project.git",
            "web_url": f"https://{automation_config.url}/example-group/example-project",
            "readme_url": f"https://{automation_config.url}/example-group/example-project/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": f"https://{automation_config.url}/uploads/-/system/project/avatar/"
            + str(ID_PROJECT)
            + "/1080x1080_c.png",
            "star_count": 0,
            "last_activity_at": "2025-01-24T21:01:51.150+01:00",
            "namespace": {
                "id": 272,
                "name": "Example Group",
                "path": "example-group",
                "kind": "group",
                "full_path": "example-group",
                "parent_id": None,
                "avatar_url": "/uploads/-/system/group/avatar/272/1080x1080_c.png",
                "web_url": f"https://{automation_config.url}/groups/example-group",
            },
            "repository_storage": "default",
            "_links": {
                "self": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT),
                "issues": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/issues",
                "merge_requests": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/merge_requests",
                "repo_branches": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/repository/branches",
                "labels": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/labels",
                "events": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/events",
                "members": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/members",
                "cluster_agents": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/cluster_agents",
            },
            "packages_enabled": True,
            "empty_repo": False,
            "archived": False,
            "visibility": "internal",
            "resolve_outdated_diff_discussions": False,
            "container_expiration_policy": {
                "cadence": "1d",
                "enabled": False,
                "keep_n": 10,
                "older_than": "90d",
                "name_regex": ".*",
                "name_regex_keep": None,
                "next_run_at": "2024-12-20T15:00:55.951+01:00",
            },
            "repository_object_format": "sha1",
            "issues_enabled": True,
            "merge_requests_enabled": True,
            "wiki_enabled": True,
            "jobs_enabled": True,
            "snippets_enabled": True,
            "container_registry_enabled": False,
            "service_desk_enabled": False,
            "service_desk_address": None,
            "can_create_merge_request_in": True,
            "issues_access_level": "enabled",
            "repository_access_level": "enabled",
            "merge_requests_access_level": "enabled",
            "forking_access_level": "enabled",
            "wiki_access_level": "enabled",
            "builds_access_level": "enabled",
            "snippets_access_level": "enabled",
            "pages_access_level": "private",
            "analytics_access_level": "enabled",
            "container_registry_access_level": "disabled",
            "security_and_compliance_access_level": "private",
            "releases_access_level": "enabled",
            "environments_access_level": "enabled",
            "feature_flags_access_level": "enabled",
            "infrastructure_access_level": "enabled",
            "monitor_access_level": "enabled",
            "model_experiments_access_level": "enabled",
            "model_registry_access_level": "enabled",
            "emails_disabled": False,
            "emails_enabled": True,
            "shared_runners_enabled": False,
            "lfs_enabled": True,
            "creator_id": 2,
            "import_url": None,
            "import_type": None,
            "import_status": "none",
            "import_error": None,
            "open_issues_count": 1,
            "description_html": "",
            "updated_at": "2025-01-24T21:01:51.150+01:00",
            "ci_default_git_depth": 20,
            "ci_delete_pipelines_in_seconds": None,
            "ci_forward_deployment_enabled": True,
            "ci_forward_deployment_rollback_allowed": True,
            "ci_job_token_scope_enabled": False,
            "ci_separated_caches": True,
            "ci_allow_fork_pipelines_to_run_in_parent_project": True,
            "ci_id_token_sub_claim_components": ["project_path", "ref_type", "ref"],
            "build_git_strategy": "fetch",
            "keep_latest_artifact": True,
            "restrict_user_defined_variables": False,
            "ci_pipeline_variables_minimum_override_role": "maintainer",
            "runners_token": None,
            "runner_token_expiration_interval": None,
            "group_runners_enabled": True,
            "auto_cancel_pending_pipelines": "enabled",
            "build_timeout": 3600,
            "auto_devops_enabled": False,
            "auto_devops_deploy_strategy": "continuous",
            "ci_push_repository_for_job_token_allowed": False,
            "ci_config_path": "",
            "public_jobs": True,
            "shared_with_groups": [],
            "only_allow_merge_if_pipeline_succeeds": False,
            "allow_merge_on_skipped_pipeline": None,
            "request_access_enabled": True,
            "only_allow_merge_if_all_discussions_are_resolved": False,
            "remove_source_branch_after_merge": True,
            "printing_merge_request_link_enabled": True,
            "merge_method": "merge",
            "squash_option": "default_off",
            "enforce_auth_checks_on_uploads": True,
            "suggestion_commit_message": None,
            "merge_commit_template": None,
            "squash_commit_template": None,
            "issue_branch_template": None,
            "warn_about_potentially_unwanted_characters": True,
            "autoclose_referenced_issues": True,
            "approvals_before_merge": 0,
            "mirror": False,
            "external_authorization_classification_label": None,
            "marked_for_deletion_at": None,
            "marked_for_deletion_on": None,
            "requirements_enabled": False,
            "requirements_access_level": "enabled",
            "security_and_compliance_enabled": True,
            "compliance_frameworks": [],
            "issues_template": None,
            "merge_requests_template": None,
            "ci_restrict_pipeline_cancellation_role": "developer",
            "merge_pipelines_enabled": False,
            "merge_trains_enabled": False,
            "merge_trains_skip_train_allowed": False,
            "allow_pipeline_trigger_approve_deployment": False,
            "permissions": {
                "project_access": None,
                "group_access": {"access_level": 50, "notification_level": 3},
            },
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
        automation_config.url + "/api/v4/projects/" + str(ID_PROJECT) + "/issues",
        status_code=201,
        json={
            "id": 4123,
            "iid": 102,
            "project_id": ID_PROJECT,
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
                + str(ID_PROJECT)
                + "/issues/102",
                "notes": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/issues/102/notes",
                "award_emoji": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT)
                + "/issues/102/award_emoji",
                "project": f"https://{automation_config.url}/api/v4/projects/"
                + str(ID_PROJECT),
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
    assert last_request["description"] == automation_config.description
    assert "assignee_id" not in last_request
