from flask import Blueprint, render_template

from stewardship.service import list_models


stewardship_blueprint = Blueprint("stewardship", __name__)


@stewardship_blueprint.route("/stewardship")
def stewardship_page():
    models = list_models()
    default_model = models[0]["name"] if models else None
    return render_template("stewardship/index.html", models=models, default_model=default_model)

