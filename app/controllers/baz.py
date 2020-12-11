from flask_restful import Resource
from app.helpers.redis import redis_cache
from app.workers.slow_job import slow_job

class Baz(Resource):
    @redis_cache("Test")
    def get(self):
        slow_job.queue(2)
        return {"hello": "world"}
