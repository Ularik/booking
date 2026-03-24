from celery import Celery

from src.config import settings

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include={
        "src.tasks.tasks"
    }
)

celery_instance.conf.beat_schedule = {
    "test": {
        'task': 'booking_todays_chekins',
        'schedule': 5
    }
}