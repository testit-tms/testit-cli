from dataclasses import dataclass
import typing


@dataclass
class Config:
    url: str
    token: str
    project_id: str
    configuration_id: str
    testrun_id: str
    testrun_name: str
    separator: str
    namespace: str
    classname: str
    results: list[typing.Any]
    is_debug: bool
    output: str
    paths_to_attachments: list[typing.Any]
    disable_cert_validation: bool
    framework: str
    ignore_flaky_failure: bool
