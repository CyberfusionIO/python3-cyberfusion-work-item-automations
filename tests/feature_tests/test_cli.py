from pytest_mock import MockerFixture
import docopt
import pytest
import json
from requests_mock import Mocker
from cyberfusion.WorkItemAutomations import cli
from cyberfusion.WorkItemAutomations.config import Config
from _pytest.logging import LogCaptureFixture
import logging


def test_cli_get_args() -> None:
    with pytest.raises(SystemExit):
        cli.get_args()


def test_cli_executes_automations(
    mocker: MockerFixture,
    requests_mock: Mocker,
    config: Config,
    example_project_name: str,
    example_group_name: str,
    caplog: LogCaptureFixture,
    metadata_file_base_path_mock: None,
) -> None:
    ID_PROJECT = 182

    mocker.patch(
        "cyberfusion.WorkItemAutomations.cli.get_args",
        return_value=docopt.docopt(
            cli.__doc__,
            ["--config-file-path", config.path],
        ),
    )

    mocker.patch(
        "cyberfusion.WorkItemAutomations.automations.Automation.should_execute",
        new=mocker.PropertyMock(return_value=True),
    )

    requests_mock.get(
        config.url
        + "/api/v4/projects/"
        + example_group_name
        + "%2F"
        + example_project_name,
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
            "ssh_url_to_repo": "git@gitlab.example.com:example-group/example-project.git",
            "http_url_to_repo": "https://gitlab.example.com/example-group/example-project.git",
            "web_url": "https://gitlab.example.com/example-group/example-project",
            "readme_url": "https://gitlab.example.com/example-group/example-project/-/blob/main/README.md",
            "forks_count": 0,
            "avatar_url": "https://gitlab.example.com/uploads/-/system/project/avatar/"
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
                "web_url": "https://gitlab.example.com/groups/example-group",
            },
            "repository_storage": "default",
            "_links": {
                "self": "https://gitlab.example.com/api/v4/projects/" + str(ID_PROJECT),
                "issues": "https://gitlab.example.com/api/v4/projects/"
                + str(ID_PROJECT)
                + "/issues",
                "merge_requests": "https://gitlab.example.com/api/v4/projects/"
                + str(ID_PROJECT)
                + "/merge_requests",
                "repo_branches": "https://gitlab.example.com/api/v4/projects/"
                + str(ID_PROJECT)
                + "/repository/branches",
                "labels": "https://gitlab.example.com/api/v4/projects/"
                + str(ID_PROJECT)
                + "/labels",
                "events": "https://gitlab.example.com/api/v4/projects/"
                + str(ID_PROJECT)
                + "/events",
                "members": "https://gitlab.example.com/api/v4/projects/"
                + str(ID_PROJECT)
                + "/members",
                "cluster_agents": "https://gitlab.example.com/api/v4/projects/"
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
        config.url + "/api/v4/projects/" + str(ID_PROJECT) + "/issues",
        status_code=201,
        json={
            "id": 4123,
            "iid": 102,
            "project_id": ID_PROJECT,
            "title": "Example title",
            "description": "Example description",
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
                "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/2/avatar.png",
                "web_url": "https://gitlab.example.com/example",
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
            "web_url": "https://gitlab.example.com/example-group/example-project/-/issues/102",
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
                "self": "https://gitlab.example.com/api/v4/projects/"
                + str(ID_PROJECT)
                + "/issues/102",
                "notes": "https://gitlab.example.com/api/v4/projects/"
                + str(ID_PROJECT)
                + "/issues/102/notes",
                "award_emoji": "https://gitlab.example.com/api/v4/projects/"
                + str(ID_PROJECT)
                + "/issues/102/award_emoji",
                "project": "https://gitlab.example.com/api/v4/projects/"
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

    with caplog.at_level(logging.INFO):
        cli.main()

    assert issue_mock.called

    for automation in config.automations:
        assert "Handling automation: " + automation.name in caplog.text
        assert "Executing automation: " + automation.name in caplog.text
        assert "Executed automation: " + automation.name in caplog.text


def test_cli_skips_automations(
    mocker: MockerFixture,
    config: Config,
    example_project_name: str,
    example_group_name: str,
    caplog: LogCaptureFixture,
    metadata_file_base_path_mock: None,
) -> None:
    mocker.patch(
        "cyberfusion.WorkItemAutomations.cli.get_args",
        return_value=docopt.docopt(
            cli.__doc__,
            ["--config-file-path", config.path],
        ),
    )

    mocker.patch(
        "cyberfusion.WorkItemAutomations.automations.Automation.should_execute",
        new=mocker.PropertyMock(return_value=False),
    )

    with caplog.at_level(logging.INFO):
        cli.main()

    for automation in config.automations:
        assert "Handling automation: " + automation.name in caplog.text
        assert "Automation should not run: " + automation.name in caplog.text
