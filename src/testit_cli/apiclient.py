"""The module provides functionality for working with TMS"""
import logging
import os
import typing

from testit_api_client import ApiClient as TmsClient
from testit_api_client import Configuration
from testit_api_client.apis import AttachmentsApi, AutoTestsApi, TestRunsApi, TestResultsApi, ProjectsApi, WorkflowsApi
from testit_api_client.model.api_v2_auto_tests_search_post_request import ApiV2AutoTestsSearchPostRequest
from testit_api_client.model.api_v2_test_results_search_post_request import ApiV2TestResultsSearchPostRequest
from testit_api_client.model.api_v2_test_runs_id_reruns_post_request import ApiV2TestRunsIdRerunsPostRequest
from testit_api_client.model.attachment_model import AttachmentModel
from testit_api_client.model.attachment_put_model import AttachmentPutModel
from testit_api_client.model.auto_test_model import AutoTestModel
from testit_api_client.model.auto_test_results_for_test_run_model import AutoTestResultsForTestRunModel
from testit_api_client.model.create_auto_test_request import CreateAutoTestRequest
from testit_api_client.model.manual_rerun_api_result import ManualRerunApiResult
from testit_api_client.model.manual_rerun_select_test_results_api_model_extraction_model import ManualRerunSelectTestResultsApiModelExtractionModel
from testit_api_client.model.manual_rerun_select_test_results_api_model_filter import ManualRerunSelectTestResultsApiModelFilter
from testit_api_client.model.test_run_v2_api_result import TestRunV2ApiResult
from testit_api_client.model.update_auto_test_request import UpdateAutoTestRequest
from testit_api_client.model.update_empty_request import UpdateEmptyRequest
from testit_api_client.models import (
    TestResultShortResponse,
    CreateEmptyRequest,
    AutoTestApiResult,
    CreateProjectRequest
)

from .converter import Converter
from .models.testrun import TestRun
from .html_escape_utils import HtmlEscapeUtils


class ApiClient:
    """Class representing an api client"""

    def __init__(self, url: str, token: str, disable_cert_validation: bool):
        client_config = Configuration(host=url)
        client_config.verify_ssl = not disable_cert_validation

        client = TmsClient(
            configuration=client_config,
            header_name="Authorization",
            header_value="PrivateToken " + token,
        )

        self.__test_run_api = TestRunsApi(api_client=client)
        self.__autotest_api = AutoTestsApi(api_client=client)
        self.__attachments_api = AttachmentsApi(api_client=client)
        self.__test_results_api = TestResultsApi(api_client=client)
        self.__projects_api = ProjectsApi(api_client=client)
        self.__workflows_api = WorkflowsApi(api_client=client)

    def create_test_run(self, project_id: str, name: str) -> TestRun:
        """Function creates test run and returns test run id."""
        model = CreateEmptyRequest(project_id=project_id, name=name)
        model = HtmlEscapeUtils.escape_html_in_object(model)
        logging.debug(f"Creating test run with model: {model}")

        test_run: TestRunV2ApiResult = self.__test_run_api.create_empty(create_empty_request=model)

        logging.info(f'Created new testrun (ID: {test_run.id})')
        logging.debug(f"Test run created: {test_run}")

        return Converter.test_run_v2_get_model_to_test_run(test_run)

    def rerun_test_run(self, test_run_id: str,
                       configuration_ids: list[str] = None,
                       status_codes: list[str] = None,
                       failure_categories: list[str] = None,
                       namespace: str = None,
                       class_name: str = None,
                       auto_test_global_ids: list[int] = None,
                       auto_test_tags: list[str] = None,
                       exclude_auto_test_tags: list[str] = None,
                       auto_test_name: str = None,
                       test_result_ids: list[str] = None,
                       webhook_ids: list[str] = None) -> None:
        """Function reruns test run and returns manual rerun result."""
        filter_model = ManualRerunSelectTestResultsApiModelFilter(
            configuration_ids=configuration_ids,
            status_codes=status_codes,
            failure_categories=failure_categories,
            namespace=namespace,
            class_name=class_name,
            auto_test_global_ids=auto_test_global_ids,
            auto_test_tags=auto_test_tags,
            exclude_auto_test_tags=exclude_auto_test_tags,
            name=auto_test_name
        ) if any(param is not None for param in [
            configuration_ids, status_codes, failure_categories,
            namespace, class_name, auto_test_global_ids, auto_test_tags,
            exclude_auto_test_tags, auto_test_name
        ]) else None

        extraction_model = ManualRerunSelectTestResultsApiModelExtractionModel(
            test_result_ids=test_result_ids
        ) if test_result_ids is not None else None

        model = ApiV2TestRunsIdRerunsPostRequest(
            filter=filter_model,
            extraction_model=extraction_model,
            webhook_ids=webhook_ids
        )

        logging.debug(f"Rerunning test run {test_run_id} with model: {model}")

        result: ManualRerunApiResult = self.__test_run_api.api_v2_test_runs_id_reruns_post(
            id=test_run_id,
            api_v2_test_runs_id_reruns_post_request=model
        )

        logging.info(f'Reran testrun (ID: {test_run_id})\nTest results count: {result.test_results_count}')
        logging.debug(f"Test run rerun result: {result}")

    def update_test_run(self, test_run: TestRun) -> None:
        """Function updates test run."""
        model: UpdateEmptyRequest = Converter.test_run_to_update_empty_request(test_run)
        model = HtmlEscapeUtils.escape_html_in_object(model)
        logging.debug(f"Updating test run with model: {model}")

        # UpdateEmptyRequest
        self.__test_run_api.update_empty(update_empty_request=model)

        logging.info(f'Updated testrun (ID: {test_run.id})')

    def complete_test_run(self, test_run_id: str) -> None:
        """Function completes test run."""
        logging.debug(f"Completing test run {test_run_id}")

        test_run = self.get_test_run(test_run_id)
        if test_run is not None and test_run.state != "Completed":
            self.__test_run_api.complete_test_run(test_run_id)

        logging.info(f"Completed testrun (ID: {test_run_id})")

    def get_test_run(self, test_run_id: str) -> TestRun:
        """Function gets test run and returns test run."""
        logging.debug(f"Getting test run {test_run_id}")

        test_run: TestRunV2ApiResult = self.__test_run_api.get_test_run_by_id(test_run_id)
        if test_run is not None:
            logging.debug(f"Got testrun (ID: {test_run_id})")
            return Converter.test_run_v2_get_model_to_test_run(test_run)

        logging.error(f"Test run {test_run_id} not found!")
        raise Exception(f"Test run {test_run_id} not found!")

    def get_autotests(self, model: ApiV2AutoTestsSearchPostRequest) \
            -> list[AutoTestApiResult]:
        """Function returns list of AutoTestApiResult."""
        logging.debug(f"Getting autotests: {model}")

        autotests: list[AutoTestApiResult] = (self.__autotest_api.api_v2_auto_tests_search_post
                                              (api_v2_auto_tests_search_post_request=model))

        logging.debug(f"Got autotests: {autotests}")

        return autotests

    def create_autotest(self, model: CreateAutoTestRequest) -> str:
        """Function creates autotest and returns autotest id."""
        model = HtmlEscapeUtils.escape_html_in_object(model)

        logging.debug(f"Creating autotest {model}")

        response: AutoTestModel = self.__autotest_api.create_auto_test(create_auto_test_request=model)

        logging.debug(f"Created autotest {response}")

        return str(response.id)

    def update_autotest(self, model: UpdateAutoTestRequest) -> None:
        """Function updates autotest"""
        try:
            escaped_model: UpdateAutoTestRequest = HtmlEscapeUtils.escape_html_in_object(model)

            logging.debug(f"Updating autotest {escaped_model}")

            # UpdateAutoTestRequest
            self.__autotest_api.update_auto_test(update_auto_test_request=escaped_model)

            logging.debug(f'Updated "{model.name}" successfully!')
        except Exception as exc:
            logging.error(f'Updated "{model.name}" status: {exc}')

    def send_test_result(
            self, testrun_id: str, model: AutoTestResultsForTestRunModel
    ) -> None:
        """Function sends autotest result to test run"""
        try:
            escaped_model: AutoTestResultsForTestRunModel = HtmlEscapeUtils.escape_html_in_object(model)

            logging.debug(f"Adding autotest results to testrun {testrun_id}: {escaped_model}")

            self.__test_run_api.set_auto_test_results_for_test_run(
                id=testrun_id, auto_test_results_for_test_run_model=[escaped_model]
            )
            logging.debug(
                f"Added autotest results to testrun {testrun_id} successfully"
            )
        except Exception as exc:
            logging.error(f"Set result status: {exc}")

    def upload_attachments(self, attachments: typing.List[str]) -> typing.List[AttachmentPutModel]:
        """Function upload attachments and returns list of AttachmentPutModel."""
        attachment_ids = []

        for attachment in attachments:
            if os.path.isfile(attachment):
                with open(attachment, "rb+") as file:
                    try:
                        attachment_response: AttachmentModel = self.__attachments_api.api_v2_attachments_post(
                            # file_type
                            file=file)

                        attachment_ids.append(AttachmentPutModel(id=attachment_response.id))

                        logging.debug(f'Attachment "{attachment}" was uploaded')
                    except Exception as exc:
                        logging.error(f'Upload attachment "{attachment}" status: {exc}')
            else:
                logging.error(f'File "{attachment}" was not found!')

        return attachment_ids

    def get_test_results(
            self,
            model: ApiV2TestResultsSearchPostRequest
    ) -> list[TestResultShortResponse]:
        """Function returns list of TestResultShortGetModel."""
        logging.debug(f"Getting test results: {model}")

        test_results: list[TestResultShortResponse] = self.__test_results_api.api_v2_test_results_search_post(
            api_v2_test_results_search_post_request=model)

        logging.debug(f"Got test results: {test_results}")

        return test_results

    def create_project(self, name: str, description: str = None, is_favorite: bool = None, workflow_id: str = None) -> str:
        """Function creates project and returns project id."""
        model = CreateProjectRequest(name=name, description=description, is_favorite=is_favorite, workflow_id=workflow_id)
        model = HtmlEscapeUtils.escape_html_in_object(model)
        logging.debug(f"Creating project with model: {model}")

        project = self.__projects_api.create_project(create_project_request=model)

        logging.info(f'Created new project (ID: {project.id})')
        logging.debug(f"Project created: {project}")

        return str(project.id)
