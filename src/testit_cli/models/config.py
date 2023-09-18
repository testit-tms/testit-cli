from dataclasses import dataclass


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
    results: str
    is_debug: bool
    output: str
