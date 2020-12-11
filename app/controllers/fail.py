from flask_restful import Resource

class Fail(Resource):
    def get(self):
        a = {
            "key": "value"
        }
        return {
            "score": a["score"]
        }
