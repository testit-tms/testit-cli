"""The module provides functionality for working with TMS"""
import logging
import os
import typing

from testit_api_client import ApiClient as TmsClient
from testit_api_client import Configuration as V2Configuration
from testit_api_client.apis import TestRunsApi as V2TestRunsApi
from testit_api_client.models import (
    CreateEmptyRequest,
    TestRunV2ApiResult,
    UpdateEmptyRequest,
)

from adapters_api import ApiClient as AdaptersHttpClient
from adapters_api import Configuration as AdaptersConfiguration
from adapters_api.apis import (
    AttachmentsApi,
    AutoTestsApi,
    ProjectsApi,
    TestResultsApi,
)
from adapters_api.apis import TestRunsApi as AdaptersTestRunsApi
from adapters_api.apis import (
    WorkflowsApi,
)
from adapters_api.models import (
    AdaptersAutoTestsPostRequest,
    AdaptersAutoTestsPutRequest,
    AdaptersAutoTestsSearchPostRequest,
    AdaptersProjectsPostRequest,
    AdaptersTestResultsSearchPostRequest,
    AdaptersTestRunsIdRerunsPostRequest,
    AttachmentModel,
    AttachmentPutModel,
    AutoTestApiResult,
    AutoTestResultsForTestRunModel,
    DetailedProjectApiResult,
    ManualRerunApiResult,
    ManualRerunSelectTestResultsApiModelExtractionModel,
    ManualRerunSelectTestResultsApiModelFilter,
    ManualRerunTestResultApiModelTestResultIds,
    TestResultShortResponse,
    WorkflowApiResult,
)
from .converter import Converter
from .html_escape_utils import HtmlEscapeUtils
from .http_retry import with_http_retries
from .models.testrun import TestRun


class ApiClient:
    """Class representing an api client (hybrid: v2 test-run CRUD + adapters elsewhere)."""

    def __init__(self, url: str, token: str, disable_cert_validation: bool):
        auth_header = "PrivateToken " + token

        v2_config = V2Configuration(host=url)
        v2_config.verify_ssl = not disable_cert_validation
        v2_client = TmsClient(
            configuration=v2_config,
            header_name="Authorization",
            header_value=auth_header,
        )
        self.__v2_test_run_api = V2TestRunsApi(api_client=v2_client)

        adapters_config = AdaptersConfiguration(host=url)
        adapters_config.verify_ssl = not disable_cert_validation
        adapters_client = AdaptersHttpClient(
            configuration=adapters_config,
            header_name="Authorization",
            header_value=auth_header,
        )
        self.__test_run_api = AdaptersTestRunsApi(api_client=adapters_client)
        self.__autotest_api = AutoTestsApi(api_client=adapters_client)
        self.__attachments_api = AttachmentsApi(api_client=adapters_client)
        self.__test_results_api = TestResultsApi(api_client=adapters_client)
        self.__projects_api = ProjectsApi(api_client=adapters_client)
        self.__workflows_api = WorkflowsApi(api_client=adapters_client)

    def create_test_run(
        self,
        project_id: str,
        name: str,
        tags: typing.Optional[typing.List[str]] = None,
        links: typing.Optional[typing.List] = None,
    ) -> TestRun:
        """Function creates test run and returns test run id."""
        create_kwargs = {"project_id": project_id, "name": name}
        if tags:
            create_kwargs["tags"] = tags
        if links:
            create_kwargs["links"] = links
        model = CreateEmptyRequest(**create_kwargs)
        model = HtmlEscapeUtils.escape_html_in_object(model)
        logging.debug(f"Creating test run with model: {model}")

        test_run: TestRunV2ApiResult = with_http_retries(
            lambda: self.__v2_test_run_api.create_empty(create_empty_request=model),
            label="Create test run",
        )

        logging.info(f'Created new testrun (ID: {test_run.id})')
        if tags or links:
            logging.info(
                "Applied tags/links on create for testrun (ID: %s): tags=%s links=%s",
                test_run.id,
                tags,
                links,
            )
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
        if failure_categories:
            logging.warning(
                "failure_categories is not supported by adapters rerun filter and will be ignored"
            )

        filter_model = ManualRerunSelectTestResultsApiModelFilter(
            configuration_ids=configuration_ids,
            status_codes=status_codes,
            namespace=namespace,
            class_name=class_name,
            auto_test_global_ids=auto_test_global_ids,
            auto_test_tags=auto_test_tags,
            exclude_auto_test_tags=exclude_auto_test_tags,
            name=auto_test_name
        ) if any(param is not None for param in [
            configuration_ids, status_codes,
            namespace, class_name, auto_test_global_ids, auto_test_tags,
            exclude_auto_test_tags, auto_test_name
        ]) else None

        extraction_model = ManualRerunSelectTestResultsApiModelExtractionModel(
            test_result_ids=ManualRerunTestResultApiModelTestResultIds(include=test_result_ids)
        ) if test_result_ids is not None else None

        model = AdaptersTestRunsIdRerunsPostRequest(
            filter=filter_model,
            extraction_model=extraction_model,
            webhook_ids=webhook_ids
        )

        logging.debug(f"Rerunning test run {test_run_id} with model: {model}")

        result: ManualRerunApiResult = self.__test_run_api.adapters_test_runs_id_reruns_post(
            id=test_run_id,
            adapters_test_runs_id_reruns_post_request=model
        )

        logging.info(f'Reran testrun (ID: {test_run_id})\nTest results count: {result.test_results_count}')
        logging.debug(f"Test run rerun result: {result}")

    def update_test_run(self, test_run: TestRun) -> None:
        """Function updates test run."""
        model: UpdateEmptyRequest = Converter.test_run_to_update_empty_request(test_run)
        model = HtmlEscapeUtils.escape_html_in_object(model)
        logging.debug(f"Updating test run with model: {model}")

        self.__v2_test_run_api.update_empty(update_empty_request=model)

        logging.info(f'Updated testrun (ID: {test_run.id})')

    def complete_test_run(self, test_run_id: str) -> None:
        """Function completes test run."""
        logging.debug(f"Completing test run {test_run_id}")

        test_run = self.get_test_run(test_run_id)
        if test_run is not None and test_run.state != "Completed":
            self.__test_run_api.adapters_test_runs_id_complete_post(test_run_id)

        logging.info(f"Completed testrun (ID: {test_run_id})")

    def get_test_run(self, test_run_id: str) -> TestRun:
        """Function gets test run and returns test run."""
        logging.debug(f"Getting test run {test_run_id}")

        test_run: TestRunV2ApiResult = self.__v2_test_run_api.get_test_run_by_id(test_run_id)
        if test_run is not None:
            logging.debug(f"Got testrun (ID: {test_run_id})")
            return Converter.test_run_v2_get_model_to_test_run(test_run)

        logging.error(f"Test run {test_run_id} not found!")
        raise Exception(f"Test run {test_run_id} not found!")

    def get_autotests(self, model: AdaptersAutoTestsSearchPostRequest) \
            -> list[AutoTestApiResult]:
        """Function returns list of AutoTestApiResult."""
        logging.debug(f"Getting autotests: {model}")

        autotests: list[AutoTestApiResult] = self.__autotest_api.adapters_auto_tests_search_post(
            adapters_auto_tests_search_post_request=model)

        logging.debug(f"Got autotests: {autotests}")

        return autotests

    def create_autotest(self, model: AdaptersAutoTestsPostRequest) -> str:
        """Function creates autotest and returns autotest id."""
        model = HtmlEscapeUtils.escape_html_in_object(model)

        logging.debug(f"Creating autotest {model}")

        response: AutoTestApiResult = self.__autotest_api.adapters_auto_tests_post(
            adapters_auto_tests_post_request=model)

        logging.debug(f"Created autotest {response}")

        return str(response.id)

    def update_autotest(self, model: AdaptersAutoTestsPutRequest) -> None:
        """Function updates autotest"""
        try:
            escaped_model: AdaptersAutoTestsPutRequest = HtmlEscapeUtils.escape_html_in_object(model)

            logging.debug(f"Updating autotest {escaped_model}")

            self.__autotest_api.adapters_auto_tests_put(
                adapters_auto_tests_put_request=escaped_model)

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

            self.__test_run_api.adapters_test_runs_id_test_results_post(
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
                        attachment_response: AttachmentModel = self.__attachments_api.adapters_attachments_post(
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
            model: AdaptersTestResultsSearchPostRequest
    ) -> list[TestResultShortResponse]:
        """Function returns list of TestResultShortGetModel."""
        logging.debug(f"Getting test results: {model}")

        test_results: list[TestResultShortResponse] = self.__test_results_api.adapters_test_results_search_post(
            adapters_test_results_search_post_request=model)

        logging.debug(f"Got test results: {test_results}")

        return test_results

    def __get_project(self, project_id: str) -> DetailedProjectApiResult:
        """Function returns DetailedProjectApiResult."""
        return self.__projects_api.adapters_projects_id_get(id=project_id)

    def __get_workflow_by_id(self, workflow_id: str) -> WorkflowApiResult:
        """Function returns WorkflowApiResult."""
        return self.__workflows_api.adapters_workflows_id_get(id=workflow_id)

    def get_status_codes(self, project_id: str) -> typing.List[str]:
        """Function returns list of statuses from project."""
        project: DetailedProjectApiResult = self.__get_project(project_id)
        workflow: WorkflowApiResult = self.__get_workflow_by_id(project.workflow_id)

        return [status.code for status in workflow.statuses]

    def create_project(self, name: str, description: str = None, is_favorite: bool = None, workflow_id: str = None) -> str:
        """Function creates project and returns project id."""
        model = AdaptersProjectsPostRequest(
            name=name, description=description, is_favorite=is_favorite, workflow_id=workflow_id)
        model = HtmlEscapeUtils.escape_html_in_object(model)
        logging.debug(f"Creating project with model: {model}")

        project = self.__projects_api.adapters_projects_post(adapters_projects_post_request=model)

        logging.info(f'Created new project (ID: {project.id})')
        logging.debug(f"Project created: {project}")

        return str(project.id)
