from databricks import sql
import httpx
import os


def _normalize_host(host):
    if host.startswith("https://"):
        host = host[len("https://") :]
    if host.startswith("http://"):
        host = host[len("http://") :]
    return host.rstrip("/")


def _workspace_url_from_host(host):
    normalized = _normalize_host(host)
    return f"https://{normalized}"


def _get_oauth_token_from_client_credentials(host, client_id, client_secret):
    token_url = f"{_workspace_url_from_host(host)}/oidc/v1/token"
    payload = {
        "grant_type": "client_credentials",
        "scope": "all-apis",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = httpx.post(token_url, data=payload, timeout=20.0)
    response.raise_for_status()
    data = response.json()
    token = data.get("access_token")
    if not token:
        raise RuntimeError("Databricks OAuth token response missing access_token.")
    return token


def get_connection():
    databricks_host = os.getenv("DATABRICKS_HOST") or os.getenv("DATABRICKS_SERVER_HOSTNAME")
    server_hostname = _normalize_host(databricks_host) if databricks_host else None
    http_path = os.getenv("DATABRICKS_HTTP_PATH")
    access_token = os.getenv("DATABRICKS_TOKEN")
    client_id = os.getenv("DATABRICKS_CLIENT_ID")
    client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")

    missing = []
    if not server_hostname:
        missing.append("DATABRICKS_HOST")
    if not http_path:
        missing.append("DATABRICKS_HTTP_PATH")
    if not access_token and not (client_id and client_secret):
        missing.append("DATABRICKS_TOKEN or (DATABRICKS_CLIENT_ID + DATABRICKS_CLIENT_SECRET)")

    if missing:
        raise RuntimeError(f"Missing Databricks connection env vars: {', '.join(missing)}")

    if not access_token:
        access_token = _get_oauth_token_from_client_credentials(
            host=server_hostname,
            client_id=client_id,
            client_secret=client_secret,
        )

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