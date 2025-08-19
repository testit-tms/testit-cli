import typing

from testit_api_client.model.api_v2_auto_tests_search_post_request import ApiV2AutoTestsSearchPostRequest
from testit_api_client.model.api_v2_test_results_search_post_request import ApiV2TestResultsSearchPostRequest
from testit_api_client.model.attachment_api_result import AttachmentApiResult
from testit_api_client.model.auto_test_api_result import AutoTestApiResult
from testit_api_client.model.auto_test_search_api_model_filter import AutoTestSearchApiModelFilter
from testit_api_client.model.auto_test_search_api_model_includes import AutoTestSearchApiModelIncludes
from testit_api_client.model.create_auto_test_request import CreateAutoTestRequest
from testit_api_client.model.link_api_result import LinkApiResult
from testit_api_client.model.test_run_v2_api_result import TestRunV2ApiResult
from testit_api_client.model.update_auto_test_request import UpdateAutoTestRequest
from testit_api_client.model.update_empty_request import UpdateEmptyRequest
from testit_api_client.models import (
    AutoTestResultsForTestRunModel,
    AttachmentPutModel,
    LinkPutModel,
    TestResultOutcome,
    TestResultShortResponse,
)
from testit_api_client.model.assign_attachment_api_model import AssignAttachmentApiModel

from .models.testcase import TestCase
from .models.testrun import TestRun


class Converter:
    @staticmethod
    def project_id_and_external_id_to_autotests_search_post_request(
            project_id: str, external_id: str) -> ApiV2AutoTestsSearchPostRequest:
        autotests_filter = AutoTestSearchApiModelFilter(
            project_ids=[project_id],
            external_ids=[external_id],
            is_deleted=False)
        autotests_includes = AutoTestSearchApiModelIncludes(
            include_steps=False,
            include_links=False,
            include_labels=False)

        return ApiV2AutoTestsSearchPostRequest(filter=autotests_filter, includes=autotests_includes)

    @staticmethod
    def autotest_ids_to_autotests_search_post_request(
            autotest_ids: typing.List[int]) -> ApiV2AutoTestsSearchPostRequest:
        autotests_filter = AutoTestSearchApiModelFilter(
            global_ids=autotest_ids)
        autotests_includes = AutoTestSearchApiModelIncludes(
            include_steps=False,
            include_links=False,
            include_labels=False)

        return ApiV2AutoTestsSearchPostRequest(filter=autotests_filter, includes=autotests_includes)

    @staticmethod
    def testrun_id_and_configuration_id_and_in_progress_outcome_to_test_results_search_post_request(
            testrun_id: str,
            configuration_id: str) -> ApiV2TestResultsSearchPostRequest:
        return ApiV2TestResultsSearchPostRequest(
            test_run_ids=[testrun_id],
            configuration_ids=[configuration_id],
            outcomes=[TestResultOutcome("InProgress")])

    @staticmethod
    def test_result_short_get_models_to_autotest_ids(
            test_results: typing.List[TestResultShortResponse]) -> typing.List[int]:
        autotest_ids = []

        for test_result in test_results:
            autotest_ids.append(test_result.autotest_global_id)

        return autotest_ids

    @staticmethod
    def autotest_models_to_external_keys(
            autotests: typing.List[AutoTestApiResult]) -> typing.List[str]:
        external_keys = []

        for autotest in autotests:
            external_key = autotest.external_key

            if external_key is None:
                continue

            external_keys.append(external_key)

        return external_keys

    @staticmethod
    def test_result_to_create_autotest_request(
            result: TestCase, external_id: str, project_id: str) -> CreateAutoTestRequest:
        return CreateAutoTestRequest(
            external_id=external_id,
            project_id=project_id,
            name=result.get_name(),
            namespace=result.get_name_space(),
            classname=result.get_class_name(),
        )

    @staticmethod
    def test_result_to_update_autotest_request(
            result: TestCase, external_id: str, project_id: str) -> UpdateAutoTestRequest:
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
        result: TestCase, external_id: str, configuration_id: str
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
    def test_run_v2_get_model_to_test_run(cls, test_run_model: TestRunV2ApiResult) -> TestRun:
        return TestRun(
            id=test_run_model.id,
            project_id=test_run_model.project_id,
            state=test_run_model.state_name.value,
            name=test_run_model.name,
            description=test_run_model.description,
            launch_source=test_run_model.launch_source,
            attachments=cls.attachment_models_to_attachment_put_models(test_run_model.attachments),
            links=cls.link_models_to_link_put_models(test_run_model.links)
        )

    @classmethod
    def attachment_models_to_attachment_put_models(
            cls,
            attachment_models: typing.List[AttachmentApiResult]) -> typing.List[AssignAttachmentApiModel]:
        attachment_put_models = []

        for attachment_model in attachment_models:
            attachment_put_models.append(
                cls.attachment_model_to_attachment_put_model(attachment_model))

        return attachment_put_models

    @staticmethod
    def attachment_model_to_attachment_put_model(attachment_model: AttachmentApiResult) -> AssignAttachmentApiModel:
        return AssignAttachmentApiModel(id=attachment_model.id)

    @staticmethod
    def attachment_put_model_to_assign_attachment(attachment_model: AttachmentPutModel) -> AssignAttachmentApiModel:
        return AssignAttachmentApiModel(id=attachment_model.id)

    @staticmethod
    def attachment_put_models_to_assign_attachments(attachment_models: list[AttachmentPutModel])\
            -> list[AssignAttachmentApiModel]:
        return list(map(lambda x: Converter.attachment_put_model_to_assign_attachment(x), attachment_models))

    @classmethod
    def link_models_to_link_put_models(
            cls,
            link_models: typing.List[LinkApiResult]) -> typing.List[LinkPutModel]:
        link_put_models = []

        for link_model in link_models:
            link_put_models.append(
                cls.link_model_to_link_put_model(link_model))

        return link_put_models

    @staticmethod
    def link_model_to_link_put_model(link_model: LinkApiResult) -> LinkPutModel:
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
            # str
            id=test_run.id,
            # str
            name=test_run.name,
            # str
            description=test_run.description,
            launch_source=test_run.launch_source,
            attachments=test_run.attachments,
            links=test_run.links
        )
