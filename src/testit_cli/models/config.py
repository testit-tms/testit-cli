from dataclasses import dataclass

from testit_cli.models.mode import Mode


@dataclass
class Config:
    mode: Mode
    url: str
    token: str
    project_id: str
    configuration_id: str
    testrun_id: str
    testrun_name: str
    results: str
    is_debug: bool
    output: str
