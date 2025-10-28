import os

import factory

from cyberfusion.WorkItemAutomations.config import (
    CreateIssueAutomationConfig,
    NOPAutomationConfig,
    SummariseIssuesAutomationConfig,
)


class BaseAutomationConfigFactory(factory.Factory):
    class Meta:
        abstract = True

    class Params:
        private_token_suffix = factory.Faker("pystr", min_chars=20, max_chars=20)
        url_with_trailing_slash = factory.Faker("url")

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
    state_directory_path = factory.Faker("file_path")

    @classmethod
    def _adjust_kwargs(cls, **kwargs: dict) -> dict:
        kwargs["state_directory_path"] = os.path.join(
            os.path.sep,
            "tmp",
            "glwia-tests",
            os.path.relpath(kwargs["state_directory_path"], os.path.sep),
        )

        return kwargs

    @factory.post_generation
    def create_state_directory(
        obj, create: bool, extracted: None, **kwargs: dict
    ) -> None:
        if not create:
            return

        os.makedirs(obj.state_directory_path)


class CreateIssueAutomationConfigFactory(BaseAutomationConfigFactory):
    class Meta:
        model = CreateIssueAutomationConfig

    class Params:
        namespace = factory.Faker("word")
        project_name = factory.Faker("word")

    project = factory.LazyAttribute(lambda obj: f"{obj.namespace}/{obj.project_name}")
    title = factory.Faker("sentence")
    assignee_group = factory.Faker("word")
    description = factory.Faker("sentence")
    template = factory.Faker("sentence")


class SummariseIssuesAutomationConfigFactory(BaseAutomationConfigFactory):
    class Meta:
        model = SummariseIssuesAutomationConfig

    class Params:
        namespace = factory.Faker("word")
        project_name = factory.Faker("word")

    project = factory.LazyAttribute(lambda obj: f"{obj.namespace}/{obj.project_name}")
    iteration_date_range = "{today_minus_7_days}/{today}"
    description = factory.Faker("sentence")


class NOPAutomationConfigFactory(BaseAutomationConfigFactory):
    class Meta:
        model = NOPAutomationConfig
