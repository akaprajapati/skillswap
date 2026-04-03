from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.notification import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# ✅ GET USER NOTIFICATIONS
@router.get("/{user_id}")
def get_notifications(user_id: int, db: Session = Depends(get_db)):
    data = db.query(Notification).filter_by(user_id=user_id).all()

    return data


# ✅ MARK AS READ
@router.post("/read/{notif_id}")
def mark_read(notif_id: int, db: Session = Depends(get_db)):
    notif = db.query(Notification).get(notif_id)

    notif.is_read = True
    db.commit()

    return {"message": "Marked as read"}