from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.skill import Skill, SkillCategory
from app.models.user import User
from app.schemas.skill import SkillCreate, CategoryCreate, AssignSkill
from app.core.dependencies import require_permission

router = APIRouter(prefix="/skills", tags=["Skills"])


# ✅ CREATE CATEGORY
@router.post("/category")
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    user=Depends(require_permission("create_skill"))
):
    if db.query(SkillCategory).filter_by(name=payload.name).first():
        raise HTTPException(400, "Category exists")

    cat = SkillCategory(name=payload.name)
    db.add(cat)
    db.commit()

    return {"message": "Category created"}


# ✅ CREATE SKILL
@router.post("/")
def create_skill(
    payload: SkillCreate,
    db: Session = Depends(get_db),
    user=Depends(require_permission("create_skill"))
):
    skill = Skill(
        name=payload.name,
        category_id=payload.category_id
    )
    db.add(skill)
    db.commit()

    return {"message": "Skill created"}


# ✅ ASSIGN OFFERED SKILL
@router.post("/offer")
def add_offered_skill(
    payload: AssignSkill,
    db: Session = Depends(get_db),
    user=Depends(require_permission("create_skill"))
):
    user_obj = db.query(User).get(payload.user_id)
    skill = db.query(Skill).get(payload.skill_id)

    if not user_obj or not skill:
        raise HTTPException(404, "User or Skill not found")

    user_obj.offered_skills.append(skill)
    db.commit()

    return {"message": "Skill added to offered"}


# ✅ ASSIGN WANTED SKILL
@router.post("/want")
def add_wanted_skill(
    payload: AssignSkill,
    db: Session = Depends(get_db),
    user=Depends(require_permission("create_skill"))
):
    user_obj = db.query(User).get(payload.user_id)
    skill = db.query(Skill).get(payload.skill_id)

    if not user_obj or not skill:
        raise HTTPException(404, "User or Skill not found")

    user_obj.wanted_skills.append(skill)
    db.commit()

    return {"message": "Skill added to wanted"}


# ✅ GET ALL SKILLS
@router.get("/")
def list_skills(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()
    return skills


# ✅ GET USER PROFILE (WITH SKILLS)
@router.get("/user/{user_id}")
def get_user_skills(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)

    if not user:
        raise HTTPException(404, "User not found")

    return {
        "user": user.name,
        "offered": [s.name for s in user.offered_skills],
        "wanted": [s.name for s in user.wanted_skills]
    }