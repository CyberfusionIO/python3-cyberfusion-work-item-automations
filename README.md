# python3-cyberfusion-work-item-automations

Automations for GitLab work items (issues, PRs, etc.)

The following automations are supported:

* Create recurring issues (using cron schedule)

GitLab doesn't support workflows natively. For example, there's no built-in way to create recurring issues, or take actions on issues when something happens to a PR, etc.
For the purpose of developing GitLab itself, GitLab does provide the external tool [`gitlab-triage`](https://gitlab.com/gitlab-org/ruby/gems/gitlab-triage). However, it is quite limiting: for example, it doesn't allow for creating standalone, recurring issues.

Although there are plans to implement [workflows for automation](https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/autoflow/) in GitLab itself, the timeline is unclear. Hence this project.

# Install

## PyPI

Run the following command to install the package from PyPI:

    pip3 install python3-cyberfusion-work-item-automations

## Debian

Run the following commands to build a Debian package:

    mk-build-deps -i -t 'apt -o Debug::pkgProblemResolver=yes --no-install-recommends -y'
    dpkg-buildpackage -us -uc

# Configure

No configuration is supported.

# Usage

## Create config file

In its most basic form, the config file must contain the URL to your GitLab instance, and a private token (PAT).
Create the PAT according to the [documentation](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#create-a-personal-access-token) with the `api` scope.

```yaml
automations: []
private_token: glpat-1aVadca471A281la331L
url: https://gitlab.example.com
```

On Debian, add the config file to `/etc/glwia.yml` (used by the automatically configured cron, running automations).
In any other environment, use a path of your choosing.

## Add automations

Add one or more automations to the `automations` key.

⚠️ Every automation must have a **unique** name.

### Create issues

```yaml
automations:
  create_issue:
    - name: Do something repetitive
      schedule: 5 13 3 * *
      # Project to create issue in. Format: # namespace/project
      project: example-group/example-project
      # Issue title
      #
      # Variables:
      #   - next_week_number (example: 5)
      #   - current_month_number (example: 1)
      #   - current_year (example: 2025)
      title: Check the yard for month {current_month_number}-{current_year}
      # Assign the issue to a member of this group
      #
      # Optional:
      #   If specified, issue is assigned to a **random** user in the specified group.
      #   If unspecified, the issue is not assigned to anyone.
      assignee_group: best-developers
      # Issue contents
      description: Check stuff, do stuff, ...
```

## Run automations

### Debian

On Debian, automations are automatically run every minute (according to each automation's respective schedule).

### Other environments

Run automations manually:

```bash
glwia --config-file-path /tmp/glwia.yml  # Short for 'GitLab Work Item Automations'
```

Set `--config-file-path` to a path of your choosing.
