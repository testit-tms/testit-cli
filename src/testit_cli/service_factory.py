from testit_cli.logger import Logger
from testit_cli.apiclient import ApiClient
from testit_cli.importer import Importer
from testit_cli.parser import Parser
from testit_cli.service import Service
from testit_cli.models.config import Config


class ServiceFactory:
    @classmethod
    def get(cls, config: Config) -> Service:
        Logger.register_logger(config.is_debug)

        api_client = ApiClient(config.url, config.token)
        parser = Parser(config)
        importer = Importer(api_client, config)

        return Service(config, api_client, parser, importer)
