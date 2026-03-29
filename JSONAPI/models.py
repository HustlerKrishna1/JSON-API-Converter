"""
models.py
---------
Builds Pydantic models dynamically from the inferred schema.
Each field is typed as Any so any JSON value is accepted.
"""

from typing import Any, Optional
from pydantic import create_model


def build_model(resource: str, fields: list[str]):
    """
    Returns a Pydantic BaseModel class with:
      - one Optional[Any] field per detected column (excluding 'id')
    """
    field_definitions = {
        field: (Optional[Any], None)
        for field in fields
        if field != "id"
    }
    return create_model(resource.capitalize(), **field_definitions)
