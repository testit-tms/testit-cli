import pytest

from tests.cli_support import (
    assert_exit_code,
    assert_help_ok,
    assert_invalid_parameter_value,
    assert_missing_required_option,
    invoke,
)
from tests.helper import Helper


@pytest.fixture()
def runner():
    from click.testing import CliRunner

    return CliRunner()


def test_root_help_lists_known_commands(runner):
    result = invoke(runner, [])
    assert_help_ok(result, "Commands:")
    for line in Helper.root_help_command_lines():
        assert line in result.output


@pytest.mark.parametrize("argv, unknown_token", Helper.unknown_subcommand_cases())
def test_unknown_command_reports_error(runner, argv, unknown_token):
    result = invoke(runner, argv)
    assert_exit_code(result, 2)
    assert f"No such command '{unknown_token}'" in result.output


@pytest.mark.parametrize("argv, command_lines", Helper.subgroup_help_cases())
def test_subgroup_help_lists_nested_commands(runner, argv, command_lines):
    result = invoke(runner, argv)
    assert_help_ok(result, "Commands:")
    for fragment in command_lines:
        assert fragment in result.output


@pytest.mark.parametrize("argv, missing_long_option", Helper.missing_required_option_cases())
def test_missing_required_option(runner, argv, missing_long_option):
    assert_missing_required_option(invoke(runner, argv), missing_long_option)


@pytest.mark.parametrize("argv", Helper.invalid_option_cases())
def test_unrecognized_option_exits_with_usage_error(runner, argv):
    assert_exit_code(invoke(runner, argv), 2)


@pytest.mark.parametrize("argv, doc_fragment", Helper.command_help_doc_cases())
def test_command_help_includes_description(runner, argv, doc_fragment):
    assert_help_ok(invoke(runner, argv), doc_fragment)


@pytest.mark.parametrize("argv, option_hint", Helper.invalid_rerun_uuid_multi_option_cases())
def test_rerun_rejects_invalid_uuid_for_optional_multi_options(runner, argv, option_hint):
    assert_invalid_parameter_value(invoke(runner, argv), option_hint)
