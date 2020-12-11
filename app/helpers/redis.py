from functools import wraps
from app import redis_client


def redis_cache(redis_key):
    def _redis_cache(f):
        @wraps(f)
        def __decorated(*args, **kwargs):
            print(redis_key)
            print(redis_client.get(redis_key))

            return f(*args, **kwargs)

        return __decorated

    return _redis_cache
