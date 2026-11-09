import json
import os
import tempfile
from unittest.mock import Mock, patch

import pytest

from src.testit_cli.models.config import Config
from src.testit_cli.service import Service
from src.testit_cli.v2_client import V2ApiError, V2Client
from tests.cli_support import assert_exit_code, invoke
from tests.helper import Helper


@pytest.fixture()
def runner():
    from click.testing import CliRunner

    return CliRunner()


def test_launch_requires_exactly_one_source(runner):
    result = invoke(runner, Helper.launch_minimal_argv())
    assert_exit_code(result, 2)
    assert "exactly one of" in result.output


def test_launch_rejects_multiple_sources(runner):
    argv = [
        "testrun", "create", "launch",
        "-u", "https://demo.testit.software",
        "-t", "T2lKd2pLZGI4WHRhaVZUejNl",
        "-pi", "3802f329-190c-4617-8bb0-2c3696abeb8f",
        "-ci", "3802f329-190c-4617-8bb0-2c3696abeb8f",
        "--test-plan-id", "3802f329-190c-4617-8bb0-2c3696abeb8f",
        "--filter", "tags=smoke",
    ]
    result = invoke(runner, argv)
    assert_exit_code(result, 2)
    assert "exactly one of" in result.output


def test_launch_rejects_invalid_filter(runner):
    argv = Helper.launch_minimal_argv() + ["--filter", "namespace=foo"]
    result = invoke(runner, argv)
    assert_exit_code(result, 2)
    assert "Invalid value" in result.output or "Unsupported filter" in result.output


def test_launch_rejects_empty_ids_file(runner):
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8", suffix=".txt") as tmp:
        tmp.write("# empty\n")
        path = tmp.name
    try:
        argv = Helper.launch_minimal_argv() + ["--autotest-external-ids-file", path]
        result = invoke(runner, argv)
        assert_exit_code(result, 2)
        assert "empty" in result.output.lower()
    finally:
        os.unlink(path)


def test_service_launch_by_tags(capsys):
    config = Config(
        url="https://demo.testit.software",
        token="token",
        project_id="proj",
        configuration_id="cfg",
        launch_tags=["smoke"],
        testrun_name="Nightly",
        output="",
    )
    v2 = Mock(spec=V2Client)
    v2.search_autotest_external_ids.return_value = ["ext-a", "ext-b"]
    v2.create_run_by_auto_tests.return_value = "run-123"

    service = Service(config, Mock(), Mock(), Mock(), Mock(), v2)
    service.launch_test_run()

    v2.search_autotest_external_ids.assert_called_once_with("proj", ["smoke"])
    v2.create_run_by_auto_tests.assert_called_once_with(
        "proj", "cfg", ["ext-a", "ext-b"], name="Nightly"
    )
    assert capsys.readouterr().out.strip() == "run-123"


def test_service_launch_by_ids_file_skips_search(capsys):
    config = Config(
        url="https://demo.testit.software",
        token="token",
        project_id="proj",
        configuration_id="cfg",
        autotest_external_ids=["ext-1"],
        output="",
    )
    v2 = Mock(spec=V2Client)
    v2.create_run_by_auto_tests.return_value = "run-456"

    Service(config, Mock(), Mock(), Mock(), Mock(), v2).launch_test_run()

    v2.search_autotest_external_ids.assert_not_called()
    v2.create_run_by_auto_tests.assert_called_once_with(
        "proj", "cfg", ["ext-1"], name=None
    )
    assert capsys.readouterr().out.strip() == "run-456"


def test_service_launch_by_test_plan(capsys):
    config = Config(
        url="https://demo.testit.software",
        token="token",
        project_id="proj",
        configuration_id="cfg",
        test_plan_id="plan",
        output="",
    )
    v2 = Mock(spec=V2Client)
    v2.search_test_point_work_item_ids.return_value = ["wi-1"]
    v2.create_run_by_work_items.return_value = "run-789"

    Service(config, Mock(), Mock(), Mock(), Mock(), v2).launch_test_run()

    v2.search_test_point_work_item_ids.assert_called_once_with("plan", "cfg")
    v2.create_run_by_work_items.assert_called_once_with(
        "proj", "plan", "cfg", ["wi-1"], name=None
    )
    assert capsys.readouterr().out.strip() == "run-789"


def test_service_launch_empty_search_raises():
    config = Config(
        url="https://demo.testit.software",
        token="token",
        project_id="proj",
        configuration_id="cfg",
        launch_tags=["missing"],
        output="",
    )
    v2 = Mock(spec=V2Client)
    v2.search_autotest_external_ids.return_value = []

    with pytest.raises(ValueError, match="No autotest external IDs"):
        Service(config, Mock(), Mock(), Mock(), Mock(), v2).launch_test_run()


def test_service_launch_writes_output_file(capsys):
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as tmp:
        path = tmp.name
    config = Config(
        url="https://demo.testit.software",
        token="token",
        project_id="proj",
        configuration_id="cfg",
        autotest_external_ids=["ext-1"],
        output=path,
    )
    v2 = Mock(spec=V2Client)
    v2.create_run_by_auto_tests.return_value = "run-out"

    try:
        Service(config, Mock(), Mock(), Mock(), Mock(), v2).launch_test_run()
        assert capsys.readouterr().out.strip() == "run-out"
        with open(path, encoding="utf-8") as handle:
            assert handle.read() == "run-out"
    finally:
        os.unlink(path)


def test_v2_client_search_and_create_by_auto_tests():
    client = V2Client("https://demo.testit.software", "tok", disable_cert_validation=True)

    search_payload = [{"externalId": "a"}, {"externalId": "b"}, {"externalId": "a"}]
    create_payload = {"id": "run-1"}

    with patch.object(client, "_V2Client__http") as http:
        search_resp = Mock()
        search_resp.status = 200
        search_resp.data = json.dumps(search_payload).encode("utf-8")

        create_resp = Mock()
        create_resp.status = 200
        create_resp.data = json.dumps(create_payload).encode("utf-8")

        http.request.side_effect = [search_resp, create_resp]

        ids = client.search_autotest_external_ids("proj", ["smoke"])
        assert ids == ["a", "b"]

        run_id = client.create_run_by_auto_tests("proj", "cfg", ids, name="N")
        assert run_id == "run-1"
        assert http.request.call_count == 2


def test_v2_client_raises_on_http_error():
    client = V2Client("https://demo.testit.software", "tok")
    with patch.object(client, "_V2Client__http") as http:
        resp = Mock()
        resp.status = 400
        resp.data = b'{"error":"bad"}'
        http.request.return_value = resp

        with pytest.raises(V2ApiError) as exc_info:
            client.create_run_by_auto_tests("p", "c", ["x"])
        assert exc_info.value.status == 400
