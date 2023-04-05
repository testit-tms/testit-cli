import glob
import logging
import os
from xml.dom import minidom

from testit_cli.configurator import Configurator
from testit_cli.models.status import Status
from testit_cli.models.testcase import TestCase


class Parser:
    def __init__(self, config: Configurator):
        self.__path_to_results = config.get_path()
        self.__separator = config.get_separator()
        self.__namespace = config.get_namespace()

    def read_file(self):  # noqa: C901
        results = []
        files = self.__get_files()

        for file in files:

            xml = minidom.parse(file)
            testcases = xml.getElementsByTagName("testcase")

            for elem in testcases:
                name = elem.attributes["name"].value
                duration = float(elem.attributes["time"].value) * 1000 if "time" in elem.attributes else 0

                if self.__separator is not None and self.__separator in elem.attributes["classname"].value:
                    class_name = elem.attributes["classname"].value.split(self.__separator)[-1]
                    name_space = elem.attributes["classname"].value[:-(len(class_name) + 1)]
                else:
                    class_name = elem.attributes["classname"].value
                    name_space = "namespace"

                if self.__namespace is not None:
                    name_space = self.__namespace

                testcase = TestCase(name, name_space, class_name, duration)

                if elem.childNodes is not None:
                    for child in elem.childNodes:
                        if child.nodeName == "error" or child.nodeName == "failure":
                            if "message" in child.attributes:
                                testcase.set_message(child.attributes["message"].value)
                            if child.firstChild is not None:
                                testcase.set_trace(child.firstChild.wholeText)
                            testcase.set_status(Status.FAILED)
                        elif child.nodeName == "skipped":
                            if "message" in child.attributes:
                                testcase.set_message(child.attributes["message"].value)
                            testcase.set_status(Status.SKIPPED)

                results.append(testcase)

        logging.info(
            f"Found {len(files)} result file with a total of {len(results)} tests"
        )

        return results

    def __get_files(self):

        if os.path.isdir(self.__path_to_results):
            return glob.glob(f"{self.__path_to_results}/*.xml")

        files = []

        if os.path.isfile(self.__path_to_results):
            files.append(self.__path_to_results)

        return files
