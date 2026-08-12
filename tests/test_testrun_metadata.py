from unittest.mock import Mock

import pytest
from testit_api_client.model.link_put_model import LinkPutModel
from testit_api_client.model.link_type import LinkType

from src.testit_cli.models.testrun import TestRun
from src.testit_cli.models.testrun_link import TestRunLink
from src.testit_cli.service import Service
from src.testit_cli.testrun_metadata import (
    merge_links,
    merge_tags,
    parse_testrun_links,
    parse_testrun_tags,
    to_create_link_models,
)


@pytest.mark.parametrize(
    "raw, expected",
    [
        (None, None),
        ("", None),
        ("  ", None),
        ("smoke, nightly", ["smoke", "nightly"]),
        ('["smoke", "nightly"]', ["smoke", "nightly"]),
        ("smoke", ["smoke"]),
    ],
)
def test_parse_testrun_tags(raw, expected):
    assert parse_testrun_tags(raw) == expected


def test_parse_testrun_tags_invalid_json_array():
    assert parse_testrun_tags("[") is None


def test_parse_testrun_links_ok():
    raw = (
        '[{"url":"https://ci.example/jobs/1","title":"CI Job","type":"Related"},'
        '{"url":"https://ci.example/jobs/2"}]'
    )
    links = parse_testrun_links(raw)
    assert links == [
        TestRunLink(
            url="https://ci.example/jobs/1",
            title="CI Job",
            description=None,
            link_type="Related",
        ),
        TestRunLink(
            url="https://ci.example/jobs/2",
            title=None,
            description=None,
            link_type=None,
        ),
    ]


@pytest.mark.parametrize("raw", [None, "", "not-json", "{}", '[{"title":"x"}]'])
def test_parse_testrun_links_invalid(raw):
    assert parse_testrun_links(raw) is None


def test_merge_tags_and_links_dedupe():
    assert merge_tags(["a"], ["a", "b"]) == ["a", "b"]
    related = LinkType("Related")
    existing = [LinkPutModel(url="https://a", type=related, has_info=False)]
    incoming = [
        LinkPutModel(url="https://a", type=related, has_info=False),
        LinkPutModel(url="https://b", type=related, has_info=False),
    ]
    merged = merge_links(existing, incoming)
    assert [link.url for link in merged] == ["https://a", "https://b"]


def test_to_create_link_models_defaults_type():
    models = to_create_link_models([TestRunLink(url="https://ci.example/1")])
    assert models is not None
    assert len(models) == 1
    assert models[0].url == "https://ci.example/1"
    assert str(models[0].type) == "Related"


def test_create_test_run_passes_tags_and_links():
    api_client = Mock()
    api_client.create_test_run.return_value = TestRun(
        id="run-1",
        project_id="proj-1",
        state="InProgress",
        name="Run",
        description="",
        launch_source="",
        attachments=[],
        links=[],
        tags=["smoke"],
    )
    api_client.upload_attachments.return_value = []
    config = Mock(
        project_id="proj-1",
        testrun_name="Run",
        testrun_tags=["smoke"],
        testrun_links=[TestRunLink(url="https://ci.example/1", title="CI", link_type="Related")],
        paths_to_attachments=[],
        output="out.txt",
    )
    service = Service(config, api_client, Mock(), Mock(), Mock())
    service._Service__write_to_output = Mock()

    service.create_test_run()

    kwargs = api_client.create_test_run.call_args.kwargs
    assert kwargs["tags"] == ["smoke"]
    assert kwargs["links"] is not None
    assert kwargs["links"][0].url == "https://ci.example/1"


def test_upload_results_merges_tags_and_links_early():
    related = LinkType("Related")
    existing = TestRun(
        id="run-1",
        project_id="proj-1",
        state="InProgress",
        name="Run",
        description="",
        launch_source="",
        attachments=[],
        links=[LinkPutModel(url="https://existing", type=related, has_info=False)],
        tags=["ui"],
    )
    api_client = Mock()
    api_client.get_test_run.return_value = existing
    api_client.upload_attachments.return_value = []
    parser = Mock()
    parser.read_file.return_value = []
    importer = Mock()
    config = Mock(
        testrun_id="run-1",
        testrun_tags=["smoke"],
        testrun_links=[TestRunLink(url="https://ci.example/1")],
        paths_to_attachments=[],
        project_id=None,
    )
    service = Service(config, api_client, parser, importer, Mock())

    service.upload_results()

    assert api_client.update_test_run.call_count >= 1
    first_update = api_client.update_test_run.call_args_list[0].args[0]
    assert first_update.tags == ["ui", "smoke"]
    assert [link.url for link in first_update.links] == ["https://existing", "https://ci.example/1"]
