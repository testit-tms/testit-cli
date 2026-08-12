from dataclasses import dataclass
from typing import Optional


@dataclass
class TestRunLink:
    url: str
    title: Optional[str] = None
    description: Optional[str] = None
    link_type: Optional[str] = None
