from flask import Blueprint, render_template


user_routes = Blueprint("users", __name__, url_prefix="/users", template_folder="templates")


@user_routes.route("/")
def index():
    return render_template("index.html")
