"""
parser.py
---------
Reads db.json and identifies:
  - which keys are collections (list values)
  - what fields each collection has (inferred from first item)
"""

import json
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).parent.parent / "data" / "db.json"


def load_db() -> dict[str, Any]:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database file not found: {DB_PATH}")
    with DB_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def detect_collections(data: dict[str, Any]) -> dict[str, list[str]]:
    """
    Returns a mapping of resource_name -> list of field names.
    Only keys whose values are non-empty lists of dicts are treated as resources.
    """
    collections: dict[str, list[str]] = {}
    for key, value in data.items():
        if isinstance(value, list) and value and isinstance(value[0], dict):
            collections[key] = list(value[0].keys())
    return collections


def get_resource_schema(resource: str) -> list[str]:
    """Returns field names for a given resource."""
    data = load_db()
    items = data.get(resource, [])
    if not items:
        return []
    return [k for k in items[0].keys() if k != "id"]
