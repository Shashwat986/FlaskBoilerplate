from flask_restful import Resource
from honeybadger import honeybadger
from app.models.user import User


class Foo(Resource):
    def get(self, version):
        if version == 1:
            return self.get_v1()
        elif version == 2:
            return self.get_v2()
        else:
            return self.get_v2()

    def get_base_logic(self):
        honeybadger.notify(error_class='Exception', error_message='Test Message')
        return {
            "hello": "world",
            "count": len(User.all())
        }

    def get_v1(self):
        return {
            **self.get_base_logic(),
            **{
                "version": 1
            }
        }

    def get_v2(self):
        return {
            **self.get_base_logic(),
            **{
                "version": 2
            }
        }
