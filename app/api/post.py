from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_permission
from app.models.post import Post, PostLike, Comment
from app.schemas.post import PostCreate, CommentCreate
from app.db.deps import get_db


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
# GET FEED
# -------------------
@router.get("/")
def get_feed(
    user=Depends(require_permission("view_feed")),
    db: Session = Depends(get_db)
):
    posts = db.query(Post).order_by(Post.id.desc()).all()
    return posts


# -------------------
# LIKE POST
# -------------------
@router.post("/like/{post_id}")
def like_post(
    post_id: int,
    user=Depends(require_permission("like_post")),
    db: Session = Depends(get_db)
):
    like = PostLike(user_id=user.id, post_id=post_id)
    db.add(like)
    db.commit()
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
    comment = Comment(
        user_id=user.id,
        post_id=data.post_id,
        content=data.content
    )
    db.add(comment)
    db.commit()
    return {"message": "Comment added"}