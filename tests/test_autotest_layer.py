import pytest
from src.testit_cli.converter import Converter
from src.testit_cli.models.testcase import TestCase


@pytest.mark.parametrize("raw", [None, "", "  "])
def test_layer_to_api_model_omits_when_empty(raw):
    assert Converter.layer_to_api_model(raw) is None


def test_layer_to_api_model_maps_name_and_run_source():
    layer = Converter.layer_to_api_model("API")
    assert layer is not None
    assert layer.name == "API"
    assert str(layer.source) == "Run"


def test_create_autotest_request_includes_layer_when_set():
    result = TestCase("test", "ns", "cls", 1)
    request = Converter.test_result_to_create_autotest_request(
        result, "ext-id", "proj-id", layer="E2E"
    )
    assert request.layer is not None
    assert request.layer.name == "E2E"
    assert str(request.layer.source) == "Run"


def test_create_autotest_request_omits_layer_when_not_set():
    result = TestCase("test", "ns", "cls", 1)
    request = Converter.test_result_to_create_autotest_request(
        result, "ext-id", "proj-id"
    )
    assert "layer" not in request.to_dict()


def test_update_autotest_request_always_resets_layer_false_and_sets_layer_when_given():
    result = TestCase("test", "ns", "cls", 1)
    result.set_is_flaky(False)
    request = Converter.test_result_to_update_autotest_request(
        result, "ext-id", "proj-id", layer="API"
    )
    assert request.reset_layer is False
    assert request.layer is not None
    assert request.layer.name == "API"
