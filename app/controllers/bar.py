from flask_restful import Resource
from flask import request
import jsonschema
from ..models.user import User
from . import login

BAR_SCHEMA = {
  "type": "object",
  "properties": {
    "hello": {
      "type": "string"
    },
    "world": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "color": {
            "type": "string"
          },
          "size": {
            "type": "number"
          }
        },
        "required": ["color"]
      },
      "minItems": 1
    }
  },
  "required": ["hello", "world"]
}

class Bar(Resource):
  @login.check_user_logged_in
  def post(self):
    try:
      jsonschema.validate(instance=request.get_json(), schema=BAR_SCHEMA)
    except jsonschema.exceptions.ValidationError:
      return {
        "success": False
      }

    json = request.get_json()

    return {
      'hello': 'world',
      'count': len(json['world']),
      'data': [i['color'] for i in json['world']]
    }
