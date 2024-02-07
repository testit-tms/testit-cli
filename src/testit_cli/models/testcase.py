from datetime import timedelta

from testit_api_client.model.available_test_result_outcome import AvailableTestResultOutcome

from .status import Status


class TestCase:
    __name: str = None
    __name_space: str = None
    __class_name: str = None
    __duration: timedelta = None
    __status: Status = None
    __message: str = None
    __trace: str = None
    __is_flaky: bool = None

    def __init__(self, name, name_space, class_name, duration):
        self.__name = name
        self.__name_space = name_space
        self.__class_name = class_name
        self.__duration = timedelta(seconds=float(duration))
        self.__status = Status.PASSED
        self.__trace = ""

    def get_name(self):
        return self.__name

    def get_name_space(self):
        return self.__name_space

    def get_class_name(self):
        return self.__class_name

    def get_duration(self):
        return self.__duration.total_seconds()

    def get_message(self):
        return self.__message

    def set_message(self, value: str):
        self.__message = value

    def get_trace(self):
        return self.__trace

    def set_trace(self, value: str):
        self.__trace = value

    def get_status(self):
        return AvailableTestResultOutcome(self.__status.value)

    def set_status(self, value: Status):
        self.__status = value

    def get_is_flaky(self) -> bool:
        return self.__is_flaky

    def set_is_flaky(self, value: bool):
        self.__is_flaky = value
