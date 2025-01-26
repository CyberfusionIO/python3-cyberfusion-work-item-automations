from cyberfusion.WorkItemAutomations.automations.nop import (
    NOPAutomation,
)
from tests.factories import NOPAutomationConfigFactory

from faker import Faker

faker = Faker()


def test_nop():
    automation_config = NOPAutomationConfigFactory.build()

    automation = NOPAutomation(automation_config)

    automation.execute()
