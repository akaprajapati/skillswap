from app.core.celery_app import celery
from app.db.session import SessionLocal
from app.models.notification import Notification
import asyncio


@celery.task
def notify_match(user_id, match_id):
    db = SessionLocal()

    # 🧠 Save notification in DB
    notif = Notification(
        user_id=user_id,
        title="New Match 🎉",
        message=f"You have a new match! Match ID: {match_id}"
    )

    db.add(notif)
    db.commit()
    db.refresh(notif)

    # 🔥 Send real-time (optional async bridge)
    try:
        from app.services.notification_manager import manager

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            manager.send(user_id, {
                "title": notif.title,
                "message": notif.message
            })
        )
    except:
        pass

    db.close()