from dataclasses import dataclass


@dataclass
class TestRun:
    id: str
    project_id: str
    state: str
