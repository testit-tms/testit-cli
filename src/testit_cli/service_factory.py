from .logger import Logger
from .apiclient import ApiClient
from .importer import Importer
from .parser import Parser
from .service import Service
from .models.config import Config


class ServiceFactory:
    @classmethod
    def get(cls, config: Config) -> Service:
        Logger.register_logger(config.is_debug)

        api_client = ApiClient(config.url, config.token, config.disable_cert_validation)
        parser = Parser(config)
        importer = Importer(api_client, config)

        return Service(config, api_client, parser, importer)
