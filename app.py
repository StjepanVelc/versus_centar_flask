from dotenv import load_dotenv
import os
from flask import Flask, request

from extensions import db, mail
from models import *
from flask import render_template
from routes.public import bp as public_bp
from routes.auth import bp as auth_bp
from extensions import csrf
import logging
from logging.handlers import RotatingFileHandler
from extensions import db, mail, csrf, limiter

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config["MAINTENANCE_MODE"] = True
    app.secret_key = os.getenv("SECRET_KEY", "dev-key")

    database_url = os.environ.get("DATABASE_URL")

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    db.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    @app.before_request
    def check_for_maintenance():
        if app.config.get("MAINTENANCE_MODE"):
        # Dozvoli statičke fajlove i admin login da ostanu dostupni
            if request.endpoint and (
            request.endpoint.startswith("static")
            or request.endpoint == "auth.admin_login"
            ):
                return

            return render_template("maintenance.html"), 503
            
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    
    with app.app_context():
        db.create_all()

    limiter.init_app(app)
    return app

app = create_app()

if not app.debug:
    handler = RotatingFileHandler("error.log", maxBytes=1000000, backupCount=3)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)
    
if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_ENV") == "development")

