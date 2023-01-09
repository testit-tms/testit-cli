from args_parser import ArgsParser
from logger import Logger

from .apiclient import ApiClient
from .configurator import Configurator
from .importer import Importer
from .parser import Parser


def console_main():
    arg_parser = ArgsParser()
    config = Configurator(arg_parser)

    Logger.register_logger(config.is_debug())

    if config.get_path() is None:
        return

    parser = Parser(config)
    api_client = ApiClient(config.get_url(), config.get_private_token())
    importer = Importer(parser, api_client, config)

    importer.send_results()


if __name__ == "__main__":
    console_main()
