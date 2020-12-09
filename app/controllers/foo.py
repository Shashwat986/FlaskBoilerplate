from flask_restful import Resource
from ..models.user import User

class Foo(Resource):
    def get(self):
        return {
          'hello': 'world',
          'count': len(User.query.all())
        }
