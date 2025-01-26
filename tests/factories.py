import factory

from cyberfusion.WorkItemAutomations.config import (
    CreateIssueAutomationConfig,
    NOPAutomationConfig,
)


class BaseAutomationConfigFactory(factory.Factory):
    class Meta:
        abstract = True

    class Params:
        private_token_suffix = factory.Faker("pystr", min_chars=20, max_chars=20)
        url_with_trailing_slash = factory.Faker(
            "url",
        )

    name = factory.Faker(
        "sentence",
    )
    schedule = "* * * * *"
    url = factory.LazyAttribute(
        lambda obj: obj.url_with_trailing_slash[:-1]
    )  # Remove trailing slash; not natively supported
    private_token = factory.LazyAttribute(
        lambda obj: f"glpat-{obj.private_token_suffix}"
    )


class CreateIssueAutomationConfigFactory(BaseAutomationConfigFactory):
    class Meta:
        model = CreateIssueAutomationConfig

    class Params:
        namespace = factory.Faker(
            "word",
        )
        project_name = factory.Faker(
            "word",
        )

    project = factory.LazyAttribute(lambda obj: f"{obj.namespace}/{obj.project_name}")
    title = factory.Faker(
        "sentence",
    )
    assignee_group = factory.Faker(
        "word",
    )
    description = factory.Faker(
        "sentence",
    )


class NOPAutomationConfigFactory(BaseAutomationConfigFactory):
    class Meta:
        model = NOPAutomationConfig
