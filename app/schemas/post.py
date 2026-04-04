from pydantic import BaseModel


class PostCreate(BaseModel):
    content: str


class CommentCreate(BaseModel):
    post_id: int
    content: str