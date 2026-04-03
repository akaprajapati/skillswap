import uvicorn
import multiprocessing
import subprocess
import time
import sys

from app.core.settings import settings
from app.core.logging import logger


def start_api():
    logger.info("🚀 Starting FastAPI...")
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )


def start_celery_worker():
    logger.info("🔥 Starting Celery worker...")

    command = [
        sys.executable,
        "-m",
        "celery",
        "-A",
        "app.core.celery_app",
        "worker",
        "--loglevel=info",
        "--pool=solo"   # Windows safe
    ]

    subprocess.run(command)


def start_celery_beat():
    logger.info("⏱ Starting Celery beat...")

    command = [
        sys.executable,
        "-m",
        "celery",
        "-A",
        "app.core.celery_app",
        "beat",
        "--loglevel=info"
    ]

    subprocess.run(command)


def check_redis():
    import redis
    try:
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        logger.info("✅ Redis connected")
    except Exception as e:
        logger.error(f"❌ Redis error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    logger.info("🔥 Starting SkillSwap System...")

    check_redis()

    api = multiprocessing.Process(target=start_api)
    worker = multiprocessing.Process(target=start_celery_worker)
    beat = multiprocessing.Process(target=start_celery_beat)

    api.start()
    time.sleep(2)

    worker.start()
    time.sleep(2)

    beat.start()

    try:
        api.join()
        worker.join()
        beat.join()
    except KeyboardInterrupt:
        logger.warning("⚠️ Shutting down...")

        api.terminate()
        worker.terminate()
        beat.terminate()