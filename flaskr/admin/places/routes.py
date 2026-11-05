from flask import Blueprint, render_template


place_routes = Blueprint("places", __name__, url_prefix="/places", template_folder="templates")


@place_routes.route("/")
def index():
    return render_template("index.html")
