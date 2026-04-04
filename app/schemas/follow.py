from pydantic import BaseModel


class FollowRequest(BaseModel):
    user_id: int  # user to follow/unfollow