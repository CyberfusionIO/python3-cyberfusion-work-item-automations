import pytest
from dataclasses import asdict
from tests.factories import NOPAutomationConfigFactory
from tests.helpers import create_config

from faker import Faker

faker = Faker()


def test_duplicate_name() -> None:
    NAME = faker.word()

    config = create_config(
        {
            "nop": [
                asdict(NOPAutomationConfigFactory.build(name=NAME)),
                asdict(NOPAutomationConfigFactory.build(name=NAME)),
            ]
        },
    )

    with pytest.raises(ValueError, match=f"^Duplicate automation name: {NAME}$"):
        config.automations
