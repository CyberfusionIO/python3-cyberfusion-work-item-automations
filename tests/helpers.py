from cyberfusion.Common import get_tmp_file

import yaml

from cyberfusion.WorkItemAutomations.config import Config
from faker import Faker

faker = Faker()


def create_config(automations: dict) -> Config:
    path = get_tmp_file()

    first_automation = list(automations.values())[0][0]

    data = {
        "url": first_automation["url"],
        "private_token": first_automation["private_token"],
        "automations": automations,
    }

    with open(path, "w") as f:
        yaml.dump(data, f)

    return Config(path)
