from datetime import timedelta
from typing import Optional

from testit_api_client.models import AvailableTestResultOutcome

from .status import Status


class TestCase:
    __name: Optional[str] = None
    __name_space: Optional[str] = None
    __class_name: Optional[str] = None
    __duration: Optional[timedelta] = None
    __status: Optional[Status] = None
    __message: Optional[str] = None
    __trace: Optional[str] = None
    __is_flaky: Optional[bool] = None

    def __init__(self, name, name_space, class_name, duration):
        self.__name = name
        self.__name_space = name_space
        self.__class_name = class_name
        self.__duration = timedelta(seconds=float(duration))
        self.__status = Status.PASSED
        self.__trace = ""

    def get_name(self) -> Optional[str]:
        return self.__name

    def get_name_space(self) -> Optional[str]:
        return self.__name_space

    def get_class_name(self) -> Optional[str]:
        return self.__class_name

    def get_duration(self) -> Optional[float]:
        return self.__duration.total_seconds()

    def get_message(self) -> Optional[str]:
        return self.__message

    def set_message(self, value: str) -> None:
        self.__message = value

    def get_trace(self) -> Optional[str]:
        return self.__trace

    def set_trace(self, value: str) -> None:
        self.__trace = value

    def get_status(self) -> AvailableTestResultOutcome:
        return AvailableTestResultOutcome(self.__status.value)

    def set_status(self, value: Status) -> None:
        self.__status = value

    def get_is_flaky(self) -> Optional[bool]:
        return self.__is_flaky

    def set_is_flaky(self, value: bool) -> None:
        self.__is_flaky = value
