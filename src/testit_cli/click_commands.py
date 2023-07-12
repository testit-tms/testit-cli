import click

from testit_cli.models.config import Config
from testit_cli.service_factory import ServiceFactory


@click.group()
def execute():
    pass


@execute.group()
def results():
    pass


@results.command("upload")
@click.option("-u", "--url", type=str, prompt="Set url", help="Set url address of the Test IT instance (https://demo.testit.software)")
@click.option("-t", "--token", type=str, prompt="Set API token", help="Set API token (T2lKd2pLZGI4WHRhaVZUejNl)")
@click.option("-ci", "--configuration-id", type=str, prompt="Set configuration id", help="Set configuration id (15dbb164-c1aa-4cbf-830c-8c01ae14f4fb)")
@click.option("-ti", "--testrun-id", type=str, prompt="Set test run id", help="Set test run id (3802f329-190c-4617-8bb0-2c3696abeb8f)")
@click.option("-s", "--separator", type=str, help="Separate the classname value in the results into namespace and classname (.)", default=None)
@click.option("-ns", "--namespace", type=str, help="Set namespace (NameSpace01)", default=None)
@click.option("-cn", "--classname", type=str, help="Set classname (ClassName01)", default=None)
@click.option("-r", "--results", type=str, prompt="Set directory with results", help="Set directory with results file (DIR)")
@click.option("-d", "--debug", is_flag=True, help="Set debug logs")
def upload_results(url, token, configuration_id, testrun_id, separator, namespace, classname, results, debug):
    config = Config(url, token, "", configuration_id, testrun_id, "", separator, namespace, classname, results, debug, "")
    service = ServiceFactory().get(config)

    service.upload_results()


@results.command("import")
@click.option("-u", "--url", type=str, prompt="Set url", help="Set url address of the Test IT instance (https://demo.testit.software)")
@click.option("-t", "--token", type=str, prompt="Set API token", help="Set API token (T2lKd2pLZGI4WHRhaVZUejNl)")
@click.option("-pi", "--project-id", type=str, prompt="Set project id", help="Set project id (5236eb3f-7c05-46f9-a609-dc0278896464)")
@click.option("-ci", "--configuration-id", type=str, prompt="Set configuration id", help="Set configuration id (15dbb164-c1aa-4cbf-830c-8c01ae14f4fb)")
@click.option("-ti", "--testrun-id", type=str, help="Set test run id (3802f329-190c-4617-8bb0-2c3696abeb8f)", default=None)
@click.option("-tn", "--testrun-name", type=str, help="Set test run name (TestRun01)", default=None)
@click.option("-s", "--separator", type=str, help="Separate the classname value in the results into namespace and classname (.)", default=None)
@click.option("-ns", "--namespace", type=str, help="Set namespace (NameSpace01)", default=None)
@click.option("-cn", "--classname", type=str, help="Set classname (ClassName01)", default=None)
@click.option("-r", "--results", type=str, prompt="Set directory with results", help="Set directory with results file (DIR)")
@click.option("-d", "--debug", is_flag=True, help="Set debug logs")
def import_results(url, token, project_id, configuration_id, testrun_id, testrun_name, separator, namespace, classname, results, debug):
    config = Config(url, token, project_id, configuration_id, testrun_id, testrun_name, separator, namespace, classname, results, debug, "")
    service = ServiceFactory().get(config)

    service.import_results()


@execute.group()
def testrun():
    pass


@testrun.command("create")
@click.option("-u", "--url", type=str, prompt="Set url", help="Set url address of the Test IT instance (https://demo.testit.software)")
@click.option("-t", "--token", type=str, prompt="Set API token", help="Set API token (T2lKd2pLZGI4WHRhaVZUejNl)")
@click.option("-pi", "--project-id", type=str, prompt="Set project id", help="Set project id (5236eb3f-7c05-46f9-a609-dc0278896464)")
@click.option("-tn", "--testrun-name", type=str, help="Set test run name (TestRun01)", default=None)
@click.option("-o", "--output", type=str, prompt="Set file path", help="Set file path for output (FILE)")
@click.option("-d", "--debug", is_flag=True, help="Set debug logs")
def create_testrun(url, token, project_id, testrun_name, output, debug):
    config = Config(url, token, project_id, "", "", testrun_name, "", "", "", "", debug, output)
    service = ServiceFactory().get(config)

    service.create_testrun()


@testrun.command("complete")
@click.option("-u", "--url", type=str, prompt="Set url", help="Set url address of the Test IT instance (https://demo.testit.software)")
@click.option("-t", "--token", type=str, prompt="Set API token", help="Set API token (T2lKd2pLZGI4WHRhaVZUejNl)")
@click.option("-ti", "--testrun-id", type=str, prompt="Set test run id", help="Set test run id (3802f329-190c-4617-8bb0-2c3696abeb8f)")
@click.option("-d", "--debug", is_flag=True, help="Set debug logs")
def complete_testrun(url, token, testrun_id, debug):
    config = Config(url, token, "", "", testrun_id, "", "", "", "", "", debug, "")
    service = ServiceFactory().get(config)

    service.finished_testrun()
