from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base

# 🔗 IMPORT RELATIONS
from app.models.rbac import user_roles
from app.models.skill import user_skills_offered, user_skills_wanted


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    name = Column(String)
    bio = Column(String)

    is_active = Column(Boolean, default=True)

    # 🔐 RBAC
    roles = relationship("Role", secondary=user_roles, backref="users")

    # 🔥 SKILLS (THIS WAS MISSING / WRONG)
    offered_skills = relationship(
        "Skill",
        secondary=user_skills_offered,
        backref="offered_by_users"
    )

    wanted_skills = relationship(
        "Skill",
        secondary=user_skills_wanted,
        backref="wanted_by_users"
    )