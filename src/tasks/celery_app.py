from celery import Celery

from src.config import settings

broker_url = settings.REDIS_URL

if settings.MODE == 'DOCKER':
    broker_url = f"redis://{settings.REDIS_HOST_DOCKER}:{settings.REDIS_PORT}"

celery_instance = Celery(
    "tasks",
    broker=broker_url,
    include={
        "src.tasks.tasks"
    }
)

celery_instance.conf.beat_schedule = {"test": {"task": "booking_todays_chekins", "schedule": 5}}
