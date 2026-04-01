from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from stewardship.model_registry import MODEL_DEFS
from stewardship.service import add_row, edit_rows, get_rows, list_models, remove_rows


router = APIRouter(prefix="/api/stewardship", tags=["stewardship"])
templates = Jinja2Templates(directory="templates")


def _extract_values(form_data, columns):
    values = {}
    for column in columns:
        field_name = f"field__{column}"
        if field_name in form_data:
            values[column] = form_data.get(field_name)
    return values


@router.get("/table", response_class=HTMLResponse)
def table_partial(request: Request, model: str, page: int = 1, page_size: int = 20, message: str = "", level: str = "info"):
    data = get_rows(model_name=model, page=page, page_size=page_size)
    return templates.TemplateResponse(
        "components/stewardship_table.html",
        {
            "request": request,
            "model": model,
            "columns": MODEL_DEFS[model],
            "rows": data["rows"],
            "key_column": data["key_column"],
            "page": page,
            "page_size": page_size,
            "total": data["total"],
            "total_pages": data["total_pages"],
            "message": message,
            "level": level,
        },
    )


@router.post("/create", response_class=HTMLResponse)
async def create_row(request: Request, model: str = Form(...), page: int = Form(1), page_size: int = Form(20)):
    form = await request.form()
    values = _extract_values(form, MODEL_DEFS[model])
    add_row(model, values)
    return table_partial(request, model=model, page=page, page_size=page_size, message="Row added.", level="success")


@router.post("/update", response_class=HTMLResponse)
async def update_row(
    request: Request,
    model: str = Form(...),
    page: int = Form(1),
    page_size: int = Form(20),
    selected_keys: list[str] = Form(default=[]),
):
    form = await request.form()
    values = _extract_values(form, MODEL_DEFS[model])
    if not selected_keys:
        return table_partial(request, model=model, page=page, page_size=page_size, message="Select rows to edit.", level="warning")
    count = edit_rows(model, selected_keys, values)
    return table_partial(request, model=model, page=page, page_size=page_size, message=f"Updated {count} row(s).", level="success")


@router.post("/delete", response_class=HTMLResponse)
def delete_row(
    request: Request,
    model: str = Form(...),
    page: int = Form(1),
    page_size: int = Form(20),
    selected_keys: list[str] = Form(default=[]),
):
    if not selected_keys:
        return table_partial(request, model=model, page=page, page_size=page_size, message="Select rows to delete.", level="warning")
    count = remove_rows(model, selected_keys)
    return table_partial(request, model=model, page=page, page_size=page_size, message=f"Deleted {count} row(s).", level="success")


@router.get("/models")
def models():
    return {"models": list_models()}

