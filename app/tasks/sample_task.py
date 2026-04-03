from app.core.celery_app import celery

@celery.task
def test_task():
    print("🔥 Celery is working!")
    return "Done"