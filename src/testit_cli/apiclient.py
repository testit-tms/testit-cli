"""The module provides functionality for working with TMS"""
import logging
import os
import typing

from testit_api_client import ApiClient as TmsClient
from testit_api_client import Configuration
from testit_api_client.apis import AttachmentsApi, AutoTestsApi, TestRunsApi, TestResultsApi, ProjectsApi, WorkflowsApi
from testit_api_client.models import (
    ApiV2AutoTestsSearchPostRequest,
    ApiV2TestResultsSearchPostRequest,
    AttachmentModel,
    AttachmentPutModel,
    AutoTestModel,
    AutoTestResultsForTestRunModel,
    CreateAutoTestRequest,
    TestRunV2ApiResult,
    UpdateAutoTestRequest,
    UpdateEmptyRequest,
    TestResultShortResponse,
    CreateEmptyRequest,
    AutoTestApiResult,
    ProjectModel,
    WorkflowApiResult,
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

    def __get_project(self, project_id: str) -> ProjectModel:
        """Function returns ProjectModel."""
        return self.__projects_api.get_project_by_id(id=project_id)

    def __get_workflow_by_id(self, workflow_id: str) -> WorkflowApiResult:
        """Function returns WorkflowApiResult."""
        return self.__workflows_api.api_v2_workflows_id_get(id=workflow_id)

    def get_status_codes(self, project_id: str) -> typing.List[str]:
        """Function returns list of statuses from project."""
        project: ProjectModel = self.__get_project(project_id)
        workflow: WorkflowApiResult = self.__get_workflow_by_id(project.workflow_id)

        return [status.code for status in workflow.statuses]
