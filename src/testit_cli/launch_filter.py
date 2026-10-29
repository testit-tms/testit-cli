"""Parsers for `testrun create launch` filter and autotest external ids file."""
import typing


class LaunchFilterError(ValueError):
    """Invalid --filter or external ids file content."""


def parse_launch_filter(raw: str) -> typing.List[str]:
    """
    Parse `--filter tags=tag1,tag2` into a list of tags.

    Only the `tags=` key is supported.
    """
    if raw is None:
        raise LaunchFilterError("Filter value is required")

    value = str(raw).strip()
    if not value:
        raise LaunchFilterError("Filter value is empty")

    if "=" not in value:
        raise LaunchFilterError(
            f'Unsupported filter "{value}". Expected format: tags=tag1,tag2'
        )

    key, _, rest = value.partition("=")
    key = key.strip().lower()
    if key != "tags":
        raise LaunchFilterError(
            f'Unsupported filter key "{key}". Only tags=... is supported'
        )

    tags = [t.strip() for t in rest.split(",") if t.strip()]
    if not tags:
        raise LaunchFilterError("Filter tags=... must list at least one tag")
    return tags


def read_autotest_external_ids_file(path: str) -> typing.List[str]:
    """
    Read autotest external IDs from a file: one ID per line.
    Empty lines and lines starting with # are ignored.
    """
    ids: typing.List[str] = []
    seen = set()

    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped not in seen:
                seen.add(stripped)
                ids.append(stripped)

    return ids
