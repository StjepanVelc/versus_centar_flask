from dotenv import load_dotenv
import os
from flask import Flask, request
from flask.cli import with_appcontext
from models import *
from flask import render_template
from routes.public import bp as public_bp
from routes.auth import bp as auth_bp
from extensions import csrf
import logging
from logging.handlers import RotatingFileHandler
from extensions import db, mail, csrf, limiter
from extensions import migrate

def create_app():
    
    if os.getenv("FLASK_ENV") != "production":
        load_dotenv()
    app = Flask(__name__)
    config_type = os.getenv("FLASK_ENV", "development")

    if config_type == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")
    
    
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    db.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    
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

    limiter.init_app(app)
    return app


app = create_app()


if not app.debug:
    handler = RotatingFileHandler("error.log", maxBytes=1000000, backupCount=3)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)
    
if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_ENV") == "development")

