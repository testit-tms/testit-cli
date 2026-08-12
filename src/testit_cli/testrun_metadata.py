"""Parse and merge test run tags/links (config → API)."""
import json
import logging
from typing import List, Optional

from testit_api_client.model.create_link_api_model import CreateLinkApiModel
from testit_api_client.model.link_put_model import LinkPutModel
from testit_api_client.model.link_type import LinkType

from .models.testrun_link import TestRunLink

LINK_TYPES = ("Related", "BlockedBy", "Defect", "Issue", "Requirement", "Repository")


def parse_testrun_tags(raw: Optional[str]) -> Optional[List[str]]:
    if raw is None or not str(raw).strip():
        return None
    text = str(raw).strip()
    if text.startswith("["):
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            logging.warning("Invalid test run tags JSON: %s", exc)
            return None
        if not isinstance(data, list):
            logging.warning("Test run tags JSON must be an array of strings")
            return None
        tags = [str(item).strip() for item in data if str(item).strip()]
        return tags or None
    tags = [part.strip() for part in text.split(",") if part.strip()]
    return tags or None


def parse_testrun_links(raw: Optional[str]) -> Optional[List[TestRunLink]]:
    if raw is None or not str(raw).strip():
        return None
    try:
        data = json.loads(str(raw).strip())
    except json.JSONDecodeError as exc:
        logging.warning("Invalid test run links JSON: %s", exc)
        return None
    if not isinstance(data, list):
        logging.warning("Test run links JSON must be an array of objects")
        return None
    links = []
    for item in data:
        if not isinstance(item, dict):
            logging.warning("Skipping invalid test run link entry: %s", item)
            continue
        url = item.get("url")
        if not url or not str(url).strip():
            logging.warning("Skipping test run link without url: %s", item)
            continue
        link_type = item.get("type")
        if link_type is not None and str(link_type) not in LINK_TYPES:
            logging.warning(
                "Unknown link type %r; allowed: %s. Using Related.",
                link_type,
                ", ".join(LINK_TYPES),
            )
            link_type = "Related"
        links.append(
            TestRunLink(
                url=str(url).strip(),
                title=item.get("title"),
                description=item.get("description"),
                link_type=str(link_type) if link_type is not None else None,
            )
        )
    return links or None


def _to_link_type(value: Optional[str]) -> LinkType:
    name = value or "Related"
    try:
        return LinkType(name)
    except Exception:
        return LinkType("Related")


def to_create_link_models(links: Optional[List[TestRunLink]]) -> Optional[List[CreateLinkApiModel]]:
    if not links:
        return None
    return [
        CreateLinkApiModel(
            url=link.url,
            title=link.title,
            description=link.description,
            type=_to_link_type(link.link_type),
            has_info=False,
        )
        for link in links
    ]


def to_link_put_models(links: Optional[List[TestRunLink]]) -> List[LinkPutModel]:
    if not links:
        return []
    return [
        LinkPutModel(
            url=link.url,
            title=link.title,
            description=link.description,
            type=_to_link_type(link.link_type),
            has_info=False,
        )
        for link in links
    ]


def merge_tags(existing: Optional[List[str]], incoming: Optional[List[str]]) -> List[str]:
    result = list(existing or [])
    seen = set(result)
    for tag in incoming or []:
        if tag not in seen:
            result.append(tag)
            seen.add(tag)
    return result


def merge_links(
    existing: Optional[List[LinkPutModel]],
    incoming: Optional[List[LinkPutModel]],
) -> List[LinkPutModel]:
    result = list(existing or [])
    seen = {link.url for link in result}
    for link in incoming or []:
        if link.url not in seen:
            result.append(link)
            seen.add(link.url)
    return result
