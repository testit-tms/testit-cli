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
    def get_command_results_import_with_long_arguments_without_url_argument(cls):
        return ["results", "import", "--token", cls.__TOKEN, "--project-id", cls.__UUID, "--configuration-id", cls.__UUID, "--results", cls.__DIR_PATH]

    @classmethod
    def get_command_results_import_with_short_arguments_without_url_argument(cls):
        return ["results", "import", "-t", cls.__TOKEN, "-pi", cls.__UUID, "-ci", cls.__UUID, "-r", cls.__DIR_PATH]

    @classmethod
    def get_output_for_results_import_without_url_argument(cls):
        return "results import --help' for help.\n\nError: Missing option '-u' / '--url'.\n"

    @classmethod
    def get_command_results_import_with_long_arguments_without_token_argument(cls):
        return ["results", "import", "--url", cls.__URL, "--project-id", cls.__UUID, "--configuration-id", cls.__UUID, "--results", cls.__DIR_PATH]

    @classmethod
    def get_command_results_import_with_short_arguments_without_token_argument(cls):
        return ["results", "import", "-u", cls.__URL, "-pi", cls.__UUID, "-ci", cls.__UUID, "-r", cls.__DIR_PATH]

    @classmethod
    def get_output_for_results_import_without_token_argument(cls):
        return "results import --help' for help.\n\nError: Missing option '-t' / '--token'.\n"

    @classmethod
    def get_command_results_import_with_long_arguments_without_project_id_argument(cls):
        return ["results", "import", "--url", cls.__URL, "--token", cls.__TOKEN, "--configuration-id", cls.__UUID, "--results", cls.__DIR_PATH]

    @classmethod
    def get_command_results_import_with_short_arguments_without_project_id_argument(cls):
        return ["results", "import", "-u", cls.__URL, "-t", cls.__TOKEN, "-ci", cls.__UUID, "-r", cls.__DIR_PATH]

    @classmethod
    def get_output_for_results_import_without_project_id_argument(cls):
        return "results import --help' for help.\n\nError: Missing option '-pi' / '--project-id'.\n"

    @classmethod
    def get_command_results_import_with_long_arguments_without_configuration_id_argument(cls):
        return ["results", "import", "--url", cls.__URL, "--token", cls.__TOKEN, "--project-id", cls.__UUID, "--results", cls.__DIR_PATH]

    @classmethod
    def get_command_results_import_with_short_arguments_without_configuration_id_argument(cls):
        return ["results", "import", "-u", cls.__URL, "-t", cls.__TOKEN, "-pi", cls.__UUID, "-r", cls.__DIR_PATH]

    @classmethod
    def get_output_for_results_import_without_configuration_id_argument(cls):
        return "results import --help' for help.\n\nError: Missing option '-ci' / '--configuration-id'.\n"

    @classmethod
    def get_command_results_import_with_long_arguments_without_results_argument(cls):
        return ["results", "import", "--url", cls.__URL, "--token", cls.__TOKEN, "--project-id", cls.__UUID, "--configuration-id", cls.__UUID]

    @classmethod
    def get_command_results_import_with_short_arguments_without_results_argument(cls):
        return ["results", "import", "-u", cls.__URL, "-t", cls.__TOKEN, "-pi", cls.__UUID, "-ci", cls.__UUID]

    @classmethod
    def get_output_for_results_import_without_results_argument(cls):
        return "results import --help' for help.\n\nError: Missing option '-r' / '--results'.\n"

    @classmethod
    def get_command_results_upload_with_long_arguments_without_url_argument(cls):
        return ["results", "upload", "--token", cls.__TOKEN, "--testrun-id", cls.__UUID, "--configuration-id", cls.__UUID, "--results", cls.__DIR_PATH]

    @classmethod
    def get_command_results_upload_with_short_arguments_without_url_argument(cls):
        return ["results", "upload", "-t", cls.__TOKEN, "-ti", cls.__UUID, "-ci", cls.__UUID, "-r", cls.__DIR_PATH]

    @classmethod
    def get_output_for_results_upload_without_url_argument(cls):
        return "results upload --help' for help.\n\nError: Missing option '-u' / '--url'.\n"

    @classmethod
    def get_command_results_upload_with_long_arguments_without_token_argument(cls):
        return ["results", "upload", "--url", cls.__URL, "--testrun-id", cls.__UUID, "--configuration-id", cls.__UUID,
                "--results", cls.__DIR_PATH]

    @classmethod
    def get_command_results_upload_with_short_arguments_without_token_argument(cls):
        return ["results", "upload", "-u", cls.__URL, "-ti", cls.__UUID, "-ci", cls.__UUID, "-r", cls.__DIR_PATH]

    @classmethod
    def get_output_for_results_upload_without_token_argument(cls):
        return "results upload --help' for help.\n\nError: Missing option '-t' / '--token'.\n"

    @classmethod
    def get_command_results_upload_with_long_arguments_without_testrun_id_argument(cls):
        return ["results", "upload", "--url", cls.__URL, "--token", cls.__TOKEN, "--configuration-id", cls.__UUID,
                "--results", cls.__DIR_PATH]

    @classmethod
    def get_command_results_upload_with_short_arguments_without_testrun_id_argument(cls):
        return ["results", "upload", "-u", cls.__URL, "-t", cls.__TOKEN, "-ci", cls.__UUID, "-r", cls.__DIR_PATH]

    @classmethod
    def get_output_for_results_upload_without_testrun_id_argument(cls):
        return "results upload --help' for help.\n\nError: Missing option '-ti' / '--testrun-id'.\n"

    @classmethod
    def get_command_results_upload_with_long_arguments_without_configuration_id_argument(cls):
        return ["results", "upload", "--url", cls.__URL, "--token", cls.__TOKEN, "--testrun-id", cls.__UUID, "--results", cls.__DIR_PATH]

    @classmethod
    def get_command_results_upload_with_short_arguments_without_configuration_id_argument(cls):
        return ["results", "upload", "-u", cls.__URL, "-t", cls.__TOKEN, "-ti", cls.__UUID, "-r", cls.__DIR_PATH]

    @classmethod
    def get_output_for_results_upload_without_configuration_id_argument(cls):
        return "results upload --help' for help.\n\nError: Missing option '-ci' / '--configuration-id'.\n"

    @classmethod
    def get_command_results_upload_with_long_arguments_without_results_argument(cls):
        return ["results", "upload", "--url", cls.__URL, "--token", cls.__TOKEN, "--testrun-id", cls.__UUID, "--configuration-id", cls.__UUID]

    @classmethod
    def get_command_results_upload_with_short_arguments_without_results_argument(cls):
        return ["results", "upload", "-u", cls.__URL, "-t", cls.__TOKEN, "-ti", cls.__UUID, "-ci", cls.__UUID]

    @classmethod
    def get_output_for_results_upload_without_results_argument(cls):
        return "results upload --help' for help.\n\nError: Missing option '-r' / '--results'.\n"

    @classmethod
    def get_command_testrun_create_with_long_arguments_without_url_argument(cls):
        return ["testrun", "create", "--token", cls.__TOKEN, "--project-id", cls.__UUID, "--output", cls.__FILE_PATH]

    @classmethod
    def get_command_testrun_create_with_short_arguments_without_url_argument(cls):
        return ["testrun", "create", "-t", cls.__TOKEN, "-pi", cls.__UUID, "-o", cls.__FILE_PATH]

    @classmethod
    def get_output_for_testrun_create_without_url_argument(cls):
        return "testrun create --help' for help.\n\nError: Missing option '-u' / '--url'.\n"

    @classmethod
    def get_command_testrun_create_with_long_arguments_without_token_argument(cls):
        return ["testrun", "create", "--url", cls.__URL, "--project-id", cls.__UUID, "--output", cls.__FILE_PATH]

    @classmethod
    def get_command_testrun_create_with_short_arguments_without_token_argument(cls):
        return ["testrun", "create", "-u", cls.__URL, "-pi", cls.__UUID, "-o", cls.__FILE_PATH]

    @classmethod
    def get_output_for_testrun_create_without_token_argument(cls):
        return "testrun create --help' for help.\n\nError: Missing option '-t' / '--token'.\n"

    @classmethod
    def get_command_testrun_create_with_long_arguments_without_project_id_argument(cls):
        return ["testrun", "create", "--url", cls.__URL, "--token", cls.__TOKEN, "--output", cls.__FILE_PATH]

    @classmethod
    def get_command_testrun_create_with_short_arguments_without_project_id_argument(cls):
        return ["testrun", "create", "-u", cls.__URL, "-t", cls.__TOKEN, "-o", cls.__FILE_PATH]

    @classmethod
    def get_output_for_testrun_create_without_project_id_argument(cls):
        return "testrun create --help' for help.\n\nError: Missing option '-pi' / '--project-id'.\n"

    @classmethod
    def get_command_testrun_create_with_long_arguments_without_output_argument(cls):
        return ["testrun", "create", "--url", cls.__URL, "--token", cls.__TOKEN, "--project-id", cls.__UUID]

    @classmethod
    def get_command_testrun_create_with_short_arguments_without_output_argument(cls):
        return ["testrun", "create", "-u", cls.__URL, "-t", cls.__TOKEN, "-pi", cls.__UUID]

    @classmethod
    def get_output_for_testrun_create_without_output_argument(cls):
        return "testrun create --help' for help.\n\nError: Missing option '-o' / '--output'.\n"

    @classmethod
    def get_command_testrun_complete_with_long_arguments_without_url_argument(cls):
        return ["testrun", "complete", "--token", cls.__TOKEN, "--testrun-id", cls.__UUID]

    @classmethod
    def get_command_testrun_complete_with_short_arguments_without_url_argument(cls):
        return ["testrun", "complete", "-t", cls.__TOKEN, "-ti", cls.__UUID]

    @classmethod
    def get_output_for_testrun_complete_without_url_argument(cls):
        return "testrun complete --help' for help.\n\nError: Missing option '-u' / '--url'.\n"

    @classmethod
    def get_command_testrun_complete_with_long_arguments_without_token_argument(cls):
        return ["testrun", "complete", "--url", cls.__URL, "--testrun-id", cls.__UUID]

    @classmethod
    def get_command_testrun_complete_with_short_arguments_without_token_argument(cls):
        return ["testrun", "complete", "-u", cls.__URL, "-ti", cls.__UUID]

    @classmethod
    def get_output_for_testrun_complete_without_token_argument(cls):
        return "testrun complete --help' for help.\n\nError: Missing option '-t' / '--token'.\n"

    @classmethod
    def get_command_testrun_complete_with_long_arguments_without_testrun_id_argument(cls):
        return ["testrun", "complete", "--url", cls.__URL, "--token", cls.__TOKEN]

    @classmethod
    def get_command_testrun_complete_with_short_arguments_without_testrun_id_argument(cls):
        return ["testrun", "complete", "-u", cls.__URL, "-t", cls.__TOKEN]

    @classmethod
    def get_output_for_testrun_complete_without_testrun_id_argument(cls):
        return "testrun complete --help' for help.\n\nError: Missing option '-ti' / '--testrun-id'.\n"

    @classmethod
    def get_command_testrun_upload_attachments_with_long_arguments_without_url_argument(cls):
        return ["testrun", "upload_attachments", "--token", cls.__TOKEN, "--testrun-id", cls.__UUID]

    @classmethod
    def get_command_testrun_upload_attachments_with_short_arguments_without_url_argument(cls):
        return ["testrun", "upload_attachments", "-t", cls.__TOKEN, "-ti", cls.__UUID]

    @classmethod
    def get_output_for_testrun_upload_attachments_without_url_argument(cls):
        return "testrun upload_attachments --help' for help.\n\nError: Missing option '-u' / '--url'.\n"

    @classmethod
    def get_command_testrun_upload_attachments_with_long_arguments_without_token_argument(cls):
        return ["testrun", "upload_attachments", "--url", cls.__URL, "--testrun-id", cls.__UUID]

    @classmethod
    def get_command_testrun_upload_attachments_with_short_arguments_without_token_argument(cls):
        return ["testrun", "upload_attachments", "-u", cls.__URL, "-ti", cls.__UUID]

    @classmethod
    def get_output_for_testrun_upload_attachments_without_token_argument(cls):
        return "testrun upload_attachments --help' for help.\n\nError: Missing option '-t' / '--token'.\n"

    @classmethod
    def get_command_testrun_upload_attachments_with_long_arguments_without_testrun_id_argument(cls):
        return ["testrun", "upload_attachments", "--url", cls.__URL, "--token", cls.__TOKEN]

    @classmethod
    def get_command_testrun_upload_attachments_with_short_arguments_without_testrun_id_argument(cls):
        return ["testrun", "upload_attachments", "-u", cls.__URL, "-t", cls.__TOKEN]

    @classmethod
    def get_output_for_testrun_upload_attachments_without_testrun_id_argument(cls):
        return "testrun upload_attachments --help' for help.\n\nError: Missing option '-ti' / '--testrun-id'.\n"

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
    def get_command_testrun_upload_attachments_with_long_arguments(cls):
        return ["testrun", "upload_attachments", "--url", cls.__URL, "--token", cls.__TOKEN, "--testrun-id", cls.__UUID, "--attachments", cls.__DIR_PATH]

    @classmethod
    def get_command_testrun_upload_attachments_with_short_arguments(cls):
        return ["testrun", "upload_attachments", "-u", cls.__URL, "-t", cls.__TOKEN, "-ti", cls.__UUID, "-a", cls.__DIR_PATH]

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
    def get_command_testrun_upload_attachments_with_all_long_arguments(cls):
        return cls.get_command_testrun_upload_attachments_with_long_arguments() + ["--debug"]

    @classmethod
    def get_command_testrun_upload_attachments_with_all_short_arguments(cls):
        return cls.get_command_testrun_upload_attachments_with_short_arguments() + ["-d"]

    @classmethod
    def get_command_testrun_complete_with_another_argument(cls):
        return ["testrun", "complete", "--start"]

    @classmethod
    def get_command_testrun_upload_attachments_with_another_argument(cls):
        return ["testrun", "upload_attachments", "--start"]
