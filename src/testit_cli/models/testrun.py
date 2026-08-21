from dataclasses import dataclass, field
from typing import List

from adapters_api.model.assign_attachment_api_model import AssignAttachmentApiModel
from adapters_api.model.update_link_api_model import UpdateLinkApiModel


@dataclass
class TestRun:
    id: str
    project_id: str
    state: str
    name: str
    description: str
    launch_source: str
    attachments: List[AssignAttachmentApiModel]
    links: List[UpdateLinkApiModel]
    tags: List[str] = field(default_factory=list)
