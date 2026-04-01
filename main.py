# main.py
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, render_template
from api import stewardship_api_router
from stewardship import stewardship_blueprint

# --- Flask App ---
flask_app = Flask(__name__)
flask_app.register_blueprint(stewardship_blueprint)

@flask_app.route("/")
def home():
    return render_template("index.html")

# --- FastAPI App ---
fastapi_app = FastAPI()
fastapi_app.include_router(stewardship_api_router)

# Mount Flask (with Dash inside) into FastAPI
fastapi_app.mount("/", WSGIMiddleware(flask_app))

@fastapi_app.get("/api/health")
def health():
    return {"status": "ok"}

app = fastapi_app