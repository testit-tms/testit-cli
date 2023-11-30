from click.testing import CliRunner
import pytest

from src.testit_cli.click_commands import execute
from tests.helper import Helper


@pytest.fixture()
def runner():
    return CliRunner()


def test_run_without_command(runner):
    message = "Options:\n  --help  Show this message and exit.\n\nCommands:\n  results  Uploading the test results\n  testrun  Working with the test run\n"
    result = runner.invoke(execute, [])

    assert message in result.output
    assert result.exit_code == 0


def test_run_with_another_command(runner):
    another_command = "run"
    message = f"Error: No such command '{another_command}'"
    result = runner.invoke(execute, [another_command])

    assert message in result.output
    assert result.exit_code == 2


@pytest.mark.parametrize("command, message", [
    ("results", "Options:\n  --help  Show this message and exit.\n\nCommands:\n  import  Uploading the first test results\n  upload  Uploading results from different streams\n"),
    ("testrun", "Options:\n  --help  Show this message and exit.\n\nCommands:\n  complete            Completing the test run\n  create              Creating a new test run\n  upload_attachments  Uploading attachments for the test run\n")])
def test_run_with_command(runner, command, message):
    result = runner.invoke(execute, [command])

    assert message in result.output
    assert result.exit_code == 0


def test_run_results_with_another_command(runner):
    another_command = "run"
    message = f"Error: No such command '{another_command}'"
    result = runner.invoke(execute, ["results", another_command])

    assert message in result.output
    assert result.exit_code == 2


@pytest.mark.parametrize("commands, output", [
    (Helper.get_command_results_import_with_long_arguments_without_url_argument(), Helper.get_output_for_results_import_without_url_argument()),
    (Helper.get_command_results_import_with_short_arguments_without_url_argument(), Helper.get_output_for_results_import_without_url_argument()),
    (Helper.get_command_results_import_with_long_arguments_without_token_argument(), Helper.get_output_for_results_import_without_token_argument()),
    (Helper.get_command_results_import_with_short_arguments_without_token_argument(), Helper.get_output_for_results_import_without_token_argument()),
    (Helper.get_command_results_import_with_long_arguments_without_project_id_argument(), Helper.get_output_for_results_import_without_project_id_argument()),
    (Helper.get_command_results_import_with_short_arguments_without_project_id_argument(), Helper.get_output_for_results_import_without_project_id_argument()),
    (Helper.get_command_results_import_with_long_arguments_without_configuration_id_argument(), Helper.get_output_for_results_import_without_configuration_id_argument()),
    (Helper.get_command_results_import_with_short_arguments_without_configuration_id_argument(), Helper.get_output_for_results_import_without_configuration_id_argument()),
    (Helper.get_command_results_import_with_long_arguments_without_results_argument(), Helper.get_output_for_results_import_without_results_argument()),
    (Helper.get_command_results_import_with_short_arguments_without_results_argument(), Helper.get_output_for_results_import_without_results_argument()),
    (Helper.get_command_results_upload_with_long_arguments_without_url_argument(), Helper.get_output_for_results_upload_without_url_argument()),
    (Helper.get_command_results_upload_with_short_arguments_without_url_argument(), Helper.get_output_for_results_upload_without_url_argument()),
    (Helper.get_command_results_upload_with_long_arguments_without_token_argument(), Helper.get_output_for_results_upload_without_token_argument()),
    (Helper.get_command_results_upload_with_short_arguments_without_token_argument(), Helper.get_output_for_results_upload_without_token_argument()),
    (Helper.get_command_results_upload_with_long_arguments_without_testrun_id_argument(), Helper.get_output_for_results_upload_without_testrun_id_argument()),
    (Helper.get_command_results_upload_with_short_arguments_without_testrun_id_argument(), Helper.get_output_for_results_upload_without_testrun_id_argument()),
    (Helper.get_command_results_upload_with_long_arguments_without_configuration_id_argument(), Helper.get_output_for_results_upload_without_configuration_id_argument()),
    (Helper.get_command_results_upload_with_short_arguments_without_configuration_id_argument(), Helper.get_output_for_results_upload_without_configuration_id_argument()),
    (Helper.get_command_results_upload_with_long_arguments_without_results_argument(), Helper.get_output_for_results_upload_without_results_argument()),
    (Helper.get_command_results_upload_with_short_arguments_without_results_argument(), Helper.get_output_for_results_upload_without_results_argument()),
    (Helper.get_command_testrun_create_with_long_arguments_without_url_argument(), Helper.get_output_for_testrun_create_without_url_argument()),
    (Helper.get_command_testrun_create_with_short_arguments_without_url_argument(), Helper.get_output_for_testrun_create_without_url_argument()),
    (Helper.get_command_testrun_create_with_long_arguments_without_token_argument(), Helper.get_output_for_testrun_create_without_token_argument()),
    (Helper.get_command_testrun_create_with_short_arguments_without_token_argument(), Helper.get_output_for_testrun_create_without_token_argument()),
    (Helper.get_command_testrun_create_with_long_arguments_without_project_id_argument(), Helper.get_output_for_testrun_create_without_project_id_argument()),
    (Helper.get_command_testrun_create_with_short_arguments_without_project_id_argument(), Helper.get_output_for_testrun_create_without_project_id_argument()),
    (Helper.get_command_testrun_create_with_long_arguments_without_output_argument(), Helper.get_output_for_testrun_create_without_output_argument()),
    (Helper.get_command_testrun_create_with_short_arguments_without_output_argument(), Helper.get_output_for_testrun_create_without_output_argument()),
    (Helper.get_command_testrun_complete_with_long_arguments_without_url_argument(), Helper.get_output_for_testrun_complete_without_url_argument()),
    (Helper.get_command_testrun_complete_with_short_arguments_without_url_argument(), Helper.get_output_for_testrun_complete_without_url_argument()),
    (Helper.get_command_testrun_complete_with_long_arguments_without_token_argument(), Helper.get_output_for_testrun_complete_without_token_argument()),
    (Helper.get_command_testrun_complete_with_short_arguments_without_token_argument(), Helper.get_output_for_testrun_complete_without_token_argument()),
    (Helper.get_command_testrun_complete_with_long_arguments_without_testrun_id_argument(), Helper.get_output_for_testrun_complete_without_testrun_id_argument()),
    (Helper.get_command_testrun_complete_with_short_arguments_without_testrun_id_argument(), Helper.get_output_for_testrun_complete_without_testrun_id_argument()),
    (Helper.get_command_testrun_upload_attachments_with_long_arguments_without_url_argument(), Helper.get_output_for_testrun_upload_attachments_without_url_argument()),
    (Helper.get_command_testrun_upload_attachments_with_short_arguments_without_url_argument(), Helper.get_output_for_testrun_upload_attachments_without_url_argument()),
    (Helper.get_command_testrun_upload_attachments_with_long_arguments_without_token_argument(), Helper.get_output_for_testrun_upload_attachments_without_token_argument()),
    (Helper.get_command_testrun_upload_attachments_with_short_arguments_without_token_argument(), Helper.get_output_for_testrun_upload_attachments_without_token_argument()),
    (Helper.get_command_testrun_upload_attachments_with_long_arguments_without_testrun_id_argument(), Helper.get_output_for_testrun_upload_attachments_without_testrun_id_argument()),
    (Helper.get_command_testrun_upload_attachments_with_short_arguments_without_testrun_id_argument(), Helper.get_output_for_testrun_upload_attachments_without_testrun_id_argument())])
def test_run_results_with_command_without_arguments(runner, commands, output):
    result = runner.invoke(execute, commands)

    assert output in result.output
    assert result.exit_code == 2


@pytest.mark.parametrize("commands_with_args", [
    Helper.get_command_results_import_with_long_arguments(),
    Helper.get_command_results_upload_with_long_arguments(),
    Helper.get_command_results_import_with_short_arguments(),
    Helper.get_command_results_upload_with_short_arguments(),
    Helper.get_command_results_import_with_all_long_arguments(),
    Helper.get_command_results_upload_with_all_long_arguments(),
    Helper.get_command_results_import_with_all_short_arguments(),
    Helper.get_command_results_upload_with_all_short_arguments(),
    Helper.get_command_testrun_complete_with_long_arguments(),
    Helper.get_command_testrun_create_with_long_arguments(),
    Helper.get_command_testrun_upload_attachments_with_long_arguments(),
    Helper.get_command_testrun_complete_with_short_arguments(),
    Helper.get_command_testrun_create_with_short_arguments(),
    Helper.get_command_testrun_upload_attachments_with_short_arguments(),
    Helper.get_command_testrun_complete_with_all_long_arguments(),
    Helper.get_command_testrun_create_with_all_long_arguments(),
    Helper.get_command_testrun_upload_attachments_with_all_long_arguments(),
    Helper.get_command_testrun_complete_with_all_short_arguments(),
    Helper.get_command_testrun_create_with_all_short_arguments(),
    Helper.get_command_testrun_upload_attachments_with_all_short_arguments()])
def test_run_with_commands_and_arguments(runner, commands_with_args):
    result = runner.invoke(execute, commands_with_args)

    assert result.exit_code == 1


@pytest.mark.parametrize("commands_with_another_arg", [
    Helper.get_command_results_upload_with_another_argument(),
    Helper.get_command_results_import_with_another_argument(),
    Helper.get_command_testrun_complete_with_another_argument(),
    Helper.get_command_testrun_create_with_another_argument(),
    Helper.get_command_testrun_upload_attachments_with_another_argument()])
def test_run_with_command_and_another_argument(runner, commands_with_another_arg):
    result = runner.invoke(execute, commands_with_another_arg)

    assert result.exit_code == 2
