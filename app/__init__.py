from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config

app = Flask(__name__)
app.config.update(**config)
db = SQLAlchemy(app)

from app.controllers import bp as base_bp
app.register_blueprint(base_bp, url_prefix='')
