from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from honeybadger.contrib import FlaskHoneybadger
from flask_rq2 import RQ
import rq_dashboard

from app.config import config

app = Flask(__name__)
app.config.update(**config)
app.config.from_object(rq_dashboard.default_settings)

app.register_blueprint(rq_dashboard.blueprint, url_prefix="/internal/rq")

db = SQLAlchemy(app)

FlaskHoneybadger(app, report_exceptions=True)

redis_client = FlaskRedis(app)

rq = RQ(app)

from app.controllers import bp as base_bp

app.register_blueprint(base_bp, url_prefix="")
