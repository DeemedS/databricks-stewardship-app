from databricks import sql
import os

def get_connection():
    return sql.connect(
        server_hostname = os.getenv("DB_SERVER"),
        http_path = os.getenv("DB_HTTP_PATH"),
        access_token = os.getenv("DB_TOKEN")
    )

def run_query(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()