from cyberfusion.Common import get_tmp_file

import yaml
import csv

from cyberfusion.WorkItemAutomations.config import Config, BaseAutomationConfig
from faker import Faker

from requests_mock import Mocker
import json
import os

faker = Faker()


def create_config(automations: dict) -> Config:
    path = get_tmp_file()

    first_automation = list(automations.values())[0][0]

    data = {
        "url": first_automation["url"],
        "private_token": first_automation["private_token"],
        "automations": automations,
        "state_directory_path": os.path.join(os.path.sep, "tmp", "glwia-tests"),
    }

    with open(path, "w") as f:
        yaml.dump(data, f)

    return Config(path)


def mock_project_api(
    automation_config: BaseAutomationConfig,
    requests_mock: Mocker,
    namespace: str,
    project_name: str,
) -> int:
    ID_PROJECT = faker.random_int()

    requests_mock.get(
        automation_config.url + "/api/v4/projects/" + namespace + "%2F" + project_name,
        status_code=200,
        json={
            "id": ID_PROJECT,
            "description": "",
            "name": project_name,
            "name_with_namespace": namespace + " / " + project_name,
            "path": project_name,
            "path_with_namespace": namespace + " / " + project_name,
            "created_at": "2024-12-19T15:00:55.841+01:00",
            "default_branch": "main",
            "tag_list": [],
            "topics": [],
            "ssh_url_to_repo": f"git@{automation_config.url}:{namespace}/{project_name}.git",
            "http_url_to_repo": f"https://{automation_config.url}/{namespace}/{project_name}.git",
            "web_url": f"https://{automation_config.url}/{namespace}/{project_name}",
            "readme_url": f"https://{automation_config.url}/{namespace}/{project_name}/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": f"https://{automation_config.url}/uploads/-/system/project/avatar/"
            + str(ID_PROJECT)
            + "/1080x1080_c.png",
            "star_count": 0,
            "last_activity_at": "2025-01-24T21:01:51.150+01:00",
            "namespace": {
                "id": 272,
                "name": namespace,
                "path": namespace,
                "kind": "group",
                "full_path": namespace,
                "parent_id": None,
                "avatar_url": "/uploads/-/system/group/avatar/272/1080x1080_c.png",
                "web_url": f"https://{automation_config.url}/groups/{namespace}",
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

    return ID_PROJECT


def mock_group_api(
    automation_config: BaseAutomationConfig, requests_mock: Mocker, name: str
) -> tuple[int, list]:
    ID_GROUP = faker.random_int()

    requests_mock.get(
        automation_config.url + "/api/v4/groups/" + name,
        status_code=200,
        json={
            "id": ID_GROUP,
            "web_url": f"https://{automation_config.url}/groups/" + name,
            "name": name,
            "path": name,
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
            "full_name": name,
            "full_path": name,
            "created_at": "2025-01-15T11:54:58.014+01:00",
            "parent_id": None,
            "organization_id": 1,
            "shared_runners_setting": "enabled",
            "ldap_cn": name,
            "ldap_access": 5,
            "ldap_group_links": [
                {
                    "cn": name,
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
        automation_config.url + "/api/v4/groups/" + str(ID_GROUP) + "/members",
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

    return ID_GROUP, members


def convert_markdown_table_to_dict(markdown_table: str) -> dict:
    lines = markdown_table.split("\n")

    reader = csv.DictReader(lines, delimiter="|")

    dict_ = []

    for row in list(reader)[1:]:  # Skip first row
        # Strip spaces. Ignore first empty column

        r = {k.strip(): v.strip() for k, v in row.items() if k != ""}

        dict_.append(r)

    return dict_
