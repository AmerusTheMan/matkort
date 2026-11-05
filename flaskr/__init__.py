from flask import Flask
from .db import db
from .app_secrets import flask_session_key
from .admin import admin
from .main.routes import main


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.secret_key = app_secrets.flask_session_key
    
    db.init_app(app)

    # Create databse if it does not already exist.
    with app.app_context():
        db.create_all()
        app.register_blueprint(admin)
        app.register_blueprint(main)
        




    return app

