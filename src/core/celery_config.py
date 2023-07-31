from kombu import Queue
from redis import Redis

from src.core.cache.redis import broker, backend


class Settings:
    """CELERY SETTINGS"""

    broker_url: Redis = broker
    result_backend: Redis = backend
    beat_scheduler: str = "redbeat.RedBeatScheduler"
    beat_max_loop_interval: int = 5
    worker_max_tasks_per_child: int = 200
    worker_max_memory_per_child: int = 16384
    broker_transport_options: object = {"visibility_timeout": 43200}
    enable_utc: bool = False
    result_extended: bool = True
    timezone: str = "Europe/London"
    task_default_queue: str = "default"
    task_queues: tuple = (
        Queue("default", routing_key="task.#"),
        Queue("high_priority", routing_key="high_priority.#"),
        Queue("low_priority", routing_key="low_priority.#"),
    )
    task_default_exchange: str = "tasks"
    task_default_exchange_type: str = "topic"
    task_default_routing_key: str = "task.default"
    # expire task results after 7 days
    result_expires: int = 604800


settings = Settings()
