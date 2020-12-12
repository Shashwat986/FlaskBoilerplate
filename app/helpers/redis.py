from functools import wraps
from app import redis_client
import json

def redis_cache(redis_key):
    def _redis_cache(f):
        @wraps(f)
        def __decorated(*args, **kwargs):
            print(redis_key)

            response = redis_client.get(redis_key)

            # NOTE: This is a very hard cache. It doesn't look at any of the request params

            if response:
                return json.loads(response)
            else:
                response = f(*args, **kwargs)
                redis_client.set(redis_key, json.dumps(response))
                redis_client.expire(redis_key, 60)
                return response

        return __decorated

    return _redis_cache
