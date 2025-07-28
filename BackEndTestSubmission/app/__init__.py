from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logger.logconfig import setup_logging

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    setup_logging()
    db.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()

    return app
