from flask_restful import Resource
from app.helpers import redis
from app.workers.slow_job import slow_job

class Baz(Resource):
    @redis.redis_cache("Test")
    def get(self):
        slow_job.queue(2)
        return {"hello": "world"}
