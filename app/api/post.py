from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import require_permission
from app.models.post import Post, PostLike, Comment
from app.schemas.post import PostCreate, CommentCreate
from app.db.deps import get_db
from app.services.notification_service import create_notification

router = APIRouter(prefix="/posts", tags=["Posts"])


# -------------------
# CREATE POST
# -------------------
@router.post("/")
def create_post(
    data: PostCreate,
    user=Depends(require_permission("create_post")),
    db: Session = Depends(get_db)
):
    post = Post(user_id=user.id, content=data.content)
    db.add(post)
    db.commit()
    return {"message": "Post created"}


# -------------------
# GET FEED (WITH COUNTS)
# -------------------
@router.get("/")
def get_feed(
    user=Depends(require_permission("view_feed")),
    db: Session = Depends(get_db)
):
    posts = db.query(Post).order_by(Post.id.desc()).all()

    result = []

    for post in posts:
        like_count = db.query(PostLike).filter_by(post_id=post.id).count()
        comments = db.query(Comment).filter_by(post_id=post.id).all()

        result.append({
            "id": post.id,
            "user_id": post.user_id,
            "content": post.content,
            "created_at": post.created_at,
            "like_count": like_count,
            "comment_count": len(comments),
            "comments": [
                {
                    "id": c.id,
                    "user_id": c.user_id,
                    "content": c.content,
                    "created_at": c.created_at
                }
                for c in comments
            ]
        })

    return result


# -------------------
# GET SINGLE POST
# -------------------
@router.get("/{post_id}")
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = db.query(Post).get(post_id)

    if not post:
        raise HTTPException(404, "Post not found")

    like_count = db.query(PostLike).filter_by(post_id=post.id).count()
    comments = db.query(Comment).filter_by(post_id=post.id).all()

    return {
        "id": post.id,
        "user_id": post.user_id,
        "content": post.content,
        "created_at": post.created_at,
        "like_count": like_count,
        "comments": [
            {
                "id": c.id,
                "user_id": c.user_id,
                "content": c.content,
                "created_at": c.created_at
            }
            for c in comments
        ]
    }


# -------------------
# LIKE POST (NO DUPLICATE)
# -------------------
@router.post("/like/{post_id}")
def like_post(
    post_id: int,
    user=Depends(require_permission("like_post")),
    db: Session = Depends(get_db)
):
    post = db.query(Post).get(post_id)

    existing = db.query(PostLike).filter_by(
        user_id=user.id,
        post_id=post_id
    ).first()

    if existing:
        return {"message": "Already liked"}

    like = PostLike(user_id=user.id, post_id=post_id)
    db.add(like)
    db.commit()

    create_notification(
        db,
        user_id=post.user_id,
        title="Post Liked",
        message=f"{user.email} liked your post"
    )

    return {"message": "Post liked"}


# -------------------
# COMMENT
# -------------------
@router.post("/comment")
def comment_post(
    data: CommentCreate,
    user=Depends(require_permission("comment_post")),
    db: Session = Depends(get_db)
):
    post = db.query(Post).get(data.post_id)

    comment = Comment(
        user_id=user.id,
        post_id=data.post_id,
        content=data.content
    )
    db.add(comment)
    db.commit()

    create_notification(
        db,
        user_id=post.user_id,
        title="New Comment",
        message=f"{user.email} commented on your post"
    )

    return {"message": "Comment added"}


# -------------------
# PERSONALIZED FEED
# -------------------
@router.get("/feed/personalized")
def personalized_feed(
    user=Depends(require_permission("view_feed")),
    db: Session = Depends(get_db)
):
    from app.models.follow import Follow

    following = db.query(Follow).filter_by(
        follower_id=user.id
    ).all()

    following_ids = [f.following_id for f in following]

    if not following_ids:
        return []

    posts = db.query(Post).filter(
        Post.user_id.in_(following_ids)
    ).order_by(Post.id.desc()).all()

    result = []

    for post in posts:
        like_count = db.query(PostLike).filter_by(post_id=post.id).count()
        comments = db.query(Comment).filter_by(post_id=post.id).all()

        result.append({
            "id": post.id,
            "user_id": post.user_id,
            "content": post.content,
            "created_at": post.created_at,
            "like_count": like_count,
            "comment_count": len(comments),
            "comments": [
                {
                    "id": c.id,
                    "user_id": c.user_id,
                    "content": c.content
                }
                for c in comments
            ]
        })

    return result