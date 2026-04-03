from pydantic import BaseModel

class RoleCreate(BaseModel):
    name: str

class PermissionCreate(BaseModel):
    name: str

class AssignRole(BaseModel):
    user_id: int
    role_id: int

class AssignPermission(BaseModel):
    role_id: int
    permission_id: int