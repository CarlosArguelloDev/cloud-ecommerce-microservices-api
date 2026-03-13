from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.routes.payments_routes import payments_bp  # noqa: E402


def create_app():
    from flask import Flask
    from app.config import Config

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(payments_bp)

    with app.app_context():
        db.create_all()

    return app
