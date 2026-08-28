import typing

from adapters_api.model.adapters_auto_tests_post_request import AdaptersAutoTestsPostRequest
from adapters_api.model.adapters_auto_tests_put_request import AdaptersAutoTestsPutRequest
from adapters_api.model.adapters_auto_tests_search_post_request import AdaptersAutoTestsSearchPostRequest
from adapters_api.model.adapters_test_results_search_post_request import AdaptersTestResultsSearchPostRequest
from adapters_api.model.adapters_test_runs_put_request import AdaptersTestRunsPutRequest
from adapters_api.model.assign_attachment_api_model import AssignAttachmentApiModel
from adapters_api.model.attachment_api_result import AttachmentApiResult
from adapters_api.model.attachment_put_model import AttachmentPutModel
from adapters_api.model.auto_test_api_result import AutoTestApiResult
from adapters_api.model.auto_test_create_api_model_layer import AutoTestCreateApiModelLayer
from adapters_api.model.auto_test_results_for_test_run_model import AutoTestResultsForTestRunModel
from adapters_api.model.auto_test_search_api_model_filter import AutoTestSearchApiModelFilter
from adapters_api.model.auto_test_search_api_model_includes import AutoTestSearchApiModelIncludes
from adapters_api.model.layer_source import LayerSource
from adapters_api.model.link_api_result import LinkApiResult
from adapters_api.model.test_result_short_response import TestResultShortResponse
from adapters_api.model.test_run_api_result import TestRunApiResult
from adapters_api.model.test_status_api_type import TestStatusApiType
from adapters_api.model.test_status_type import TestStatusType
from adapters_api.model.update_link_api_model import UpdateLinkApiModel
from .models.testcase import TestCase
from .models.testrun import TestRun


class Converter:
    @staticmethod
    def layer_to_api_model(layer_name: typing.Optional[str]) -> typing.Optional[AutoTestCreateApiModelLayer]:
        if layer_name is None or not str(layer_name).strip():
            return None
        return AutoTestCreateApiModelLayer(
            name=str(layer_name).strip(),
            source=LayerSource("Run"),
        )

    @staticmethod
    def project_id_and_external_id_to_autotests_search_post_request(
            project_id: str, external_id: str) -> AdaptersAutoTestsSearchPostRequest:
        autotests_filter = AutoTestSearchApiModelFilter(
            project_ids=[project_id],
            external_ids=[external_id],
            is_deleted=False)
        autotests_includes = AutoTestSearchApiModelIncludes(
            include_steps=False,
            include_links=False,
            include_labels=False)

        return AdaptersAutoTestsSearchPostRequest(filter=autotests_filter, includes=autotests_includes)

    @staticmethod
    def external_ids_to_autotests_search_post_request(
            external_ids: typing.List[str]) -> AdaptersAutoTestsSearchPostRequest:
        autotests_filter = AutoTestSearchApiModelFilter(
            external_ids=external_ids,
            is_deleted=False)
        autotests_includes = AutoTestSearchApiModelIncludes(
            include_steps=False,
            include_links=False,
            include_labels=False)

        return AdaptersAutoTestsSearchPostRequest(filter=autotests_filter, includes=autotests_includes)

    @staticmethod
    def testrun_id_and_configuration_id_and_in_progress_outcome_to_test_results_search_post_request(
            testrun_id: str,
            configuration_id: str) -> AdaptersTestResultsSearchPostRequest:
        return AdaptersTestResultsSearchPostRequest(
            test_run_ids=[testrun_id],
            configuration_ids=[configuration_id],
            status_types=[TestStatusApiType("InProgress")])

    @staticmethod
    def test_result_short_models_to_autotest_external_ids(
            test_results: typing.List[TestResultShortResponse]) -> typing.List[str]:
        return [
            test_result.autotest_external_id
            for test_result in test_results
            if test_result.autotest_external_id
        ]

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
            result: TestCase,
            external_id: str,
            project_id: str,
            layer: typing.Optional[str] = None) -> AdaptersAutoTestsPostRequest:
        request_kwargs = {
            "external_id": external_id,
            "project_id": project_id,
            "name": result.get_name(),
            "namespace": result.get_name_space(),
            "classname": result.get_class_name(),
        }
        api_layer = Converter.layer_to_api_model(layer)
        if api_layer is not None:
            request_kwargs["layer"] = api_layer
        return AdaptersAutoTestsPostRequest(**request_kwargs)

    @staticmethod
    def test_result_to_update_autotest_request(
            result: TestCase,
            external_id: str,
            project_id: str,
            layer: typing.Optional[str] = None) -> AdaptersAutoTestsPutRequest:
        request_kwargs = {
            "external_id": external_id,
            "project_id": project_id,
            "name": result.get_name(),
            "namespace": result.get_name_space(),
            "classname": result.get_class_name(),
            "is_flaky": result.get_is_flaky(),
            "reset_layer": False,
        }
        api_layer = Converter.layer_to_api_model(layer)
        if api_layer is not None:
            request_kwargs["layer"] = api_layer
        return AdaptersAutoTestsPutRequest(**request_kwargs)

    @staticmethod
    def test_result_to_testrun_result_post_model(
        result: TestCase, external_id: str, configuration_id: str, status_codes: typing.List[str]
    ) -> AutoTestResultsForTestRunModel:
        model = AutoTestResultsForTestRunModel(
            configuration_id=configuration_id,
            auto_test_external_id=external_id,
            status_type=TestStatusType(result.get_status_type().value),
            traces=result.get_trace(),
            duration=round(result.get_duration()),
            message=result.get_message(),
        )

        if result.get_status().upper() in status_codes:
            model.status_code = result.get_status()

        return model

    @classmethod
    def test_run_api_result_to_test_run(cls, test_run_model: TestRunApiResult) -> TestRun:
        state = test_run_model.state_name
        state_value = getattr(state, "value", None) or str(state)
        return TestRun(
            id=test_run_model.id,
            project_id=test_run_model.project_id,
            state=state_value,
            name=test_run_model.name,
            description=test_run_model.description or "",
            launch_source=test_run_model.launch_source or "",
            attachments=cls.attachment_models_to_attachment_put_models(test_run_model.attachments),
            links=cls.link_models_to_update_link_models(test_run_model.links),
            tags=list(test_run_model.tags) if test_run_model.tags else [],
        )

    @classmethod
    def attachment_models_to_attachment_put_models(
            cls,
            attachment_models: typing.List[AttachmentApiResult]) -> typing.List[AssignAttachmentApiModel]:
        attachment_put_models = []

        for attachment_model in attachment_models or []:
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
    def attachment_put_models_to_assign_attachments(
            attachment_models: typing.List[AttachmentPutModel]) -> typing.List[AssignAttachmentApiModel]:
        return list(map(lambda x: Converter.attachment_put_model_to_assign_attachment(x), attachment_models))

    @classmethod
    def link_models_to_update_link_models(
            cls,
            link_models: typing.List[LinkApiResult]) -> typing.List[UpdateLinkApiModel]:
        link_put_models = []

        for link_model in link_models or []:
            link_put_models.append(
                cls.link_model_to_update_link_model(link_model))

        return link_put_models

    @staticmethod
    def link_model_to_update_link_model(link_model: LinkApiResult) -> UpdateLinkApiModel:
        return UpdateLinkApiModel(
            url=link_model.url,
            id=link_model.id,
            title=link_model.title,
            description=link_model.description,
            type=link_model.type,
        )

    @staticmethod
    def test_run_to_update_request(test_run: TestRun) -> AdaptersTestRunsPutRequest:
        return AdaptersTestRunsPutRequest(
            id=test_run.id,
            name=test_run.name,
            description=test_run.description,
            launch_source=test_run.launch_source,
            attachments=test_run.attachments,
            links=test_run.links,
            tags=test_run.tags,
        )
