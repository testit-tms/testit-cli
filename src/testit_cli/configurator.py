"""The module provides functionality for working with the config"""
import os
import re

import validators

from testit_cli.args_parser import ArgsParser
from testit_cli.models.config import Config
from testit_cli.models.mode import Mode


class Configurator:
    """Class representing a configurator"""

    __config: Config = None
    __env_prefix: str = "TMS"

    __path_to_results = None
    __path_to_config = None
    __specified_testrun = None

    def __init__(self, parser: ArgsParser):
        self.__config = parser.parse_args()
        env = self.__load_env_config()
        self.__merge_config(env)
        self.__validate()

    def get_path(self):
        """Function returns path of result files."""
        return self.__config.results

    def get_url(self):
        """Function returns TMS url."""
        if self.__config.url.endswith("/"):
            return self.__config.url[:-1]
        return self.__config.url

    def get_private_token(self):
        """Function returns private token."""
        return self.__config.token

    def get_project_id(self):
        """Function returns project id."""
        return self.__config.project_id

    def set_project_id(self, value: str):
        """Function sets project id."""
        self.__config.project_id = value

    def get_configuration_id(self):
        """Function returns configuration id."""
        return self.__config.configuration_id

    def get_testrun_id(self):
        """Function returns testrun id."""
        return self.__config.testrun_id

    def set_testrun_id(self, value: str):
        """Function sets testrun id."""
        self.__config.testrun_id = value

    def get_testrun_name(self):
        """Function returns testrun name."""
        return self.__config.testrun_name

    def get_mode(self):
        """Function returns mode."""
        return self.__config.mode

    def get_output(self):
        """Function returns output file path."""
        return self.__config.output

    def is_debug(self):
        """Function returns debug mode."""
        return self.__config.is_debug

    def __validate(self):  # noqa: C901
        if self.__config.mode is None:
            raise ValueError("Mode is not valid!")

        if self.__config.url is None or not validators.url(self.__config.url):
            raise ValueError("Url is not valid!")

        if self.__config.token is None:
            raise ValueError("Token is not valid!")

        if self.__config.mode in [Mode.IMPORT, Mode.CREATE_TEST_RUN]:
            if self.__config.project_id is None or not self.__validate_guid(
                self.__config.project_id
            ):
                raise ValueError("Project id is not valid!")

        if self.__config.mode in [Mode.IMPORT, Mode.UPLOAD]:
            if self.__config.configuration_id is None or not self.__validate_guid(
                self.__config.configuration_id
            ):
                raise ValueError("Configuration id is not valid!")
            if self.__config.results is None:
                raise ValueError("Results is not valid!")

        if self.__config.mode in [Mode.FINISHED_TEST_RUN, Mode.UPLOAD]:
            if self.__config.testrun_id is None:
                raise ValueError("Testrun id is not valid!")

        if self.__config.mode is Mode.CREATE_TEST_RUN:
            if self.__config.output is None:
                raise ValueError("Output file is not valid!")

    def __load_env_config(self):
        env_properties = {}

        if f"{self.__env_prefix}_URL" in os.environ.keys():
            env_properties["url"] = os.environ.get(f"{self.__env_prefix}_URL")

        if f"{self.__env_prefix}_TOKEN" in os.environ.keys():
            env_properties["token"] = os.environ.get(f"{self.__env_prefix}_TOKEN")

        if f"{self.__env_prefix}_PROJECT_ID" in os.environ.keys():
            env_properties["project_id"] = os.environ.get(
                f"{self.__env_prefix}_PROJECT_ID"
            )

        if f"{self.__env_prefix}_CONFIGURATION_ID" in os.environ.keys():
            env_properties["configuration_id"] = os.environ.get(
                f"{self.__env_prefix}_CONFIGURATION_ID"
            )

        if f"{self.__env_prefix}_TEST_RUN_ID" in os.environ.keys():
            env_properties["testrun_id"] = os.environ.get(
                f"{self.__env_prefix}_TEST_RUN_ID"
            )

        if f"{self.__env_prefix}_TEST_RUN_NAME" in os.environ.keys():
            env_properties["testrun_name"] = os.environ.get(
                f"{self.__env_prefix}_TEST_RUN_NAME"
            )

        return env_properties

    def __merge_config(self, env: dict):
        for k in env.keys():
            if env[k] is not None:
                setattr(self.__config, k, env[k])

    @staticmethod
    def __validate_guid(value: str):
        return re.fullmatch(
            r"[a-zA-Z\d]{8}-[a-zA-Z\d]{4}-[a-zA-Z\d]{4}-[a-zA-Z\d]{4}-[a-zA-Z\d]{12}",
            value,
        )
