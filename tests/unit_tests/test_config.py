from cyberfusion.Common import get_tmp_file

import yaml
import pytest

from cyberfusion.WorkItemAutomations.config import Config


def test_duplicate_name(example_group_name: str, example_project_name: str) -> None:
    path = get_tmp_file()

    NAME = "example-name"

    data = {
        "url": "https://gitlab.example.com",
        "private_token": "glpat-1aVadca471A281la331L",
        "automations": {
            "create_issue": [
                {
                    "name": NAME,
                    "project": example_group_name + "/" + example_project_name,
                    "title": "Update that",
                    "description": "Do something",
                    "schedule": "5 13 3 * *",
                },
                {
                    "name": NAME,
                    "project": example_group_name + "/" + example_project_name,
                    "title": "Update that",
                    "description": "Do something",
                    "schedule": "5 13 3 * *",
                },
            ]
        },
    }

    with open(path, "w") as f:
        yaml.dump(data, f)

    with pytest.raises(ValueError, match=f"^Duplicate automation name: {NAME}$"):
        Config(path).automations
