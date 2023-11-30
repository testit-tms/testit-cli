"""The module provides functionality for working with TMS"""
import logging
import os
import typing

from testit_api_client import ApiClient as TmsClient
from testit_api_client import Configuration
from testit_api_client.apis import AttachmentsApi, AutoTestsApi, TestRunsApi
from testit_api_client.models import AttachmentPutModel, CreateEmptyRequest

from .converter import Converter
from .models.testrun import TestRun


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

    def create_test_run(self, project_id: str, name: str) -> TestRun:
        """Function creates test run and returns test run id."""
        model = CreateEmptyRequest(project_id=project_id, name=name)
        logging.debug(f"Creating test run with model: {model}")

        test_run = self.__test_run_api.create_empty(create_empty_request=model)

        logging.info(f'Created new testrun (ID: {test_run["id"]})')
        logging.debug(f"Test run created: {test_run}")

        return Converter.test_run_v2_get_model_to_test_run(test_run)

    def update_test_run(self, test_run: TestRun):
        """Function updates test run."""
        model = Converter.test_run_to_update_empty_request(test_run)
        logging.debug(f"Updating test run with model: {model}")

        response = self.__test_run_api.update_empty(update_empty_request=model)

        logging.info(f'Updated testrun (ID: {test_run.id})')
        logging.debug(f"Test run updated: {response}")

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

    def get_autotest(self, model: Converter.project_id_and_external_id_to_autotests_search_post_request):
        """Function returns autotest."""
        logging.debug(f"Getting autotest {model}")

        autotest = self.__autotest_api.api_v2_auto_tests_search_post(api_v2_auto_tests_search_post_request=model)

        logging.debug(f"Got autotest {autotest}")

        return autotest

    def create_autotest(self, model: Converter.test_result_to_create_autotest_request):
        """Function creates autotest and returns autotest id."""
        logging.debug(f"Creating autotest {model}")

        response = self.__autotest_api.create_auto_test(create_auto_test_request=model)

        logging.debug(f"Created autotest {response}")

        return response["id"]

    def update_autotest(self, model: Converter.test_result_to_update_autotest_request):
        """Function updates autotest"""
        try:
            logging.debug(f"Updating autotest {model}")

            self.__autotest_api.update_auto_test(update_auto_test_request=model)

            logging.debug(f'Updated "{model.name}" successfully!')
        except Exception as exc:
            logging.error(f'Updated "{model.name}" status: {exc}')

    def send_test_result(
            self, testrun_id: str, model: Converter.test_result_to_testrun_result_post_model
    ):
        """Function sends autotest result to test run"""
        try:
            logging.debug(f"Adding autotest results to testrun {testrun_id}: {model}")

            self.__test_run_api.set_auto_test_results_for_test_run(
                id=testrun_id, auto_test_results_for_test_run_model=[model]
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
                try:
                    attachment_response = self.__attachments_api.api_v2_attachments_post(file=open(attachment, "rb"))

                    attachment_ids.append(AttachmentPutModel(attachment_response['id']))

                    logging.debug(f'Attachment "{attachment}" was uploaded')
                except Exception as exc:
                    logging.error(f'Upload attachment "{attachment}" status: {exc}')
            else:
                logging.error(f'File "{attachment}" was not found!')

        return attachment_ids
