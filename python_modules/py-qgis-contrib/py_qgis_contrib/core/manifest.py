""" Build manifest
"""
import traceback

from functools import cache
from pathlib import Path

from pydantic import BaseModel
from typing_extensions import Optional, cast


class Manifest(BaseModel):
    commit_id: Optional[str] = None


@cache
def get_manifest() -> Manifest:
    from importlib import resources
    path = cast(Path, resources.files('py_qgis_contrib')).joinpath("core", "manifest.json")
    if path.exists():
        try:
            with path.open() as m:
                return Manifest.model_validate_json(m.read())
        except Exception:
            traceback.print_exc()

    return Manifest()
