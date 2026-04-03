from sqlalchemy import Column, Integer, ForeignKey, String
from app.db.session import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)

    user1_id = Column(Integer, ForeignKey("users.id"))
    user2_id = Column(Integer, ForeignKey("users.id"))

    status = Column(String, default="active")  # active, completed


class Swipe(Base):
    __tablename__ = "swipes"

    id = Column(Integer, primary_key=True)

    from_user_id = Column(Integer, ForeignKey("users.id"))
    to_user_id = Column(Integer, ForeignKey("users.id"))

    action = Column(String)  # like / skip