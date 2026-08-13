import hashlib

from adapters_api.model.adapters_auto_tests_search_post_request import AdaptersAutoTestsSearchPostRequest
from adapters_api.model.adapters_test_results_search_post_request import AdaptersTestResultsSearchPostRequest
from adapters_api.model.auto_test_api_result import AutoTestApiResult
from .apiclient import ApiClient
from .converter import Converter
from .filter_factory import FilterFactory
from .models.config import Config


class AutotestsFilter:
    def __init__(self, api_client: ApiClient, config: Config):
        self.__api_client = api_client
        self.__config = config

    def create_filter(self):
        """Function returns str of filter by autotests for test Framework run command."""
        test_results_search_post_request: AdaptersTestResultsSearchPostRequest = (
            Converter.testrun_id_and_configuration_id_and_in_progress_outcome_to_test_results_search_post_request(
                self.__config.testrun_id,
                self.__config.configuration_id))
        test_results = self.__api_client.get_test_results(test_results_search_post_request)

        if len(test_results) == 0:
            exception = f"Couldn't get the test results in progress by test run id \"{self.__config.testrun_id}\" " + \
                f"and configuration id \"{self.__config.configuration_id}\""

            raise Exception(exception)

        external_ids: list[str] = Converter.test_result_short_models_to_autotest_external_ids(test_results)
        autotests_search_post_request: AdaptersAutoTestsSearchPostRequest = (
            Converter.external_ids_to_autotests_search_post_request(external_ids))
        autotests: list[AutoTestApiResult] = self.__api_client.get_autotests(autotests_search_post_request)
        external_keys: list[str] = Converter.autotest_models_to_external_keys(autotests)

        return FilterFactory.get(self.__config, external_keys)

    @staticmethod
    def __get_external_id(value: str) -> str:
        return hashlib.md5(value.encode("utf-8")).hexdigest()
