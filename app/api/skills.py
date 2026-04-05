from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.skill import Skill, SkillCategory
from app.models.user import User
from app.schemas.skill import SkillCreate, CategoryCreate, AssignSkill
from app.core.dependencies import require_permission

router = APIRouter(prefix="/skills", tags=["Skills"])


# -------------------------
# CATEGORY CRUD
# -------------------------

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

    return cat


@router.get("/category")
def list_categories(db: Session = Depends(get_db)):
    return db.query(SkillCategory).all()


# -------------------------
# SKILL CRUD
# -------------------------

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

    return skill


@router.get("/")
def list_skills(db: Session = Depends(get_db)):
    return db.query(Skill).all()


# -------------------------
# 🔥 CATEGORY → SKILLS (UI MAIN API)
# -------------------------

@router.get("/category-with-skills")
def category_with_skills(db: Session = Depends(get_db)):
    categories = db.query(SkillCategory).all()

    result = []

    for cat in categories:
        skills = db.query(Skill).filter_by(category_id=cat.id).all()

        result.append({
            "id": cat.id,
            "name": cat.name,
            "skills": [
                {"id": s.id, "name": s.name}
                for s in skills
            ]
        })

    return result


# -------------------------
# USER SKILL MANAGEMENT
# -------------------------

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

    if skill in user_obj.offered_skills:
        return {"message": "Already added"}

    user_obj.offered_skills.append(skill)
    db.commit()

    return {"message": "Skill added to offered"}


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

    if skill in user_obj.wanted_skills:
        return {"message": "Already added"}

    user_obj.wanted_skills.append(skill)
    db.commit()

    return {"message": "Skill added to wanted"}


# -------------------------
# REMOVE SKILLS (IMPORTANT FOR UI)
# -------------------------

@router.delete("/offer")
def remove_offered_skill(
    payload: AssignSkill,
    db: Session = Depends(get_db),
    user=Depends(require_permission("create_skill"))
):
    user_obj = db.query(User).get(payload.user_id)
    skill = db.query(Skill).get(payload.skill_id)

    if skill in user_obj.offered_skills:
        user_obj.offered_skills.remove(skill)
        db.commit()

    return {"message": "Removed from offered"}


@router.delete("/want")
def remove_wanted_skill(
    payload: AssignSkill,
    db: Session = Depends(get_db),
    user=Depends(require_permission("create_skill"))
):
    user_obj = db.query(User).get(payload.user_id)
    skill = db.query(Skill).get(payload.skill_id)

    if skill in user_obj.wanted_skills:
        user_obj.wanted_skills.remove(skill)
        db.commit()

    return {"message": "Removed from wanted"}


# -------------------------
# USER PROFILE SKILLS
# -------------------------

@router.get("/user/{user_id}")
def get_user_skills(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)

    if not user:
        raise HTTPException(404, "User not found")

    return {
        "user": user.name,
        "offered": [
            {"id": s.id, "name": s.name}
            for s in user.offered_skills
        ],
        "wanted": [
            {"id": s.id, "name": s.name}
            for s in user.wanted_skills
        ]
    }