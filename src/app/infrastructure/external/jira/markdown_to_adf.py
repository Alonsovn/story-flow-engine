import re
from itertools import count
from typing import Any

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_CHECKLIST_ITEM_RE = re.compile(r"^[-*]\s+\[([ xX])\]\s+(.*)$")
_BULLET_ITEM_RE = re.compile(r"^[-*]\s+(.*)$")
_INLINE_RE = re.compile(r"\*\*(?P<bold>.+?)\*\*|\[(?P<link_text>[^\]]+)\]\((?P<link_href>[^)]+)\)")


def markdown_to_adf(text: str) -> dict[str, Any]:
    """
    Converts the markdown subset used in epic/story descriptions (headings,
    bold, bullet lists, and `- [ ]` checklists) into an Atlassian Document
    Format (ADF) document, so Jira renders formatted content instead of a
    flat plain-text paragraph.
    """
    content: list[dict[str, Any]] = []
    list_buffer: list[dict[str, Any]] = []
    list_kind: str | None = None
    task_ids = count()

    def flush_list() -> None:
        nonlocal list_kind
        if list_buffer:
            content.append({"type": list_kind, "content": list(list_buffer)})
            list_buffer.clear()
        list_kind = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            flush_list()
            continue

        heading_match = _HEADING_RE.match(line)
        if heading_match:
            flush_list()
            level = min(len(heading_match.group(1)), 6)
            content.append(
                {
                    "type": "heading",
                    "attrs": {"level": level},
                    "content": _inline_nodes(heading_match.group(2)),
                }
            )
            continue

        checklist_match = _CHECKLIST_ITEM_RE.match(line)
        if checklist_match:
            if list_kind != "taskList":
                flush_list()
                list_kind = "taskList"
            state = "DONE" if checklist_match.group(1).lower() == "x" else "TODO"
            list_buffer.append(
                {
                    "type": "taskItem",
                    "attrs": {"localId": f"task-{next(task_ids)}", "state": state},
                    "content": _inline_nodes(checklist_match.group(2)),
                }
            )
            continue

        bullet_match = _BULLET_ITEM_RE.match(line)
        if bullet_match:
            if list_kind != "bulletList":
                flush_list()
                list_kind = "bulletList"
            list_buffer.append(
                {
                    "type": "listItem",
                    "content": [{"type": "paragraph", "content": _inline_nodes(bullet_match.group(1))}],
                }
            )
            continue

        flush_list()
        content.append({"type": "paragraph", "content": _inline_nodes(line)})

    flush_list()

    if not content:
        content.append({"type": "paragraph", "content": []})

    return {"type": "doc", "version": 1, "content": content}


def _inline_nodes(text: str) -> list[dict[str, Any]]:
    """Splits a line into ADF text nodes, applying bold and link marks."""
    nodes: list[dict[str, Any]] = []
    pos = 0

    for match in _INLINE_RE.finditer(text):
        if match.start() > pos:
            nodes.append({"type": "text", "text": text[pos:match.start()]})

        if match.group("bold") is not None:
            nodes.append(
                {"type": "text", "text": match.group("bold"), "marks": [{"type": "strong"}]}
            )
        else:
            nodes.append(
                {
                    "type": "text",
                    "text": match.group("link_text"),
                    "marks": [{"type": "link", "attrs": {"href": match.group("link_href")}}],
                }
            )
        pos = match.end()

    if pos < len(text):
        nodes.append({"type": "text", "text": text[pos:]})

    if not nodes:
        nodes.append({"type": "text", "text": text})

    return nodes
