from flask_restful import Resource
from app.helpers.redis import redis_cache
from app.workers.slow_job import slow_job
from app.services.cat_facts import CatFacts

class Baz(Resource):
    @redis_cache("CatFact")
    def get(self):
        slow_job.queue(2)
        fact = CatFacts()
        fact.sync()
        return {
            "fact": fact.text
        }
