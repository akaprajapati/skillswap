from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL")

celery = Celery(
    "skillswap",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery.conf.task_routes = {
    "app.tasks.*": {"queue": "default"}
}
import app.tasks.sample_task