from stewardship.model_registry import MODEL_DEFS
from stewardship.repository import create_row, delete_rows, list_rows, update_rows


def list_models():
    return [{"name": name, "columns": columns} for name, columns in sorted(MODEL_DEFS.items())]


def get_rows(model_name):
    return list_rows(model_name=model_name)


def add_row(model_name, values):
    create_row(model_name=model_name, row_values=values)


def edit_rows(model_name, selected_rows, values):
    return update_rows(model_name=model_name, selected_rows=selected_rows, row_values=values)


def remove_rows(model_name, selected_rows):
    return delete_rows(model_name=model_name, selected_rows=selected_rows)

