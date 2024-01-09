import click

from itertools import chain

from .models.config import Config
from .service_factory import ServiceFactory
from .validation import validate_uuid, validate_url


@click.group()
def execute():
    pass


@execute.group()
def results():
    """Uploading the test results"""
    pass


class ExtraArgsForOption(click.Option):
    def __init__(self, *args, **kwargs):
        self.save_other_options = kwargs.pop('save_other_options', True)
        nargs = kwargs.pop('nargs', -1)
        assert nargs == -1, 'nargs, if set, must be -1 not {}'.format(nargs)
        super(ExtraArgsForOption, self).__init__(*args, **kwargs)
        self._previous_parser_process = None
        self._eat_all_parser = None

    def add_to_parser(self, parser, ctx):

        def parser_process(value, state):
            # method to hook to the parser.process
            done = False
            value = [value]
            if self.save_other_options:
                # grab everything up to the next option
                while state.rargs and not done:
                    for prefix in self._eat_all_parser.prefixes:
                        if state.rargs[0].startswith(prefix):
                            done = True
                    if not done:
                        value.append(state.rargs.pop(0))
            else:
                # grab everything remaining
                value += state.rargs
                state.rargs[:] = []
            value = tuple(value)

            # call the actual process
            self._previous_parser_process(value, state)

        retval = super(ExtraArgsForOption, self).add_to_parser(parser, ctx)
        for name in self.opts:
            our_parser = parser._long_opt.get(name) or parser._short_opt.get(name)
            if our_parser:
                self._eat_all_parser = our_parser
                self._previous_parser_process = our_parser.process
                our_parser.process = parser_process
                break
        return retval


@results.command("upload")
@click.option("-u", "--url", type=str, envvar='TMS_URL', required=True, help="Set url address of the Test IT instance (https://demo.testit.software)", callback=validate_url)
@click.option("-t", "--token", type=str, envvar='TMS_TOKEN', required=True, help="Set API token (T2lKd2pLZGI4WHRhaVZUejNl)")
@click.option("-ci", "--configuration-id", type=str, envvar='TMS_CONFIGURATION_ID', required=True, help="Set configuration id (15dbb164-c1aa-4cbf-830c-8c01ae14f4fb)", callback=validate_uuid)
@click.option("-ti", "--testrun-id", type=str, envvar='TMS_TEST_RUN_ID', required=True, help="Set test run id (3802f329-190c-4617-8bb0-2c3696abeb8f)", callback=validate_uuid)
@click.option("-s", "--separator", type=str, help="Separate the classname value in the results into namespace and classname (.)", default=None)
@click.option("-ns", "--namespace", type=str, help="Set namespace (NameSpace01)", default=None)
@click.option("-cn", "--classname", type=str, help="Set classname (ClassName01)", default=None)
@click.option("-r", "--results", multiple=True, type=list, required=True, help="Set directory with results file (DIR)", cls=ExtraArgsForOption)
@click.option("-a", "--attachments", multiple=True, type=list, help="Path to attachments for test run (multiple)", default=[], cls=ExtraArgsForOption)
@click.option("-d", "--debug", is_flag=True, help="Set debug logs")
@click.option("-dcv", "--disable-cert-validation", is_flag=True, help="Disables certificate validation")
def upload_results(url, token, configuration_id, testrun_id, separator, namespace, classname, results, debug, attachments, disable_cert_validation):
    """Uploading results from different streams"""
    config = Config(url, token, "", configuration_id, testrun_id, "", separator, namespace, classname, list(chain.from_iterable(results)), debug, "", list(chain.from_iterable(attachments)), disable_cert_validation)
    service = ServiceFactory().get(config)

    service.upload_results()


@results.command("import")
@click.option("-u", "--url", type=str, envvar='TMS_URL', required=True, help="Set url address of the Test IT instance (https://demo.testit.software)", callback=validate_url)
@click.option("-t", "--token", type=str, envvar='TMS_TOKEN', required=True, help="Set API token (T2lKd2pLZGI4WHRhaVZUejNl)")
@click.option("-pi", "--project-id", type=str, envvar='TMS_PROJECT_ID', required=True, help="Set project id (5236eb3f-7c05-46f9-a609-dc0278896464)", callback=validate_uuid)
@click.option("-ci", "--configuration-id", type=str, envvar='TMS_CONFIGURATION_ID', required=True, help="Set configuration id (15dbb164-c1aa-4cbf-830c-8c01ae14f4fb)", callback=validate_uuid)
@click.option("-ti", "--testrun-id", type=str, envvar='TMS_TEST_RUN_ID', help="Set test run id (3802f329-190c-4617-8bb0-2c3696abeb8f)", default=None, callback=validate_uuid)
@click.option("-tn", "--testrun-name", type=str, envvar='TMS_TEST_RUN_NAME', help="Set test run name (TestRun01)", default=None)
@click.option("-s", "--separator", type=str, help="Separate the classname value in the results into namespace and classname (.)", default=None)
@click.option("-ns", "--namespace", type=str, help="Set namespace (NameSpace01)", default=None)
@click.option("-cn", "--classname", type=str, help="Set classname (ClassName01)", default=None)
@click.option("-r", "--results", multiple=True, type=list, required=True, help="Set directory with results file (DIR)", cls=ExtraArgsForOption)
@click.option("-a", "--attachments", multiple=True, type=list, help="Path to attachments for test run (multiple)", default=[], cls=ExtraArgsForOption)
@click.option("-d", "--debug", is_flag=True, help="Set debug logs")
@click.option("-dcv", "--disable-cert-validation", is_flag=True, help="Disables certificate validation")
def import_results(url, token, project_id, configuration_id, testrun_id, testrun_name, separator, namespace, classname, results, debug, attachments, disable_cert_validation):
    """Uploading the first test results"""
    if testrun_id is not None and testrun_name is not None:
        click.echo("Illegal usage: `{}` are mutually exclusive arguments.".format(', '.join(["--testrun-id", "--testrun-name"])), err=True)

    config = Config(url, token, project_id, configuration_id, testrun_id, testrun_name, separator, namespace, classname, list(chain.from_iterable(results)), debug, "", list(chain.from_iterable(attachments)), disable_cert_validation)
    service = ServiceFactory().get(config)

    service.import_results()


@execute.group()
def testrun():
    """Working with the test run"""
    pass


@testrun.command("create")
@click.option("-u", "--url", type=str, envvar='TMS_URL', required=True, help="Set url address of the Test IT instance (https://demo.testit.software)", callback=validate_url)
@click.option("-t", "--token", type=str, envvar='TMS_TOKEN', required=True, help="Set API token (T2lKd2pLZGI4WHRhaVZUejNl)")
@click.option("-pi", "--project-id", type=str, envvar='TMS_PROJECT_ID', required=True, help="Set project id (5236eb3f-7c05-46f9-a609-dc0278896464)", callback=validate_uuid)
@click.option("-tn", "--testrun-name", type=str, envvar='TMS_TEST_RUN_NAME', help="Set test run name (TestRun01)", default=None)
@click.option("-o", "--output", type=str, required=True, help="Set file path for output (FILE)")
@click.option("-a", "--attachments", multiple=True, type=list, help="Path to attachments for test run (multiple)", default=[], cls=ExtraArgsForOption)
@click.option("-d", "--debug", is_flag=True, help="Set debug logs")
@click.option("-dcv", "--disable-cert-validation", is_flag=True, help="Disables certificate validation")
def create_test_run(url, token, project_id, testrun_name, output, debug, attachments, disable_cert_validation):
    """Creating a new test run"""
    config = Config(url, token, project_id, "", "", testrun_name, "", "", "", [], debug, output, list(chain.from_iterable(attachments)), disable_cert_validation)
    service = ServiceFactory().get(config)

    service.create_test_run()


@testrun.command("complete")
@click.option("-u", "--url", type=str, envvar='TMS_URL', required=True, help="Set url address of the Test IT instance (https://demo.testit.software)", callback=validate_url)
@click.option("-t", "--token", type=str, envvar='TMS_TOKEN', required=True, help="Set API token (T2lKd2pLZGI4WHRhaVZUejNl)")
@click.option("-ti", "--testrun-id", type=str, envvar='TMS_TEST_RUN_ID', required=True, help="Set test run id (3802f329-190c-4617-8bb0-2c3696abeb8f)", callback=validate_uuid)
@click.option("-a", "--attachments", multiple=True, type=list, help="Path to attachments for test run (multiple)", default=[], cls=ExtraArgsForOption)
@click.option("-d", "--debug", is_flag=True, help="Set debug logs")
@click.option("-dcv", "--disable-cert-validation", is_flag=True, help="Disables certificate validation")
def complete_test_run(url, token, testrun_id, debug, attachments, disable_cert_validation):
    """Completing the test run"""
    config = Config(url, token, "", "", testrun_id, "", "", "", "", [], debug, "", list(chain.from_iterable(attachments)), disable_cert_validation)
    service = ServiceFactory().get(config)

    service.finished_test_run()


@testrun.command("upload_attachments")
@click.option("-u", "--url", type=str, envvar='TMS_URL', required=True, help="Set url address of the Test IT instance (https://demo.testit.software)", callback=validate_url)
@click.option("-t", "--token", type=str, envvar='TMS_TOKEN', required=True, help="Set API token (T2lKd2pLZGI4WHRhaVZUejNl)")
@click.option("-ti", "--testrun-id", type=str, envvar='TMS_TEST_RUN_ID', required=True, help="Set test run id (3802f329-190c-4617-8bb0-2c3696abeb8f)", callback=validate_uuid)
@click.option("-a", "--attachments", multiple=True, type=list, required=True, help="Path to attachments for test run (multiple)", default=[], cls=ExtraArgsForOption)
@click.option("-d", "--debug", is_flag=True, help="Set debug logs")
@click.option("-dcv", "--disable-cert-validation", is_flag=True, help="Disables certificate validation")
def upload_attachments_for_test_run(url, token, testrun_id, debug, attachments, disable_cert_validation):
    """Uploading attachments for the test run"""
    config = Config(url, token, "", "", testrun_id, "", "", "", "", [], debug, "", list(chain.from_iterable(attachments)), disable_cert_validation)
    service = ServiceFactory().get(config)

    service.upload_attachments_for_test_run()
