from flask import Blueprint, render_template


stewardship_blueprint = Blueprint("stewardship", __name__)


@stewardship_blueprint.route("/stewardship")
def stewardship_page():
    return render_template("stewardship/index.html")

