import json
from collections import Counter
from typing import Any

from fastapi import HTTPException
import requests
from src.configuration import MIRO_ACCESS_TOKEN


def _miro_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {MIRO_ACCESS_TOKEN}"}


def fetch_all_board_items(board_id: str, limit: int = 50) -> list[dict[str, Any]]:
    """
    Fetch all items from a Miro board using cursor pagination.
    GET https://api.miro.com/v2/boards/{board_id}/items
    """
    print(
        f"Fetching Miro board items from board {board_id} with limit {limit} per page..."
    )
    url = f"https://api.miro.com/v2/boards/{board_id}/items"
    items: list[dict[str, Any]] = []
    cursor: str | None = None

    while True:
        params: dict[str, Any] = {"limit": limit}
        if cursor:
            params["cursor"] = cursor

        r = requests.get(url, headers=_miro_headers(), params=params, timeout=30)
        if r.status_code == 401:
            raise HTTPException(
                status_code=401, detail="Invalid/expired MIRO_ACCESS_TOKEN"
            )
        if r.status_code == 403:
            raise HTTPException(
                status_code=403,
                detail="Miro API forbidden (token lacks access to this board or missing scopes).",
            )
        r.raise_for_status()
        data = r.json()

        items.extend(data.get("data", []))
        cursor = data.get("cursor")
        if not cursor:
            break

    return items


def fetch_connectors(board_id: str) -> list[dict[str, Any]]:
    """
    Fetch all connectors (lines/arrows) from a Miro board.
    GET https://api.miro.com/v2/boards/{board_id}/connectors
    """
    url = f"https://api.miro.com/v2/boards/{board_id}/connectors"
    connectors: list[dict[str, Any]] = []
    cursor: str | None = None

    while True:
        params: dict[str, Any] = {"limit": 50}
        if cursor:
            params["cursor"] = cursor

        r = requests.get(url, headers=_miro_headers(), params=params, timeout=30)
        if not r.ok:
            print(f"Warning: Failed to fetch connectors: {r.status_code}")
            break
        data = r.json()

        connectors.extend(data.get("data", []))
        cursor = data.get("cursor")
        if not cursor:
            break

    return connectors


def _extract_item_text(item: dict[str, Any]) -> str | None:
    """Extract any text content from an item."""
    data = item.get("data", {}) or {}
    for key in ("content", "text", "title", "plainText"):
        val = data.get(key)
        if val:
            # Strip HTML tags
            import re
            clean = re.sub(r"<[^>]+>", "", str(val)).strip()
            if clean:
                return clean
    return None


def build_miro_description(
    items: list[dict[str, Any]], max_text_items: int = 5000
) -> str:
    """
    Creates a detailed description from board items.
    Includes every item with type, position, content, and shape info.
    """
    if not items:
        return "The Miro board appears empty (no items returned)."

    types = [it.get("type", "unknown") for it in items]
    counts = Counter(types)

    lines = [
        f"Board contains {len(items)} items.",
        "Item types: " + ", ".join([f"{k}={v}" for k, v in counts.most_common(20)]),
        "",
        "=== ALL ITEMS ===",
    ]

    for i, item in enumerate(items):
        item_type = item.get("type", "unknown")
        item_id = item.get("id", "?")

        # Position
        pos = item.get("position", {}) or {}
        x, y = pos.get("x", "?"), pos.get("y", "?")

        # Size
        geo = item.get("geometry", {}) or {}
        w, h = geo.get("width", "?"), geo.get("height", "?")

        # Content
        text = _extract_item_text(item)
        data = item.get("data", {}) or {}

        # Shape type (for shape items)
        shape = data.get("shape", "")

        parts = [f"[{i+1}] type={item_type}"]
        parts.append(f"id={item_id}")
        if shape:
            parts.append(f"shape={shape}")
        parts.append(f"pos=({x},{y})")
        parts.append(f"size=({w}x{h})")
        if text:
            parts.append(f'text="{text}"')

        # Style info (color can indicate grouping)
        style = item.get("style", {}) or data.get("style", {}) or {}
        fill = style.get("fillColor") or style.get("backgroundColor")
        if fill:
            parts.append(f"color={fill}")

        lines.append("  ".join(parts))

        if i >= max_text_items:
            lines.append(f"... truncated ({len(items) - i} more items)")
            break

    return "\n".join(lines)


def build_miro_description_with_connectors(
    items: list[dict[str, Any]],
    connectors: list[dict[str, Any]],
) -> str:
    """
    Build a comprehensive description including items AND connectors (arrows/lines).
    This gives the LLM the full picture of the diagram structure.
    """
    desc = build_miro_description(items)

    if not connectors:
        desc += "\n\n=== CONNECTORS ===\nNo connectors (arrows/lines) found on the board."
        return desc

    # Build an id->label map for resolving connector endpoints
    id_to_label: dict[str, str] = {}
    for item in items:
        item_id = str(item.get("id", ""))
        text = _extract_item_text(item)
        item_type = item.get("type", "unknown")
        label = text or f"{item_type}_{item_id[-4:]}"
        id_to_label[item_id] = label

    lines = [f"\n\n=== CONNECTORS ({len(connectors)} arrows/lines) ==="]
    for c in connectors:
        start = c.get("startItem", {}) or {}
        end = c.get("endItem", {}) or {}
        start_id = str(start.get("id", "?"))
        end_id = str(end.get("id", "?"))
        start_label = id_to_label.get(start_id, f"item_{start_id[-4:]}")
        end_label = id_to_label.get(end_id, f"item_{end_id[-4:]}")

        caption = ""
        captions = c.get("captions", []) or []
        if captions:
            caption = captions[0].get("content", "") if isinstance(captions[0], dict) else str(captions[0])

        style = c.get("style", {}) or {}
        stroke_style = style.get("strokeStyle", "")

        line = f'  "{start_label}" -> "{end_label}"'
        if caption:
            line += f' label="{caption}"'
        if stroke_style:
            line += f" style={stroke_style}"
        lines.append(line)

    desc += "\n".join(lines)
    return desc
