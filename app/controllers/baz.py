from flask_restful import Resource
from app.helpers import redis

class Baz(Resource):
    @redis.redis_cache("Test")
    def get(self):
        return {"hello": "world"}
