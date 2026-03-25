# main.py
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, render_template
import dash
from dash import html, dcc

# --- Flask App ---
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return render_template("index.html")

# --- Dash App ---
dash_app = dash.Dash(__name__, server=flask_app, url_base_pathname="/dash/")
dash_app.layout = html.Div([
    html.H1("Dash Dashboard"),
    dcc.Graph(id="graph", figure={"data": [{"x":[1,2,3], "y":[4,1,2]}]})
])

# --- FastAPI App ---
fastapi_app = FastAPI()

# Mount Flask (with Dash inside) into FastAPI
fastapi_app.mount("/", WSGIMiddleware(flask_app))

@fastapi_app.get("/api/health")
def health():
    return {"status": "ok"}

app = fastapi_app