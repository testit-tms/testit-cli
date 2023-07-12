class Helper:
    __URL = "https://demo.testit.software"
    __TOKEN = "T2lKd2pLZGI4WHRhaVZUejNl"
    __UUID = "3802f329-190c-4617-8bb0-2c3696abeb8f"
    __TEST_RUN_NAME = "TestRun01"
    __SEPARATOR = "."
    __DIR_PATH = "DIR"
    __NAMESPACE = "NameSpace01"
    __CLASSNAME = "ClassName01"
    __FILE_PATH = "FILE"

    @classmethod
    def get_input_for_results_import_without_arguments(cls):
        return f"{cls.__URL}\n{cls.__TOKEN}\n{cls.__UUID}\n{cls.__UUID}\n{cls.__DIR_PATH}\n"

    @classmethod
    def get_output_for_results_import_without_arguments(cls):
        return f"Set url: {cls.__URL}\nSet API token: {cls.__TOKEN}\nSet project id: {cls.__UUID}\nSet configuration id: {cls.__UUID}\nSet directory with results: {cls.__DIR_PATH}\n"

    @classmethod
    def get_input_for_results_upload_without_arguments(cls):
        return f"{cls.__URL}\n{cls.__TOKEN}\n{cls.__UUID}\n{cls.__UUID}\n{cls.__DIR_PATH}\n"

    @classmethod
    def get_output_for_results_upload_without_arguments(cls):
        return f"Set url: {cls.__URL}\nSet API token: {cls.__TOKEN}\nSet configuration id: {cls.__UUID}\nSet test run id: {cls.__UUID}\nSet directory with results: {cls.__DIR_PATH}\n"

    @classmethod
    def get_input_for_testrun_create_without_arguments(cls):
        return f"{cls.__URL}\n{cls.__TOKEN}\n{cls.__UUID}\n{cls.__FILE_PATH}\n"

    @classmethod
    def get_output_for_testrun_create_without_arguments(cls):
        return f"Set url: {cls.__URL}\nSet API token: {cls.__TOKEN}\nSet project id: {cls.__UUID}\nSet file path: {cls.__FILE_PATH}\n"

    @classmethod
    def get_input_for_testrun_complete_without_arguments(cls):
        return f"{cls.__URL}\n{cls.__TOKEN}\n{cls.__UUID}\n"

    @classmethod
    def get_output_for_testrun_complete_without_arguments(cls):
        return f"Set url: {cls.__URL}\nSet API token: {cls.__TOKEN}\nSet test run id: {cls.__UUID}\n"

    @classmethod
    def get_command_results_import_with_long_arguments(cls):
        return ["results", "import", "--url", cls.__URL, "--token", cls.__TOKEN, "--project-id", cls.__UUID, "--configuration-id", cls.__UUID, "--results", cls.__DIR_PATH]

    @classmethod
    def get_command_results_import_with_short_arguments(cls):
        return ["results", "import", "-u", cls.__URL, "-t", cls.__TOKEN, "-pi", cls.__UUID, "-ci", cls.__UUID, "-r", cls.__DIR_PATH]

    @classmethod
    def get_command_results_upload_with_long_arguments(cls):
        return ["results", "upload", "--url", cls.__URL, "--token", cls.__TOKEN, "--configuration-id", cls.__UUID, "--testrun-id", cls.__UUID, "--results", cls.__DIR_PATH]

    @classmethod
    def get_command_results_upload_with_short_arguments(cls):
        return ["results", "upload", "-u", cls.__URL, "-t", cls.__TOKEN, "-ci", cls.__UUID, "-ti", cls.__UUID, "-r", cls.__DIR_PATH]

    @classmethod
    def get_command_testrun_create_with_long_arguments(cls):
        return ["testrun", "create", "--url", cls.__URL, "--token", cls.__TOKEN, "--project-id", cls.__UUID, "--output", cls.__FILE_PATH]

    @classmethod
    def get_command_testrun_create_with_short_arguments(cls):
        return ["testrun", "create", "-u", cls.__URL, "-t", cls.__TOKEN, "-pi", cls.__UUID, "-o", cls.__FILE_PATH]

    @classmethod
    def get_command_testrun_complete_with_long_arguments(cls):
        return ["testrun", "complete", "--url", cls.__URL, "--token", cls.__TOKEN, "--testrun-id", cls.__UUID]

    @classmethod
    def get_command_testrun_complete_with_short_arguments(cls):
        return ["testrun", "complete", "-u", cls.__URL, "-t", cls.__TOKEN, "-ti", cls.__UUID]

    @classmethod
    def get_command_results_import_with_all_long_arguments(cls):
        return cls.get_command_results_import_with_long_arguments() + [
            "--testrun-id", cls.__UUID, "--testrun-name", cls.__TEST_RUN_NAME, "--separator", cls.__SEPARATOR, "--namespace", cls.__NAMESPACE, "--classname", cls.__CLASSNAME, "--debug"]

    @classmethod
    def get_command_results_import_with_all_short_arguments(cls):
        return cls.get_command_results_import_with_short_arguments() + ["-ti", cls.__UUID, "-tn", cls.__TEST_RUN_NAME, "-s", cls.__SEPARATOR, "-ns", cls.__NAMESPACE, "-cn", cls.__CLASSNAME, "-d"]

    @classmethod
    def get_command_results_import_with_another_argument(cls):
        return ["results", "import", "--start"]

    @classmethod
    def get_command_results_upload_with_all_long_arguments(cls):
        return cls.get_command_results_upload_with_long_arguments() + ["--separator", cls.__SEPARATOR, "--namespace", cls.__NAMESPACE, "--classname", cls.__CLASSNAME, "--debug"]

    @classmethod
    def get_command_results_upload_with_all_short_arguments(cls):
        return cls.get_command_results_upload_with_short_arguments() + ["-s", cls.__SEPARATOR, "-ns", cls.__NAMESPACE, "-cn", cls.__CLASSNAME, "-d"]

    @classmethod
    def get_command_results_upload_with_another_argument(cls):
        return ["results", "upload", "--start"]

    @classmethod
    def get_command_testrun_create_with_all_long_arguments(cls):
        return cls.get_command_testrun_create_with_long_arguments() + ["--testrun-name", cls.__TEST_RUN_NAME, "--debug"]

    @classmethod
    def get_command_testrun_create_with_all_short_arguments(cls):
        return cls.get_command_testrun_create_with_short_arguments() + ["-tn", cls.__TEST_RUN_NAME, "-d"]

    @classmethod
    def get_command_testrun_create_with_another_argument(cls):
        return ["testrun", "create", "--start"]

    @classmethod
    def get_command_testrun_complete_with_all_long_arguments(cls):
        return cls.get_command_testrun_complete_with_long_arguments() + ["--debug"]

    @classmethod
    def get_command_testrun_complete_with_all_short_arguments(cls):
        return cls.get_command_testrun_complete_with_short_arguments() + ["-d"]

    @classmethod
    def get_command_testrun_complete_with_another_argument(cls):
        return ["testrun", "complete", "--start"]
