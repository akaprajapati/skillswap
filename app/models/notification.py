from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from datetime import datetime
from app.db.session import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    message = Column(String)

    is_read = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)