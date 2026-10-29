import os
import tempfile

import pytest

from src.testit_cli.launch_filter import (
    LaunchFilterError,
    parse_launch_filter,
    read_autotest_external_ids_file,
)


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("tags=smoke", ["smoke"]),
        ("tags=smoke,nightly", ["smoke", "nightly"]),
        ("tags= smoke , nightly ", ["smoke", "nightly"]),
        ("TAGS=a,b", ["a", "b"]),
    ],
)
def test_parse_launch_filter_ok(raw, expected):
    assert parse_launch_filter(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        "",
        "   ",
        "smoke",
        "namespace=foo",
        "tags=",
        "tags=,,,",
    ],
)
def test_parse_launch_filter_invalid(raw):
    with pytest.raises(LaunchFilterError):
        parse_launch_filter(raw)


def test_read_autotest_external_ids_file():
    content = """
# comment
ext-1

ext-2
# another
ext-1
ext-3
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8", suffix=".txt") as tmp:
        tmp.write(content)
        path = tmp.name
    try:
        assert read_autotest_external_ids_file(path) == ["ext-1", "ext-2", "ext-3"]
    finally:
        os.unlink(path)


def test_read_autotest_external_ids_file_empty():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8", suffix=".txt") as tmp:
        tmp.write("# only comments\n\n")
        path = tmp.name
    try:
        assert read_autotest_external_ids_file(path) == []
    finally:
        os.unlink(path)
