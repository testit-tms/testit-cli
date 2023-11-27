import typing

from testit_api_client.models import (
    AutotestsSelectModelFilter,
    AutotestsSelectModelIncludes,
    AutoTestResultsForTestRunModel,
    ApiV2AutoTestsSearchPostRequest,
    AttachmentModel,
    AttachmentPutModel,
    CreateAutoTestRequest,
    LinkModel,
    LinkPutModel,
    TestRunV2GetModel,
    UpdateAutoTestRequest,
    UpdateEmptyRequest
)

from .models.testrun import TestRun


class Converter:
    @staticmethod
    def project_id_and_external_id_to_autotests_search_post_request(project_id: str, external_id: str):
        autotests_filter = AutotestsSelectModelFilter(
            project_ids=[project_id],
            external_ids=[external_id],
            is_deleted=False)
        autotests_includes = AutotestsSelectModelIncludes(
            include_steps=False,
            include_links=False,
            include_labels=False)

        return ApiV2AutoTestsSearchPostRequest(filter=autotests_filter, includes=autotests_includes)

    @staticmethod
    def test_result_to_create_autotest_request(result, external_id: str, project_id: str):
        return CreateAutoTestRequest(
            external_id=external_id,
            project_id=project_id,
            name=result.get_name(),
            namespace=result.get_name_space(),
            classname=result.get_class_name(),
        )

    @staticmethod
    def test_result_to_update_autotest_request(result, external_id: str, project_id: str):
        return UpdateAutoTestRequest(
            external_id=external_id,
            project_id=project_id,
            name=result.get_name(),
            namespace=result.get_name_space(),
            classname=result.get_class_name(),
            is_flaky=result.get_is_flaky()
        )

    @staticmethod
    def test_result_to_testrun_result_post_model(
        result, external_id: str, configuration_id: str
    ):
        return AutoTestResultsForTestRunModel(
            configuration_id,
            external_id,
            result.get_status(),
            traces=result.get_trace(),
            duration=round(result.get_duration()),
            message=result.get_message(),
        )

    @classmethod
    def test_run_v2_get_model_to_test_run(cls, test_run_model: TestRunV2GetModel) -> TestRun:
        return TestRun(
            id=test_run_model["id"],
            project_id=test_run_model["project_id"],
            state=test_run_model["state_name"].value,
            name=test_run_model["name"],
            description=test_run_model["description"],
            launch_source=test_run_model["launch_source"],
            attachments=cls.attachment_models_to_attachment_put_models(test_run_model["attachments"]),
            links=cls.link_models_to_link_put_models(test_run_model["links"])
        )

    @classmethod
    def attachment_models_to_attachment_put_models(
            cls,
            attachment_models: typing.List[AttachmentModel]) -> typing.List[AttachmentPutModel]:
        attachment_put_models = []

        for attachment_model in attachment_models:
            attachment_put_models.append(
                cls.attachment_model_to_attachment_put_model(attachment_model))

        return attachment_put_models

    @staticmethod
    def attachment_model_to_attachment_put_model(attachment_model: AttachmentModel) -> AttachmentPutModel:
        return AttachmentPutModel(id=attachment_model.id)

    @classmethod
    def link_models_to_link_put_models(
            cls,
            link_models: typing.List[LinkModel]) -> typing.List[LinkPutModel]:
        link_put_models = []

        for link_model in link_models:
            link_put_models.append(
                cls.link_model_to_link_put_model(link_model))

        return link_put_models

    @staticmethod
    def link_model_to_link_put_model(link_model: LinkModel) -> LinkPutModel:
        return LinkPutModel(
            url=link_model.url,
            id=link_model.id,
            title=link_model.title,
            description=link_model.description,
            type=link_model.type,
            has_info=link_model.has_info
        )

    @staticmethod
    def test_run_to_update_empty_request(test_run: TestRun) -> UpdateEmptyRequest:
        return UpdateEmptyRequest(
            id=test_run.id,
            name=test_run.name,
            description=test_run.description,
            launch_source=test_run.launch_source,
            attachments=test_run.attachments,
            links=test_run.links
        )
