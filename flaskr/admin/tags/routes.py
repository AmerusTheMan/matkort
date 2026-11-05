from flask import Blueprint, render_template


tag_routes = Blueprint("tags", __name__, url_prefix="/tags", template_folder="templates")


@tag_routes.route("/")
def index():
    return render_template("index.html")
