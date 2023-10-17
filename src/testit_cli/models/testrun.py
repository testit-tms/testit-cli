from dataclasses import dataclass


@dataclass
class TestRun:
    id: str
    project_id: str
    state: str
    name: str
    description: str
    launch_source: str
    attachments: list
    links: list
