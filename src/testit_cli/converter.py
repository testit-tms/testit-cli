import typing

from testit_api_client import AutoTestSearchApiModel, AutoTestFilterApiModel, AutoTestSearchIncludeApiModel, \
    TestResultsFilterApiModel, TestRunV2ApiResult, AttachmentApiResult, LinkApiResult, UpdateEmptyTestRunApiModel, \
    AssignAttachmentApiModel
from testit_api_client.models import (
    AutoTestResultsForTestRunModel,
    AttachmentModel,
    AttachmentPutModel,
    AutoTestPostModel,
    AutoTestPutModel,
    LinkModel,
    LinkPutModel,
    TestResultOutcome,
    TestResultShortResponse,
    AutoTestModel
)

from .models.testrun import TestRun


class Converter:
    @staticmethod
    def project_id_and_external_id_to_autotests_search_post_request(project_id: str, external_id: str) \
            -> AutoTestSearchApiModel:
        autotests_filter = AutoTestFilterApiModel(
            project_ids=[project_id],
            external_ids=[external_id],
            is_deleted=False)
        autotests_includes = AutoTestSearchIncludeApiModel(
            include_steps=False,
            include_links=False,
            include_labels=False)

        return AutoTestSearchApiModel(filter=autotests_filter, includes=autotests_includes)

    @staticmethod
    def autotest_ids_to_autotests_search_post_request(autotest_ids: typing.List[int]) \
            -> AutoTestSearchApiModel:
        autotests_filter = AutoTestFilterApiModel(
            global_ids=autotest_ids)
        autotests_includes = AutoTestSearchIncludeApiModel(
            include_steps=False,
            include_links=False,
            include_labels=False)

        return AutoTestSearchApiModel(filter=autotests_filter, includes=autotests_includes)

    @staticmethod
    def testrun_id_and_configuration_id_and_in_progress_outcome_to_test_results_search_post_request(
            testrun_id: str,
            configuration_id: str) -> TestResultsFilterApiModel:
        return TestResultsFilterApiModel(
            test_run_ids=[testrun_id],
            configuration_ids=[configuration_id],
            outcomes=[TestResultOutcome("InProgress")])

    @staticmethod
    def test_result_short_get_models_to_autotest_ids(test_results: typing.List[TestResultShortResponse]) \
            -> list[int]:
        autotest_ids = []

        for test_result in test_results:
            autotest_ids.append(test_result.autotest_global_id)

        return autotest_ids

    @staticmethod
    def autotest_models_to_external_keys(autotests: typing.List[AutoTestModel]) \
            -> list[str]:
        external_keys = []

        for autotest in autotests:
            external_key = autotest.external_key

            if external_key is None:
                continue

            external_keys.append(external_key)

        return external_keys

    @staticmethod
    def test_result_to_create_autotest_request(result, external_id: str, project_id: str) \
            -> AutoTestPostModel:
        return AutoTestPostModel(
            external_id=external_id,
            project_id=project_id,
            name=result.get_name(),
            namespace=result.get_name_space(),
            classname=result.get_class_name(),
        )

    @staticmethod
    def test_result_to_update_autotest_request(result, external_id: str, project_id: str) \
            -> AutoTestPutModel:
        return AutoTestPutModel(
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
    ) -> AutoTestResultsForTestRunModel:
        return AutoTestResultsForTestRunModel(
            configuration_id=configuration_id,
            auto_test_external_id=external_id,
            outcome=result.get_status(),
            traces=result.get_trace(),
            duration=round(result.get_duration()),
            message=result.get_message(),
        )

    @classmethod
    def test_run_v2_get_result_to_test_run(cls, test_run_result: TestRunV2ApiResult) -> TestRun:
        return TestRun(
            id=test_run_result.id,
            project_id=test_run_result.project_id,
            state=test_run_result.state_name.value,
            name=test_run_result.name,
            description=test_run_result.description,
            launch_source=test_run_result.launch_source,
            attachments=cls.attachment_results_to_attachment_put_models(test_run_result.attachments),
            links=cls.link_results_to_link_put_models(test_run_result.links)
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

    @classmethod
    def attachment_results_to_attachment_put_models(
            cls,
            attachment_results: typing.List[AttachmentApiResult]) -> typing.List[AttachmentPutModel]:
        attachment_put_models = []

        for attachment_result in attachment_results:
            attachment_put_models.append(
                cls.attachment_result_to_attachment_put_model(attachment_result))

        return attachment_put_models

    @staticmethod
    def attachment_model_to_attachment_put_model(attachment_model: AttachmentModel) -> AttachmentPutModel:
        return AttachmentPutModel(id=attachment_model.id)

    @staticmethod
    def attachment_result_to_attachment_put_model(attachment_result: AttachmentApiResult) -> AttachmentPutModel:
        return AttachmentPutModel(id=attachment_result.id)

    @classmethod
    def link_models_to_link_put_models(
            cls,
            link_models: typing.List[LinkModel]) -> typing.List[LinkPutModel]:
        link_put_models = []

        for link_model in link_models:
            link_put_models.append(
                cls.link_model_to_link_put_model(link_model))

        return link_put_models

    @classmethod
    def link_results_to_link_put_models(
            cls,
            link_results: typing.List[LinkApiResult]) -> typing.List[LinkPutModel]:
        link_put_models = []

        for link_result in link_results:
            link_put_models.append(
                cls.link_result_to_link_put_model(link_result))

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
    def link_result_to_link_put_model(link_result: LinkApiResult) -> LinkPutModel:
        return LinkPutModel(
            url=link_result.url,
            id=link_result.id,
            title=link_result.title,
            description=link_result.description,
            type=link_result.type,
            has_info=link_result.has_info
        )

    @staticmethod
    def test_run_to_update_empty_request(test_run: TestRun) -> UpdateEmptyTestRunApiModel:
        return UpdateEmptyTestRunApiModel(
            id=test_run.id,
            name=test_run.name,
            description=test_run.description,
            launch_source=test_run.launch_source,
            attachments=Converter.test_run_attachments_to(test_run.attachments),
            links=test_run.links
        )

    @staticmethod
    def test_run_attachments_to(attachments: list[AttachmentPutModel]) -> list[AssignAttachmentApiModel]:
        def convert(x: AttachmentPutModel) -> AssignAttachmentApiModel:
            return AssignAttachmentApiModel(id=x.id, model_config=x.model_config)

        return [convert(x) for x in attachments]
