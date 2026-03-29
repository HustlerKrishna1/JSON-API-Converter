"""
storage.py
----------
All file I/O goes through here.
Assigns UUIDs to new items and persists changes back to db.json.
"""

import json
import uuid
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).parent.parent / "data" / "db.json"


def _read() -> dict[str, Any]:
    with DB_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write(data: dict[str, Any]) -> None:
    with DB_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _seed_ids(resource: str) -> None:
    """Ensure every item in a resource has an 'id' field."""
    data = _read()
    changed = False
    for item in data.get(resource, []):
        if "id" not in item:
            item["id"] = str(uuid.uuid4())
            changed = True
    if changed:
        _write(data)


# ── CRUD ─────────────────────────────────────────────────────────────────────

def get_all(resource: str) -> list[dict]:
    _seed_ids(resource)
    data = _read()
    return data.get(resource, [])


def get_by_id(resource: str, item_id: str) -> dict | None:
    return next((i for i in get_all(resource) if i.get("id") == item_id), None)


def create_item(resource: str, payload: dict) -> dict:
    data = _read()
    payload["id"] = str(uuid.uuid4())
    data.setdefault(resource, []).append(payload)
    _write(data)
    return payload


def update_item(resource: str, item_id: str, payload: dict) -> dict | None:
    data = _read()
    items = data.get(resource, [])
    for idx, item in enumerate(items):
        if item.get("id") == item_id:
            payload["id"] = item_id          # preserve the original ID
            items[idx] = payload
            _write(data)
            return payload
    return None


def delete_item(resource: str, item_id: str) -> bool:
    data = _read()
    items = data.get(resource, [])
    filtered = [i for i in items if i.get("id") != item_id]
    if len(filtered) == len(items):
        return False                          # nothing was removed
    data[resource] = filtered
    _write(data)
    return True
