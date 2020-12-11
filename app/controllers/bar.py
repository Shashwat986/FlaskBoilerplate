from flask_restful import Resource
from flask import request
from app.models.user import User
from app.helpers import login
from app.helpers import validate

BAR_SCHEMA = {
    "type": "object",
    "properties": {
        "hello": {"type": "string"},
        "world": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "color": {"type": "string"},
                    "size": {"type": "number"}
                },
                "required": ["color"],
            },
            "minItems": 1,
        },
    },
    "required": ["hello", "world"],
}


class Bar(Resource):
    @login.check_user_logged_in
    @validate.validate_schema(BAR_SCHEMA)
    def post(self):
        json = request.get_json()

        return {
            "hello": "world",
            "count": len(json["world"]),
            "data": [i["color"] for i in json["world"]],
        }

    def post_schema_validation_error(self, error):
        print(request)
        return {
            "success": False,
            "message": error.message
        }
