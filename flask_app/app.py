from flask import Flask, jsonify
from flask_cors import CORS
from flask_app.model.db import main_db
import os
from flask_app.api.register import register_apis
from flask_app.middleware import Middleware

USER = os.environ.get("DB_USER", "postgres")
PASS = os.environ.get("DB_PASS", "1234")
IP = os.environ.get("IP", "0.0.0.0")
PORT = os.environ.get("PORT", "5432")
DB = os.environ.get("DB", "postgres")

CONFIG = f"postgresql://{USER}:{PASS}@{IP}:{PORT}/{DB}"


def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route("/")
    def home():
        return jsonify("Claude Zhang's APIs")

    app.config["RESTX_MASK_SWAGGER"] = False
    app.config["RESTX_JSON"] = {"ensure_ascii": False}
    if os.environ.get("ENV", "") == "TEST":
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = CONFIG
    main_db.init_app(app)
    app = register_apis(app)
    app.wsgi_app = Middleware(app.wsgi_app)
    with app.app_context():
        main_db.create_all()
    return app
