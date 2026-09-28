import os

from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text


load_dotenv()


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static"),
    )

    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY",
        "flood-alert-secret-key",
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///flood_alert.db",
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "กรุณาเข้าสู่ระบบเพื่อเปิดพื้นที่ของฉัน"
    login_manager.login_message_category = "info"

    from .auth import auth
    from .main import main

    app.register_blueprint(auth)
    app.register_blueprint(main)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()
        _migrate_tracked_area(app)

    if (
        not app.debug
        or os.environ.get("WERKZEUG_RUN_MAIN") == "true"
    ):
        from .scheduler import start_scheduler

        start_scheduler(app)

    return app


def _migrate_tracked_area(app):
    """Add the optional subdistrict column to existing SQLite databases."""
    inspector = inspect(db.engine)

    if not inspector.has_table("tracked_area"):
        return

    columns = {
        column["name"]
        for column in inspector.get_columns("tracked_area")
    }

    if "subdistrict" in columns:
        return

    db.session.execute(
        text(
            "ALTER TABLE tracked_area "
            "ADD COLUMN subdistrict VARCHAR(100)"
        )
    )
    db.session.commit()
