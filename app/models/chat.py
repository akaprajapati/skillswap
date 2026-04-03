from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from datetime import datetime
from app.db.session import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)

    match_id = Column(Integer, ForeignKey("matches.id"))

    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))

    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)