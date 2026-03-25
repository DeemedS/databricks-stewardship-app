from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask

# Flask app
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "<h1>Hello World from Databricks Apps</h1>"

# FastAPI app
fastapi_app = FastAPI()

# Mount Flask inside FastAPI
fastapi_app.mount("/", WSGIMiddleware(flask_app))

app = fastapi_app