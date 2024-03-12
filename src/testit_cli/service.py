import logging

from .models.config import Config
from .models.testrun import TestRun
from .parser import Parser
from .apiclient import ApiClient
from .dir_worker import DirWorker
from .file_worker import FileWorker
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
        self.__api_client.complete_test_run(self.__config.testrun_id)

    def upload_results(self):
        self.__upload_results()

    def create_test_run(self):
        test_run = self.__create_test_run()
        self.__update_test_run_with_attachments(test_run)

        DirWorker.create_dir(self.__config.output)

        with open(self.__config.output, "w") as text_file:
            text_file.write(test_run.id)

    def finished_test_run(self):
        test_run = self.__api_client.get_test_run(self.__config.testrun_id)
        self.__update_test_run_with_attachments(test_run)

        self.__api_client.complete_test_run(self.__config.testrun_id)

    def upload_attachments_for_test_run(self):
        test_run = self.__api_client.get_test_run(self.__config.testrun_id)
        self.__update_test_run_with_attachments(test_run)

    def __create_test_run(self) -> TestRun:
        return self.__api_client.create_test_run(
            self.__config.project_id,
            self.__config.testrun_name
        )

    def __upload_attachments(self) -> list:
        files = []

        for path_to_attachments in self.__config.paths_to_attachments:
            files.extend(FileWorker.get_files(path_to_attachments))

        return self.__api_client.upload_attachments(files)

    def __upload_results(self):
        logging.info("Collecting log files ...")

        results = self.__parser.read_file()

        if self.__config.testrun_id is None:
            test_run = self.__create_test_run()
            self.__config.testrun_id = test_run.id
        else:
            test_run = self.__api_client.get_test_run(self.__config.testrun_id)
            self.__config.project_id = test_run.project_id

        logging.info("Sending test results to Test IT ...")

        self.__importer.send_results(results)

        self.__update_test_run_with_attachments(test_run)

        logging.info("Successfully sent test results")

    def __update_test_run_with_attachments(self, test_run: TestRun):
        test_run.attachments.extend(self.__upload_attachments())
        self.__api_client.update_test_run(test_run)
