"""
ARQ Worker для обработки фоновых задач
"""
from app.core.redis import WorkerSettings
from app.workers.broadcast import send_broadcast, process_broadcast_message

# Настройки воркера экспортируются для ARQ
class WorkerSettings(WorkerSettings):
    """Настройки воркера с функциями"""
    functions = [
        send_broadcast,
        process_broadcast_message,
    ]
