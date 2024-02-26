from redis import ConnectionPool, Redis

from src.config import settings


class RedisManager:
    def __init__(self):
        self._pool = ConnectionPool(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
        )
        self.redis = Redis(connection_pool=self._pool)

    def get_redis_pool(self) -> ConnectionPool:
        return self._pool

    def close_redis_pool(self) -> None:
        self._pool.disconnect()
