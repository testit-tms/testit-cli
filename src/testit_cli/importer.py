import hashlib

from tqdm import tqdm

from .apiclient import ApiClient
from .converter import Converter
from .models.config import Config
from .models.testcase import TestCase


class Importer:
    def __init__(self, api_client: ApiClient, config: Config):
        self.__api_client = api_client
        self.__config = config

    def send_results(self, results: [TestCase]):
        for result in tqdm(results, desc="Uploading"):
            external_id = self.__get_external_id(
                result.get_name_space()
                + result.get_class_name()
                + result.get_name()
            )

            autotest = self.__api_client.get_autotest(
                Converter.project_id_and_external_id_to_autotests_search_post_request(
                    self.__config.project_id, external_id
                )
            )

            if not autotest:
                self.__api_client.create_autotest(
                    Converter.test_result_to_create_autotest_request(
                        result, external_id, self.__config.project_id
                    )
                )
            else:
                result.set_is_flaky(autotest[0]['is_flaky'])

                self.__api_client.update_autotest(
                    Converter.test_result_to_update_autotest_request(
                        result, external_id, self.__config.project_id
                    )
                )

            self.__api_client.send_test_result(
                self.__config.testrun_id,
                Converter.test_result_to_testrun_result_post_model(
                    result, external_id, self.__config.configuration_id
                ),
            )

    @staticmethod
    def __get_external_id(value: str):
        return hashlib.md5(value.encode("utf-8")).hexdigest()
