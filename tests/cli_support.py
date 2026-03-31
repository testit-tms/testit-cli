"""Shared assertions for the Click CLI: less duplication, tolerant of minor output formatting changes."""

from __future__ import annotations

from typing import Iterable

from click.testing import CliRunner, Result


def invoke(runner: CliRunner, argv: Iterable[str]) -> Result:
    from src.testit_cli.click_commands import execute

    return runner.invoke(execute, list(argv))


def assert_help_ok(result: Result, doc_fragment: str) -> None:
    assert result.exit_code == 0, result.output
    assert doc_fragment in result.output, f"Expected help text to contain description fragment: {doc_fragment!r}"


def assert_missing_required_option(result: Result, long_option: str) -> None:
    """Click reports a missing required option as 'Error: Missing option …' plus the flag name."""
    assert result.exit_code == 2, result.output
    assert "Error: Missing option" in result.output
    assert long_option in result.output


def assert_exit_code(result: Result, code: int) -> None:
    assert result.exit_code == code, result.output


def assert_invalid_parameter_value(result: Result, option_hint: str) -> None:
    """Click reports invalid values as 'Invalid value for …' (e.g. failed UUID callback)."""
    assert result.exit_code == 2, result.output
    assert "Invalid value" in result.output
    assert option_hint in result.output
