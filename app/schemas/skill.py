from pydantic import BaseModel

class SkillCreate(BaseModel):
    name: str
    category_id: int

class CategoryCreate(BaseModel):
    name: str

class AssignSkill(BaseModel):
    user_id: int
    skill_id: int