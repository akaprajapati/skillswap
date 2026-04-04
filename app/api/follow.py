from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.follow import Follow
from app.models.user import User
from app.core.dependencies import require_permission
from app.services.notification_service import create_notification

router = APIRouter(prefix="/follow", tags=["Follow"])


# -----------------------
# FOLLOW USER
# -----------------------
@router.post("/")
def follow_user(
    user_id: int,
    user=Depends(require_permission("view_feed")),
    db: Session = Depends(get_db)
):
    if user.id == user_id:
        raise HTTPException(400, "Cannot follow yourself")

    target = db.query(User).get(user_id)
    if not target:
        raise HTTPException(404, "User not found")

    existing = db.query(Follow).filter_by(
        follower_id=user.id,
        following_id=user_id
    ).first()

    if existing:
        return {"message": "Already following"}

    follow = Follow(
        follower_id=user.id,
        following_id=user_id
    )
    db.add(follow)
    db.commit()
    
    create_notification(
    db,
    user_id=user_id,
    title="New Follower",
    message=f"{user.email} started following you"
    )

    return {"message": "Followed successfully"}


# -----------------------
# UNFOLLOW USER
# -----------------------
@router.delete("/")
def unfollow_user(
    user_id: int,
    user=Depends(require_permission("view_feed")),
    db: Session = Depends(get_db)
):
    follow = db.query(Follow).filter_by(
        follower_id=user.id,
        following_id=user_id
    ).first()

    if not follow:
        return {"message": "Not following"}

    db.delete(follow)
    db.commit()

    return {"message": "Unfollowed"}


# -----------------------
# GET FOLLOWERS
# -----------------------
@router.get("/followers/{user_id}")
def get_followers(user_id: int, db: Session = Depends(get_db)):
    followers = db.query(Follow).filter_by(following_id=user_id).all()

    return [{"user_id": f.follower_id} for f in followers]


# -----------------------
# GET FOLLOWING
# -----------------------
@router.get("/following/{user_id}")
def get_following(user_id: int, db: Session = Depends(get_db)):
    following = db.query(Follow).filter_by(follower_id=user_id).all()

    return [{"user_id": f.following_id} for f in following]