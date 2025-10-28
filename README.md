# python3-cyberfusion-work-item-automations

Automations for GitLab work items (issues, PRs, etc.)

The following automations are supported:

* Create recurring issues (using cron schedule)
* Summarise issues (useful for sprints, stand-ups, etc.)

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
To the private token's user - usually a dedicated bot account - grant access to projects and/or groups it must be able to access, depending on your configuration.
The necessary role, e.g. 'Guest' or 'Developer', depends on the actions taken. Usually, granting the 'Developer' role suffices.

```yaml
automations: {}
private_token: glpat-...
url: https://gitlab.example.com
state_directory_path: /tmp/glwia
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
      # or use a template (see https://docs.gitlab.com/user/project/description_templates/#create-an-issue-template)
      template: check_stuff.md
```

Want to add properties to the issue, such as labels or an assignee?
Use [quick actions](https://docs.gitlab.com/ee/user/project/quick_actions.html#issues-merge-requests-and-epics).
For example:

```yaml
automations:
  create_issue:
    - name: Do something repetitive
      ...
      description: |
        /assign @ceo
        /label ~"status::to do"
```

### Summarise issues

```yaml
automations:
  summarise_issues:
    - name: Summarise this week's issues (start-of-week stand-up)
      schedule: 0 11 * * 1  # Monday, 11:00
      # Project to create issue in. Format: # namespace/project
      project: example-group/example-project
      # Optional:
      #   If specified, summarised are open issues in the given iteration.
      #   If unspecified, summarised are all open issues in projects that the bot can access.
      #
      # Variables:
      #   - today_minus_7_days (example: 2025-01-02)
      #   - today_plus_7_days (example: 2025-01-08)
      #   - today (example: 2025-01-14)
      # Note: these variables don't add or subtract the given amount of days
      # (e.g. 7 days) to/from today, but equal a total of 7 days (including
      # today). This matches GitLab iterations, which span exactly 7 days
      # (e.g. days 20 from start - 26 to finish).
      #
      iteration_date_range: '{today_minus_7_days}/{today}'
      # Additional issue contents (added to top)
      description: Check stuff, do stuff, ...
```

### NOP

An automation that does nothing, for testing purposes.

```yaml
automations:
  nop:
    - name: Do nothing
      schedule: 5 13 3 * *
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
