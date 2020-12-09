from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from .config import config

app = Flask(__name__)
app.config.update(**config)
db = SQLAlchemy(app)

redis_client = FlaskRedis(app)

from app.controllers import bp as base_bp

app.register_blueprint(base_bp, url_prefix="")
