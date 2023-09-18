from testit_api_client.models import (
    AutotestsSelectModelFilter,
    ApiV2AutoTestsSearchPostRequest,
    CreateAutoTestRequest,
    UpdateAutoTestRequest,
    AutoTestResultsForTestRunModel,
)


class Converter:
    @staticmethod
    def project_id_and_external_id_to_autotests_search_post_request(project_id: str, external_id: str):
        autotests_filter = AutotestsSelectModelFilter(
            project_ids=[project_id],
            external_ids=[external_id],
            is_deleted=False)

        return ApiV2AutoTestsSearchPostRequest(filter=autotests_filter)

    @staticmethod
    def test_result_to_create_autotest_request(result, external_id: str, project_id: str):
        return CreateAutoTestRequest(
            external_id=external_id,
            project_id=project_id,
            name=result.get_name(),
            namespace=result.get_name_space(),
            classname=result.get_class_name(),
        )

    @staticmethod
    def test_result_to_update_autotest_request(result, external_id: str, project_id: str):
        return UpdateAutoTestRequest(
            external_id=external_id,
            project_id=project_id,
            name=result.get_name(),
            namespace=result.get_name_space(),
            classname=result.get_class_name(),
            is_flaky=result.get_is_flaky()
        )

    @staticmethod
    def test_result_to_testrun_result_post_model(
        result, external_id: str, configuration_id: str
    ):
        return AutoTestResultsForTestRunModel(
            configuration_id,
            external_id,
            result.get_status(),
            traces=result.get_trace(),
            duration=round(result.get_duration()),
            message=result.get_message(),
        )
