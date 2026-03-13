from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.routes.users_routes import users_bp  # noqa: E402


def create_app():
    from flask import Flask
    from flask_jwt_extended import JWTManager
    from app.config import Config

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(users_bp)

    with app.app_context():
        db.create_all()

    return app
