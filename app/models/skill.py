from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.session import Base

# 🔗 Association Tables

user_skills_offered = Table(
    "user_skills_offered",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("skill_id", ForeignKey("skills.id"), primary_key=True),
)

user_skills_wanted = Table(
    "user_skills_wanted",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("skill_id", ForeignKey("skills.id"), primary_key=True),
)

# 📌 Category Model
class SkillCategory(Base):
    __tablename__ = "skill_categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


# 📌 Skill Model
class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("skill_categories.id"))

    category = relationship("SkillCategory")