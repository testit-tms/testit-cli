import os
import tempfile

import pytest
from unittest.mock import Mock

from src.testit_cli.service import Service
from src.testit_cli.models.config import Config


@pytest.fixture
def mock_config():
    return Mock(spec=Config)


@pytest.fixture
def api_client():
    return Mock()


@pytest.fixture
def service(mock_config, api_client):
    return Service(
        config=mock_config,
        api_client=api_client,
        parser=Mock(),
        importer=Mock(),
        autotests_filter=Mock(),
    )


def _assert_utf8_file_equals(path: str, expected: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        assert f.read() == expected
    with open(path, "rb") as f:
        assert f.read().decode("utf-8") == expected


def test_write_to_output_uses_utf8_encoding(service, mock_config):
    # Deliberate non-ASCII payload to assert UTF-8 read/write round-trip.
    content = "Тестовый контент с кириллицей: АБВГД абвгд"
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as tmp:
        path = tmp.name
    mock_config.output = path
    try:
        service._Service__write_to_output(content)
        _assert_utf8_file_equals(path, content)
    finally:
        if os.path.exists(path):
            os.unlink(path)


def test_write_to_output_creates_parent_directory(service, mock_config):
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, "nested", "out.txt")
        mock_config.output = path
        service._Service__write_to_output("test content")
        assert os.path.isfile(path)
        _assert_utf8_file_equals(path, "test content")


def test_rerun_test_run_forwards_config_to_api_client(service, mock_config, api_client):
    mock_config.testrun_id = "3802f329-190c-4617-8bb0-2c3696abeb8f"
    mock_config.configuration_ids = [
        "15dbb164-c1aa-4cbf-830c-8c01ae14f4fb",
        "5236eb3f-7c05-46f9-a609-dc0278896464",
    ]
    mock_config.status_codes = ["Failed"]
    mock_config.failure_categories = ["cat-1"]
    mock_config.namespace = "ns"
    mock_config.classname = "MyClass"
    mock_config.auto_test_global_ids = [10, 20]
    mock_config.auto_test_tags = ["smoke"]
    mock_config.exclude_auto_test_tags = ["slow"]
    mock_config.auto_test_name = "test-name"
    mock_config.test_result_ids = [
        "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
        "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
    ]
    mock_config.webhook_ids = [
        "cccccccc-cccc-4ccc-8ccc-cccccccccccc",
    ]

    service.rerun_test_run()

    api_client.rerun_test_run.assert_called_once_with(
        "3802f329-190c-4617-8bb0-2c3696abeb8f",
        configuration_ids=[
            "15dbb164-c1aa-4cbf-830c-8c01ae14f4fb",
            "5236eb3f-7c05-46f9-a609-dc0278896464",
        ],
        status_codes=["Failed"],
        failure_categories=["cat-1"],
        namespace="ns",
        class_name="MyClass",
        auto_test_global_ids=[10, 20],
        auto_test_tags=["smoke"],
        exclude_auto_test_tags=["slow"],
        auto_test_name="test-name",
        test_result_ids=[
            "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
            "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
        ],
        webhook_ids=["cccccccc-cccc-4ccc-8ccc-cccccccccccc"],
    )
