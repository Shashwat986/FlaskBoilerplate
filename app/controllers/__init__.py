from flask import Blueprint
from flask_restful import Api

from .foo import Foo
from .bar import Bar
from .baz import Baz

bp = Blueprint("api", __name__)
api = Api(bp)

api.add_resource(Foo, "/foo")
api.add_resource(Bar, "/bar")
api.add_resource(Baz, "/baz")
