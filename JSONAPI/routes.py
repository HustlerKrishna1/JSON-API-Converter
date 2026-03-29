"""
routes.py
---------
For each detected resource, builds an APIRouter with full CRUD.
All routers are returned as a list and mounted in main.py.
"""

from fastapi import APIRouter, HTTPException
from app import storage
from app.models import build_model


def make_router(resource: str, fields: list[str]) -> APIRouter:
    router = APIRouter(prefix=f"/{resource}", tags=[resource])
    Model = build_model(resource, fields)

    # ── GET all ──────────────────────────────────────────────────────────────
    @router.get("/", summary=f"List all {resource}")
    def list_all():
        return storage.get_all(resource)

    # ── GET by id ─────────────────────────────────────────────────────────────
    @router.get("/{item_id}", summary=f"Get a {resource[:-1]} by ID")
    def get_one(item_id: str):
        item = storage.get_by_id(resource, item_id)
        if item is None:
            raise HTTPException(status_code=404, detail=f"{resource[:-1]} '{item_id}' not found")
        return item

    # ── POST ─────────────────────────────────────────────────────────────────
    @router.post("/", status_code=201, summary=f"Create a new {resource[:-1]}")
    def create(body: Model):
        payload = {k: v for k, v in body.model_dump().items() if v is not None}
        return storage.create_item(resource, payload)

    # ── PUT ──────────────────────────────────────────────────────────────────
    @router.put("/{item_id}", summary=f"Replace a {resource[:-1]} by ID")
    def update(item_id: str, body: Model):
        payload = {k: v for k, v in body.model_dump().items() if v is not None}
        updated = storage.update_item(resource, item_id, payload)
        if updated is None:
            raise HTTPException(status_code=404, detail=f"{resource[:-1]} '{item_id}' not found")
        return updated

    # ── DELETE ───────────────────────────────────────────────────────────────
    @router.delete("/{item_id}", status_code=204, summary=f"Delete a {resource[:-1]}")
    def delete(item_id: str):
        removed = storage.delete_item(resource, item_id)
        if not removed:
            raise HTTPException(status_code=404, detail=f"{resource[:-1]} '{item_id}' not found")

    return router


def build_all_routers(collections: dict[str, list[str]]) -> list[APIRouter]:
    return [make_router(resource, fields) for resource, fields in collections.items()]
