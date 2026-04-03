from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.user import User
from app.services.matchmaking import (
    create_swipe,
    check_mutual_like,
    create_match,
    check_skill_match
)
from app.core.dependencies import require_permission

router = APIRouter(prefix="/match", tags=["Match"])


# ✅ SWIPE (LIKE / SKIP)
@router.post("/swipe")
def swipe(
    from_user_id: int,
    to_user_id: int,
    action: str,
    db: Session = Depends(get_db),
    user=Depends(require_permission("initiate_match"))
):
    if action not in ["like", "skip"]:
        raise HTTPException(400, "Invalid action")

    from_user = db.query(User).get(from_user_id)
    to_user = db.query(User).get(to_user_id)

    if not from_user or not to_user:
        raise HTTPException(404, "User not found")

    # Save swipe
    create_swipe(db, from_user_id, to_user_id, action)

    # Only proceed if LIKE
    if action == "like":
        mutual = check_mutual_like(db, from_user_id, to_user_id)

        if mutual:
            # 🔥 Check skill compatibility
            if check_skill_match(from_user, to_user):
                match = create_match(db, from_user_id, to_user_id)
                return {
                    "message": "🎉 Match created!",
                    "match_id": match.id
                }
            else:
                return {"message": "Mutual like but no skill compatibility"}

    return {"message": "Swipe recorded"}


# ✅ GET MATCHES FOR USER
@router.get("/user/{user_id}")
def get_matches(user_id: int, db: Session = Depends(get_db)):
    matches = db.query(User).filter(
        (User.id == user_id)
    ).first()

    return matches