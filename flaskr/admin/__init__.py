from .places.routes import place_routes
from .tags.routes import tag_routes
from .users.routes import user_routes
from flask import Blueprint

admin = Blueprint("admin", __name__, url_prefix="/admin")

admin.register_blueprint(place_routes)
admin.register_blueprint(tag_routes)
admin.register_blueprint(user_routes)
