from arq import create_pool
from arq.connections import RedisSettings
from app.core.config import settings

async def get_redis_pool():
    """Создать пул соединений для ARQ"""
    return await create_pool(
        RedisSettings(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            database=settings.REDIS_DB,
        )
    )

# Настройки для воркера ARQ
class WorkerSettings:
    redis_settings = RedisSettings(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        database=settings.REDIS_DB,
    )
    
    # Функции, которые будет выполнять воркер
    functions = [
        "app.workers.broadcast.send_broadcast",
        "app.workers.broadcast.process_broadcast_message",
    ]
    
    # Настройки воркера
    max_jobs = 10
    job_timeout = 300  # 5 минут
