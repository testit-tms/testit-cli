from dataclasses import dataclass
from typing import List
from testit_api_client.model.assign_attachment_api_model import AssignAttachmentApiModel
from testit_api_client.model.link_put_model import LinkPutModel


@dataclass
class TestRun:
    id: str
    project_id: str
    state: str
    name: str
    description: str
    launch_source: str
    attachments: List[AssignAttachmentApiModel]
    links: List[LinkPutModel]
