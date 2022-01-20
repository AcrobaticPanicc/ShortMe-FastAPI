from fastapi_cache import caches
from fastapi_cache.backends.redis import CACHE_KEY


def redis_cache():
    return caches.get(CACHE_KEY)
