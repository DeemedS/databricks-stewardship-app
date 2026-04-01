from stewardship.model_registry import MODEL_DEFS
from stewardship.repository import (
    create_row,
    delete_rows_by_keys,
    get_key_column,
    list_rows_paginated,
    update_rows_by_keys,
)


def list_models():
    return [{"name": name, "columns": columns} for name, columns in sorted(MODEL_DEFS.items())]


def get_rows(model_name, page=1, page_size=20):
    rows, total, total_pages = list_rows_paginated(model_name=model_name, page=page, page_size=page_size)
    return {
        "rows": rows,
        "total": total,
        "total_pages": total_pages,
        "key_column": get_key_column(model_name),
    }


def add_row(model_name, values):
    create_row(model_name=model_name, row_values=values)


def edit_rows(model_name, selected_keys, values):
    return update_rows_by_keys(model_name=model_name, selected_keys=selected_keys, row_values=values)


def remove_rows(model_name, selected_keys):
    return delete_rows_by_keys(model_name=model_name, selected_keys=selected_keys)

