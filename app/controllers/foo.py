from flask_restful import Resource
from honeybadger import honeybadger
from ..models.user import User


class Foo(Resource):
    def get(self):
        honeybadger.notify(error_class='Exception', error_message='Test Message')
        return {"hello": "world", "count": len(User.all())}
