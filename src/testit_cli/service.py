import logging

from .models.config import Config
from .parser import Parser
from .apiclient import ApiClient
from .importer import Importer


class Service:
    def __init__(
        self,
        config: Config,
        api_client: ApiClient,
        parser: Parser,
        importer: Importer,
    ):
        self.__config = config
        self.__api_client = api_client
        self.__parser = parser
        self.__importer = importer

    def import_results(self):
        self.__upload_results()
        self.finished_testrun()

    def upload_results(self):
        self.__upload_results()

    def create_testrun(self):
        test_run_id = self.__create_test_run()
        with open(self.__config.output, "w") as text_file:
            text_file.write(test_run_id)

    def finished_testrun(self):
        self.__api_client.complete_test_run(self.__config.testrun_id)

    def __create_test_run(self):
        return self.__api_client.create_test_run(
            self.__config.project_id, self.__config.testrun_name
        )

    def __upload_results(self):
        logging.info("Collecting log files ...")

        results = self.__parser.read_file()

        if self.__config.testrun_id is None:
            test_run_id = self.__create_test_run()
            self.__config.testrun_id = test_run_id
        else:
            test_run = self.__api_client.get_test_run(self.__config.testrun_id)
            self.__config.project_id = test_run.project_id

        logging.info("Sending test results to Test IT ...")

        self.__importer.send_results(results)

        logging.info("Successfully sent test results")
