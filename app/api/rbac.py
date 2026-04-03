from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.rbac import Role, Permission, role_permissions
from app.models.user import User
from app.schemas.rbac import RoleCreate, PermissionCreate, AssignRole, AssignPermission

router = APIRouter(prefix="/rbac", tags=["RBAC"])


# ✅ CREATE ROLE
@router.post("/roles")
def create_role(payload: RoleCreate, db: Session = Depends(get_db)):
    if db.query(Role).filter(Role.name == payload.name).first():
        raise HTTPException(400, "Role already exists")

    role = Role(name=payload.name)
    db.add(role)
    db.commit()
    return {"message": "Role created"}


# ✅ CREATE PERMISSION
@router.post("/permissions")
def create_permission(payload: PermissionCreate, db: Session = Depends(get_db)):
    if db.query(Permission).filter(Permission.name == payload.name).first():
        raise HTTPException(400, "Permission already exists")

    perm = Permission(name=payload.name)
    db.add(perm)
    db.commit()
    return {"message": "Permission created"}


# ✅ ASSIGN ROLE TO USER
@router.post("/assign-role")
def assign_role(payload: AssignRole, db: Session = Depends(get_db)):
    user = db.query(User).get(payload.user_id)
    role = db.query(Role).get(payload.role_id)

    if not user or not role:
        raise HTTPException(404, "User or Role not found")

    user.roles.append(role)
    db.commit()

    return {"message": "Role assigned"}


# ✅ ASSIGN PERMISSION TO ROLE
@router.post("/assign-permission")
def assign_permission(payload: AssignPermission, db: Session = Depends(get_db)):
    role = db.query(Role).get(payload.role_id)
    perm = db.query(Permission).get(payload.permission_id)

    if not role or not perm:
        raise HTTPException(404, "Role or Permission not found")

    db.execute(role_permissions.insert().values(
        role_id=role.id,
        permission_id=perm.id
    ))
    db.commit()

    return {"message": "Permission assigned"}