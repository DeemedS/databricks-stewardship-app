from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, render_template

fastapi_app = FastAPI()
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return render_template("index.html")

@fastapi_app.get("/api/health")
def health():
    return {"status": "ok"}

# Mount Flask inside FastAPI
fastapi_app.mount("/", WSGIMiddleware(flask_app))

app = fastapi_app