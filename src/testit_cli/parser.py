import logging
from xml.dom import minidom

from .models.config import Config
from .models.status import Status
from .models.testcase import TestCase
from .file_worker import FileWorker


class Parser:
    __FAILURE_NODE_NAMES = [
        "error",
        "failure",
        "rerunFailure",
        "rerunError",
        "flakyFailure",
        "flakyError",
        "system-err"]
    __MESSAGE_ATTRIBUTE_NAME = "message"
    __TAGS_OF_TESTS = [
        "testcase",
        "test-case"
    ]

    def __init__(self, config: Config):
        self.__paths_to_results = config.results
        self.__separator = config.separator
        self.__namespace = config.namespace
        self.__classname = config.classname

    def read_file(self):  # noqa: C901
        results = []
        files = []

        for path_to_results in self.__paths_to_results:
            files.extend(FileWorker.get_files(path_to_results, "xml"))

        for file in files:
            xml = minidom.parse(file)
            testcases = self.__get_testcases(xml)

            for elem in testcases:
                name = elem.attributes["name"].value
                duration = float(elem.attributes["time"].value) * 1000 if "time" in elem.attributes else 0
                name_space = "namespace"
                class_name = "classname"

                if self.__separator is not None and self.__separator in elem.attributes["classname"].value:
                    class_name = elem.attributes["classname"].value.split(self.__separator)[-1]
                    name_space = elem.attributes["classname"].value[:-(len(class_name) + 1)]
                elif "classname" in elem.attributes:
                    class_name = elem.attributes["classname"].value

                if self.__namespace is not None:
                    name_space = self.__namespace

                if self.__classname is not None:
                    class_name = self.__classname

                testcase = TestCase(name, name_space, class_name, duration)

                if elem.childNodes is not None:
                    for child in elem.childNodes:
                        if child.attributes and self.__MESSAGE_ATTRIBUTE_NAME in child.attributes:
                            testcase.set_message(child.attributes[self.__MESSAGE_ATTRIBUTE_NAME].value)

                        if child.nodeName == "skipped":
                            testcase.set_status(Status.SKIPPED)

                            continue
                        elif child.nodeName in self.__FAILURE_NODE_NAMES:
                            testcase.set_status(Status.FAILED)

                        testcase.set_trace(
                            testcase.get_trace() + self.__form_trace(child.childNodes))

                results.append(testcase)

        logging.info(
            f"Found {len(files)} result file with a total of {len(results)} tests"
        )

        return results

    @classmethod
    def __form_trace(cls, child_nodes: list) -> str:
        trace = ""

        for child in child_nodes:
            if "data" in dir(child) and child.data.replace("\t", "").replace("\n", "") != "":
                trace += child.data + "\n"
            if any(child.childNodes):
                trace += cls.__form_trace(child.childNodes)

        return trace

    @classmethod
    def __get_testcases(cls, xml) -> list:
        for tag in cls.__TAGS_OF_TESTS:
            testcases = xml.getElementsByTagName(tag)

            if testcases:
                return testcases

        return []
