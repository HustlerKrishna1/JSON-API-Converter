"""
main.py
-------
FastAPI entry point.
On startup: parse db.json → generate routes → mount all routers.
Also exposes a /reload endpoint to re-parse if db.json changes.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import json
from pathlib import Path

from app.parser import load_db, detect_collections
from app.routes import build_all_routers

DB_PATH = Path(__file__).parent.parent / "data" / "db.json"

app = FastAPI(
    title="JSON → API Converter",
    description="Upload a JSON file and get a fully functional REST API instantly.",
    version="1.0.0",
)

_mounted_resources: list[str] = []


def mount_routes() -> dict[str, list[str]]:
    """Parse db.json and mount dynamic routers. Returns detected collections."""
    data = load_db()
    collections = detect_collections(data)
    routers = build_all_routers(collections)
    for router in routers:
        app.include_router(router)
    _mounted_resources.clear()
    _mounted_resources.extend(collections.keys())
    return collections


# ── Mount routes at startup ───────────────────────────────────────────────────
collections = mount_routes()


# ── Meta endpoints ────────────────────────────────────────────────────────────

@app.get("/", tags=["meta"])
def root():
    """Lists all auto-generated resources."""
    return {
        "message": "JSON → API Converter is running",
        "resources": _mounted_resources,
        "endpoints": {
            r: [f"GET /{r}", f"GET /{r}/{{id}}", f"POST /{r}", f"PUT /{r}/{{id}}", f"DELETE /{r}/{{id}}"]
            for r in _mounted_resources
        },
    }


@app.post("/upload", tags=["meta"])
async def upload_json(file: UploadFile = File(...)):
    """
    Upload a new JSON file to replace the current database.
    The API will hot-reload with the new structure.
    """
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only .json files are accepted")

    contents = await file.read()
    try:
        data = json.loads(contents)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=422, detail=f"Invalid JSON: {e}")

    if not isinstance(data, dict):
        raise HTTPException(status_code=422, detail="Root JSON must be an object {}")

    DB_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")

    new_collections = mount_routes()
    return {
        "message": "Database replaced and routes regenerated",
        "resources": list(new_collections.keys()),
    }
