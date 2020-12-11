from flask_restful import Resource
from honeybadger import honeybadger

class Fail(Resource):
    def get(self):
        a = {
            "key": "value"
        }
        return {
            "score": a["score"]
        }
