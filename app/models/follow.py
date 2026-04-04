from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from datetime import datetime
from app.db.session import Base


class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True)

    follower_id = Column(Integer, ForeignKey("users.id"))
    following_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('follower_id', 'following_id', name='unique_follow'),
    )