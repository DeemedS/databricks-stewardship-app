import os

from core.database import get_connection
from stewardship.model_registry import MODEL_DEFS

DB_CATALOG = os.getenv("DATABRICKS_CATALOG")
DB_SCHEMA = os.getenv("DATABRICKS_SCHEMA", "wanderbricks")


def _safe_table_name(model_name):
    if model_name not in MODEL_DEFS:
        raise ValueError("Unknown model selected.")
    if DB_CATALOG:
        return f"{DB_CATALOG}.{DB_SCHEMA}.{model_name}"
    return f"{DB_SCHEMA}.{model_name}"


def _get_key_column(columns):
    id_cols = [column for column in columns if column.endswith("_id")]
    if id_cols:
        return id_cols[0]
    if "id" in columns:
        return "id"
    return columns[0]


def _sql_literal(value):
    if value is None or str(value).strip() == "":
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return str(value)
    escaped = str(value).replace("'", "''")
    return f"'{escaped}'"


def list_rows(model_name, limit=500):
    columns = MODEL_DEFS[model_name]
    table = _safe_table_name(model_name)
    query = f"SELECT {', '.join(columns)} FROM {table} LIMIT {limit}"
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        raw_rows = cursor.fetchall()
    finally:
        conn.close()

    rows = []
    for row in raw_rows:
        rows.append({columns[i]: row[i] for i in range(len(columns))})
    return rows


def list_rows_paginated(model_name, page=1, page_size=20):
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 20

    columns = MODEL_DEFS[model_name]
    table = _safe_table_name(model_name)
    offset = (page - 1) * page_size

    count_query = f"SELECT COUNT(1) FROM {table}"
    query = f"SELECT {', '.join(columns)} FROM {table} LIMIT {page_size} OFFSET {offset}"

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(count_query)
        total = cursor.fetchall()[0][0]
        cursor.execute(query)
        raw_rows = cursor.fetchall()
    finally:
        conn.close()

    rows = [{columns[i]: row[i] for i in range(len(columns))} for row in raw_rows]
    total_pages = max(1, (int(total) + page_size - 1) // page_size)
    return rows, int(total), total_pages


def get_key_column(model_name):
    return _get_key_column(MODEL_DEFS[model_name])


def create_row(model_name, row_values):
    table = _safe_table_name(model_name)
    columns = MODEL_DEFS[model_name]
    values = [_sql_literal(row_values.get(column)) for column in columns]
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(values)})"
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    finally:
        conn.close()


def update_rows(model_name, selected_rows, row_values):
    columns = MODEL_DEFS[model_name]
    table = _safe_table_name(model_name)
    key_col = _get_key_column(columns)
    set_chunks = []
    for column in columns:
        if column in row_values and row_values[column] not in (None, ""):
            set_chunks.append(f"{column} = {_sql_literal(row_values[column])}")
    if not set_chunks:
        return 0

    conn = get_connection()
    updated = 0
    try:
        cursor = conn.cursor()
        for row in selected_rows:
            key_value = row.get(key_col)
            query = f"UPDATE {table} SET {', '.join(set_chunks)} WHERE {key_col} = {_sql_literal(key_value)}"
            cursor.execute(query)
            updated += 1
        conn.commit()
    finally:
        conn.close()
    return updated


def delete_rows(model_name, selected_rows):
    columns = MODEL_DEFS[model_name]
    table = _safe_table_name(model_name)
    key_col = _get_key_column(columns)
    conn = get_connection()
    deleted = 0
    try:
        cursor = conn.cursor()
        for row in selected_rows:
            key_value = row.get(key_col)
            query = f"DELETE FROM {table} WHERE {key_col} = {_sql_literal(key_value)}"
            cursor.execute(query)
            deleted += 1
        conn.commit()
    finally:
        conn.close()
    return deleted


def update_rows_by_keys(model_name, selected_keys, row_values):
    columns = MODEL_DEFS[model_name]
    table = _safe_table_name(model_name)
    key_col = _get_key_column(columns)
    set_chunks = []
    for column in columns:
        if column in row_values and row_values[column] not in (None, ""):
            set_chunks.append(f"{column} = {_sql_literal(row_values[column])}")
    if not set_chunks:
        return 0

    conn = get_connection()
    updated = 0
    try:
        cursor = conn.cursor()
        for key_value in selected_keys:
            query = f"UPDATE {table} SET {', '.join(set_chunks)} WHERE {key_col} = {_sql_literal(key_value)}"
            cursor.execute(query)
            updated += 1
        conn.commit()
    finally:
        conn.close()
    return updated


def delete_rows_by_keys(model_name, selected_keys):
    columns = MODEL_DEFS[model_name]
    table = _safe_table_name(model_name)
    key_col = _get_key_column(columns)
    conn = get_connection()
    deleted = 0
    try:
        cursor = conn.cursor()
        for key_value in selected_keys:
            query = f"DELETE FROM {table} WHERE {key_col} = {_sql_literal(key_value)}"
            cursor.execute(query)
            deleted += 1
        conn.commit()
    finally:
        conn.close()
    return deleted

