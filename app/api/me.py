from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.core.dependencies import require_permission
from app.models.user import User

router = APIRouter(prefix="/me", tags=["Profile"])


# -------------------------
# GET CURRENT USER PROFILE
# -------------------------
@router.get("/")
def get_me(
    user=Depends(require_permission("view_feed")),
    db: Session = Depends(get_db)
):
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "bio": user.bio,
        "offered_skills": [
            {"id": s.id, "name": s.name}
            for s in user.offered_skills
        ],
        "wanted_skills": [
            {"id": s.id, "name": s.name}
            for s in user.wanted_skills
        ]
    }


# -------------------------
# UPDATE PROFILE
# -------------------------
@router.put("/")
def update_me(
    name: str = None,
    bio: str = None,
    user=Depends(require_permission("view_feed")),
    db: Session = Depends(get_db)
):
    if name is not None:
        user.name = name

    if bio is not None:
        user.bio = bio

    db.commit()

    return {"message": "Profile updated"}