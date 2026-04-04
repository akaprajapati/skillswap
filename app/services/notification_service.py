from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.services.notification_manager import manager
import asyncio


def create_notification(db: Session, user_id: int, title: str, message: str):
    notif = Notification(
        user_id=user_id,
        title=title,
        message=message
    )
    db.add(notif)
    db.commit()

    # 🔥 Real-time push
    try:
        asyncio.create_task(
            manager.send(user_id, {
                "title": title,
                "message": message
            })
        )
    except:
        pass

    return notif