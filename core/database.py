from databricks import sql
import os


def get_connection():
    server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
    http_path = os.getenv("DATABRICKS_HTTP_PATH")
    access_token = os.getenv("DATABRICKS_TOKEN")

    missing = []
    if not server_hostname:
        missing.append("DATABRICKS_SERVER_HOSTNAME")
    if not http_path:
        missing.append("DATABRICKS_HTTP_PATH")
    if not access_token:
        missing.append("DATABRICKS_TOKEN")

    if missing:
        raise RuntimeError(f"Missing Databricks connection env vars: {', '.join(missing)}")

    return sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        access_token=access_token,
    )


def run_query(query):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        conn.close()