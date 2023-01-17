import argparse

from testit_cli.models.config import Config
from testit_cli.models.mode import Mode


class ArgsParser:
    """Class representing a arguments parser"""

    def __init__(self):
        self.__init_parser()
        self.__add_args()

    def __init_parser(self):
        self.parser = argparse.ArgumentParser(
            prog="testit",
            usage="%(prog)s [options]",
            description="""This tool is the command line wrapper of Test IT
                     allowing you to upload the test results in real time to Test IT""",
        )

    def parse_args(self):
        """Function parses commandline arguments and returns config."""
        args = self.parser.parse_args()
        return Config(
            Mode(args.mode),
            args.url,
            args.token,
            args.project_id,
            args.configuration_id,
            args.testrun_id,
            args.testrun_name,
            args.results,
            args.debug,
            args.output,
        )

    def __add_args(self):
        self.parser.add_argument(
            "-m",
            "--mode",
            action="store",
            choices=["import", "create", "finish", "upload"],
            default="import",
            dest="mode",
            help="Set CLI mode",
        )
        self.parser.add_argument(
            "-u",
            "--url",
            action="store",
            default=None,
            dest="url",
            metavar="https://demo.testit.software",
            help="Set url address of the Test IT instance",
        )
        self.parser.add_argument(
            "-t",
            "--token",
            action="store",
            dest="token",
            metavar="T2lKd2pLZGI4WHRhaVZUejNl",
            help="Set API token",
        )
        self.parser.add_argument(
            "-pi",
            "--project-id",
            action="store",
            dest="project_id",
            metavar="5236eb3f-7c05-46f9-a609-dc0278896464",
            help="Set project id",
        )
        self.parser.add_argument(
            "-ci",
            "--configuration-id",
            action="store",
            dest="configuration_id",
            metavar="15dbb164-c1aa-4cbf-830c-8c01ae14f4fb",
            help="Set configuration id",
        )
        self.parser.add_argument(
            "-ti",
            "--testrun-id",
            action="store",
            dest="testrun_id",
            metavar="3802f329-190c-4617-8bb0-2c3696abeb8f",
            help="Set test run id",
        )
        self.parser.add_argument(
            "-tn",
            "--testrun-name",
            action="store",
            dest="testrun_name",
            metavar="TestRun01",
            help="Set test run name",
        )
        self.parser.add_argument(
            "-r",
            "--results",
            action="store",
            dest="results",
            metavar="DIR",
            default=None,
            help="Set directory with results file",
        )
        self.parser.add_argument(
            "-d",
            "--debug",
            action="store_true",
            dest="debug",
            help="Set debug logs",
        )
        self.parser.add_argument(
            "-o",
            "--output",
            action="store",
            dest="output",
            metavar="FILE",
            default=None,
            help="Set file path for output",
        )
