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
    # url = "https://api.miro.com/v2/boards/board_id/groups"
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


def build_miro_description(
    items: list[dict[str, Any]], max_text_items: int = 5000
) -> str:
    """
    Creates a compact description from board items.
    Prioritizes frames and text-like content.
    """
    if not items:
        return "The Miro board appears empty (no items returned)."

    types = [it.get("type", "unknown") for it in items]
    counts = Counter(types)

    extracted_texts: list[str] = []

    def add_text(s: str | None):
        if not s:
            return
        s = " ".join(s.split())
        if s and s not in extracted_texts:
            extracted_texts.append(s)

    # Frames as sections
    frames = [it for it in items if it.get("type") == "frame"]
    for fr in frames:
        d = fr.get("data", {}) or {}
        add_text(d.get("title"))
        add_text(d.get("content"))
        add_text(fr.get("title"))

    # Text-ish items
    for it in items:
        t = it.get("type")
        d = it.get("data", {}) or {}

        if t in {"sticky_note", "text", "card", "shape"}:
            add_text(d.get("content"))
            add_text(d.get("text"))
            add_text(d.get("title"))

        if len(extracted_texts) >= max_text_items:
            break

    summary_lines = [
        f"Board contains {len(items)} items.",
        "Item types: " + ", ".join([f"{k}={v}" for k, v in counts.most_common(12)]),
    ]

    if frames:
        frame_titles = [(fr.get("data", {}) or {}).get("title") for fr in frames]
        frame_titles = [ft for ft in frame_titles if ft]
        if frame_titles:
            summary_lines.append("Frames (sections): " + "; ".join(frame_titles[:12]))

    if extracted_texts:
        summary_lines.append("Key text snippets:")
        for s in extracted_texts[:12]:
            summary_lines.append(f"- {s}")

    return "\n".join(summary_lines)
