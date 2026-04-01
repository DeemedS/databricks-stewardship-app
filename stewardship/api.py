from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from stewardship.service import add_row, edit_rows, get_rows, list_models, remove_rows


router = APIRouter(prefix="/api/stewardship", tags=["stewardship"])


class RowMutationRequest(BaseModel):
    values: dict | None = None
    selected_rows: list[dict] | None = None


@router.get("/models")
def models():
    return {"models": list_models()}


@router.get("/rows/{model_name}")
def rows(model_name: str):
    try:
        return {"rows": get_rows(model_name)}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/rows/{model_name}")
def add(model_name: str, payload: RowMutationRequest):
    try:
        add_row(model_name, payload.values or {})
        return {"message": "Row added."}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/rows/{model_name}")
def edit(model_name: str, payload: RowMutationRequest):
    try:
        count = edit_rows(model_name, payload.selected_rows or [], payload.values or {})
        return {"message": f"Updated {count} row(s)."}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/rows/{model_name}")
def delete(model_name: str, payload: RowMutationRequest):
    try:
        count = remove_rows(model_name, payload.selected_rows or [])
        return {"message": f"Deleted {count} row(s)."}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

