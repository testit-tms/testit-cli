"""The module provides functionality for working with TMS"""
import logging
import os
import typing

from testit_api_client import ApiClient as TmsClient, CreateEmptyTestRunApiModel, AutoTestApiResult, \
    AutoTestSearchApiModel, AssignAttachmentApiModel
from testit_api_client import Configuration
from testit_api_client.api import AttachmentsApi, AutoTestsApi, TestRunsApi, TestResultsApi
from testit_api_client.models import TestResultShortResponse

from .converter import Converter
from .models.testrun import TestRun
from .html_escape_utils import HtmlEscapeUtils


class ApiClient:
    """Class representing a api client"""

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

    def create_test_run(self, project_id: str, name: str) -> TestRun:
        """Function creates test run and returns test run id."""
        model = CreateEmptyTestRunApiModel(project_id=project_id, name=name)
        model = HtmlEscapeUtils.escape_html_in_object(model)
        logging.debug(f"Creating test run with model: {model}")

        test_run = self.__test_run_api.create_empty(model)

        logging.info(f'Created new testrun (ID: {test_run.id})')
        logging.debug(f"Test run created: {test_run}")

        return Converter.test_run_v2_get_model_to_test_run(test_run)

    def update_test_run(self, test_run: TestRun):
        """Function updates test run."""
        model = Converter.test_run_to_update_empty_request(test_run)
        model = HtmlEscapeUtils.escape_html_in_object(model)
        logging.debug(f"Updating test run with model: {model}")

        self.__test_run_api.update_empty(model)

        logging.info(f'Updated testrun (ID: {test_run.id})')

    def complete_test_run(self, test_run_id: str):
        """Function completes test run."""
        logging.debug(f"Completing test run {test_run_id}")

        test_run = self.get_test_run(test_run_id)
        if test_run is not None and test_run.state != "Completed":
            self.__test_run_api.complete_test_run(test_run_id)

        logging.info(f"Completed testrun (ID: {test_run_id})")

    def get_test_run(self, test_run_id: str) -> Converter.test_run_v2_get_model_to_test_run:
        """Function gets test run and returns test run."""
        logging.debug(f"Getting test run {test_run_id}")

        test_run = self.__test_run_api.get_test_run_by_id(test_run_id)
        if test_run is not None:
            logging.debug(f"Got testrun (ID: {test_run_id})")
            return Converter.test_run_v2_get_model_to_test_run(test_run)

        logging.error(f"Test run {test_run_id} not found!")

    def get_autotests(self, model: AutoTestSearchApiModel) \
            -> list[AutoTestApiResult]:
        """Function returns list of AutoTestApiResult."""
        logging.debug(f"Getting autotests: {model}")

        autotests = self.__autotest_api.api_v2_auto_tests_search_post(auto_test_search_api_model=model)

        logging.debug(f"Got autotests: {autotests}")

        return autotests

    def create_autotest(self, model: Converter.test_result_to_create_autotest_request):
        """Function creates autotest and returns autotest id."""
        model = HtmlEscapeUtils.escape_html_in_object(model)

        logging.debug(f"Creating autotest {model}")

        response = self.__autotest_api.create_auto_test(auto_test_post_model=model)

        logging.debug(f"Created autotest {response}")

        return response.id

    def update_autotest(self, model: Converter.test_result_to_update_autotest_request):
        """Function updates autotest"""
        try:
            model = HtmlEscapeUtils.escape_html_in_object(model)

            logging.debug(f"Updating autotest {model}")

            self.__autotest_api.update_auto_test(auto_test_put_model=model)

            logging.debug(f'Updated "{model.name}" successfully!')
        except Exception as exc:
            logging.error(f'Updated "{model.name}" status: {exc}')

    def send_test_result(
            self, testrun_id: str, model: Converter.test_result_to_testrun_result_post_model
    ):
        """Function sends autotest result to test run"""
        try:
            model = HtmlEscapeUtils.escape_html_in_object(model)

            logging.debug(f"Adding autotest results to testrun {testrun_id}: {model}")

            self.__test_run_api.set_auto_test_results_for_test_run(
                id=testrun_id, auto_test_results_for_test_run_model=[model]
            )
            logging.debug(
                f"Added autotest results to testrun {testrun_id} successfully"
            )
        except Exception as exc:
            logging.error(f"Set result status: {exc}")

    def upload_attachments(self, attachments: typing.List[str]) -> typing.List[AssignAttachmentApiModel]:
        """Function upload attachments and returns list of AttachmentPutModel."""
        attachment_ids = []

        for attachment in attachments:
            if os.path.isfile(attachment):
                try:
                    attachment_response = self.__attachments_api.api_v2_attachments_post(
                        file=attachment)

                    attachment_ids.append(AssignAttachmentApiModel(id=attachment_response.id))

                    logging.debug(f'Attachment "{attachment}" was uploaded')
                except Exception as exc:
                    logging.error(f'Upload attachment "{attachment}" status: {exc}')
            else:
                logging.error(f'File "{attachment}" was not found!')

        return attachment_ids

    def get_test_results(
            self,
            model: Converter.testrun_id_and_configuration_id_and_in_progress_outcome_to_test_results_search_post_request
    ) -> typing.List[TestResultShortResponse]:
        """Function returns list of TestResultShortGetModel."""
        logging.debug(f"Getting test results: {model}")

        test_results = self.__test_results_api.api_v2_test_results_search_post(
            test_results_filter_api_model=model)

        logging.debug(f"Got test results: {test_results}")

        return test_results
