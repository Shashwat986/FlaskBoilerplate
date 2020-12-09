from flask import Blueprint
from flask_restful import Api
from app.helpers import login

from .foo import Foo
from .bar import Bar

bp = Blueprint('api', __name__)
api = Api(bp)

api.add_resource(Foo, '/foo')
api.add_resource(Bar, '/bar')
