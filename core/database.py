from databricks import sql
from databricks.sdk.core import Config, oauth_service_principal
import os


def _normalize_host(host):
    if host.startswith("https://"):
        host = host[len("https://") :]
    if host.startswith("http://"):
        host = host[len("http://") :]
    return host.rstrip("/")


def _build_credentials_provider(server_hostname, client_id, client_secret):
    def credential_provider():
        config = Config(
            host=f"https://{server_hostname}",
            client_id=client_id,
            client_secret=client_secret,
        )
        return oauth_service_principal(config)

    return credential_provider


def _resolve_http_path():
    explicit_path = os.getenv("DATABRICKS_HTTP_PATH")
    if explicit_path:
        return explicit_path

    # Databricks Apps commonly expose a SQL warehouse resource as an ID env var.
    warehouse_id = (
        os.getenv("DATABRICKS_WAREHOUSE_ID")
        or os.getenv("SQL_WAREHOUSE_ID")
        or os.getenv("WAREHOUSE_ID")
    )
    if warehouse_id:
        return f"/sql/1.0/warehouses/{warehouse_id}"

    return None


def get_connection():
    databricks_host = os.getenv("DATABRICKS_SERVER_HOSTNAME") or os.getenv("DATABRICKS_HOST")
    server_hostname = _normalize_host(databricks_host) if databricks_host else None
    http_path = _resolve_http_path()
    access_token = os.getenv("DATABRICKS_TOKEN")
    client_id = os.getenv("DATABRICKS_CLIENT_ID")
    client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")

    missing = []
    if not server_hostname:
        missing.append("DATABRICKS_SERVER_HOSTNAME (or DATABRICKS_HOST)")
    if not http_path:
        missing.append("DATABRICKS_HTTP_PATH or DATABRICKS_WAREHOUSE_ID/SQL_WAREHOUSE_ID/WAREHOUSE_ID")
    if not access_token and not (client_id and client_secret):
        missing.append("DATABRICKS_TOKEN or (DATABRICKS_CLIENT_ID + DATABRICKS_CLIENT_SECRET)")

    if missing:
        raise RuntimeError(f"Missing Databricks connection env vars: {', '.join(missing)}")

    connect_kwargs = {
        "server_hostname": server_hostname,
        "http_path": http_path,
    }

    if access_token:
        connect_kwargs["access_token"] = access_token
    else:
        connect_kwargs["credentials_provider"] = _build_credentials_provider(
            server_hostname=server_hostname,
            client_id=client_id,
            client_secret=client_secret,
        )

    return sql.connect(**connect_kwargs)


def run_query(query):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        conn.close()