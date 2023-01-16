from testit_cli.parser import Parser

from testit_cli.apiclient import ApiClient
from testit_cli.args_parser import ArgsParser
from testit_cli.configurator import Configurator
from testit_cli.importer import Importer
from testit_cli.logger import Logger
from testit_cli.models.mode import Mode
from testit_cli.service import Service


def console_main():
    arg_parser = ArgsParser()
    config = Configurator(arg_parser)

    Logger.register_logger(config.is_debug())

    api_client = ApiClient(config.get_url(), config.get_private_token())
    parser = Parser(config)
    importer = Importer(api_client, config)
    service = Service(config, api_client, parser, importer)

    mode = config.get_mode()
    if mode is Mode.IMPORT:
        service.import_results()

    elif mode is Mode.CREATE_TEST_RUN:
        service.create_testrun()

    elif mode is Mode.FINISHED_TEST_RUN:
        service.finished_testrun()

    elif mode is Mode.UPLOAD:
        service.upload_results()


if __name__ == "__main__":
    console_main()
