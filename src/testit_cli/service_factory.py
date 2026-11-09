from .apiclient import ApiClient
from .autotests_filter import AutotestsFilter
from .importer import Importer
from .logger import Logger
from .models.config import Config
from .parser import Parser
from .service import Service
from .v2_client import V2Client


class ServiceFactory:
    @staticmethod
    def get(config: Config) -> Service:
        Logger.register_logger(config.is_debug)

        api_client = ApiClient(config.url, config.token, config.disable_cert_validation)
        v2_client = V2Client(config.url, config.token, config.disable_cert_validation)
        parser = Parser(config)
        importer = Importer(api_client, config)
        autotests_filter = AutotestsFilter(api_client, config)

        return Service(config, api_client, parser, importer, autotests_filter, v2_client)
