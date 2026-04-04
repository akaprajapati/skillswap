from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.rbac import Role, Permission, role_permissions
from app.models.user import User
from app.schemas.rbac import RoleCreate, PermissionCreate, AssignRole, AssignPermission

router = APIRouter(prefix="/rbac", tags=["RBAC"])

# -----------------------
# ROLE CRUD
# -----------------------

@router.post("/roles")
def create_role(payload: RoleCreate, db: Session = Depends(get_db)):
    if db.query(Role).filter(Role.name == payload.name).first():
        raise HTTPException(400, "Role already exists")

    role = Role(name=payload.name)
    db.add(role)
    db.commit()
    return role


@router.get("/roles")
def get_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()


@router.put("/roles/{role_id}")
def update_role(role_id: int, payload: RoleCreate, db: Session = Depends(get_db)):
    role = db.query(Role).get(role_id)

    if not role:
        raise HTTPException(404, "Role not found")

    role.name = payload.name
    db.commit()

    return {"message": "Role updated"}


@router.delete("/roles/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).get(role_id)

    if not role:
        raise HTTPException(404, "Role not found")

    db.delete(role)
    db.commit()

    return {"message": "Role deleted"}


# -----------------------
# PERMISSION CRUD
# -----------------------

@router.post("/permissions")
def create_permission(payload: PermissionCreate, db: Session = Depends(get_db)):
    if db.query(Permission).filter(Permission.name == payload.name).first():
        raise HTTPException(400, "Permission exists")

    perm = Permission(name=payload.name)
    db.add(perm)
    db.commit()

    return perm


@router.get("/permissions")
def get_permissions(db: Session = Depends(get_db)):
    return db.query(Permission).all()


@router.put("/permissions/{perm_id}")
def update_permission(perm_id: int, payload: PermissionCreate, db: Session = Depends(get_db)):
    perm = db.query(Permission).get(perm_id)

    if not perm:
        raise HTTPException(404, "Permission not found")

    perm.name = payload.name
    db.commit()

    return {"message": "Permission updated"}


@router.delete("/permissions/{perm_id}")
def delete_permission(perm_id: int, db: Session = Depends(get_db)):
    perm = db.query(Permission).get(perm_id)

    if not perm:
        raise HTTPException(404, "Permission not found")

    db.delete(perm)
    db.commit()

    return {"message": "Permission deleted"}


# -----------------------
# USER MANAGEMENT (ADMIN PANEL 🔥)
# -----------------------

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return [
        {
            "id": u.id,
            "email": u.email,
            "roles": [r.name for r in u.roles]
        }
        for u in users
    ]


@router.get("/users/{user_id}")
def get_user_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)

    if not user:
        raise HTTPException(404, "User not found")

    permissions = set()

    for role in user.roles:
        result = db.execute(
            role_permissions.select().where(
                role_permissions.c.role_id == role.id
            )
        )

        for row in result:
            perm = db.query(Permission).get(row.permission_id)
            permissions.add(perm.name)

    return {
        "id": user.id,
        "email": user.email,
        "roles": [r.name for r in user.roles],
        "permissions": list(permissions)
    }


# -----------------------
# ROLE ASSIGNMENT
# -----------------------

@router.post("/assign-role")
def assign_role(payload: AssignRole, db: Session = Depends(get_db)):
    user = db.query(User).get(payload.user_id)
    role = db.query(Role).get(payload.role_id)

    if not user or not role:
        raise HTTPException(404, "User or Role not found")

    if role in user.roles:
        return {"message": "Already assigned"}

    user.roles.append(role)
    db.commit()

    return {"message": "Role assigned"}


@router.post("/remove-role")
def remove_role(payload: AssignRole, db: Session = Depends(get_db)):
    user = db.query(User).get(payload.user_id)
    role = db.query(Role).get(payload.role_id)

    if not user or not role:
        raise HTTPException(404, "Not found")

    if role in user.roles:
        user.roles.remove(role)
        db.commit()

    return {"message": "Role removed"}


# -----------------------
# PERMISSION ASSIGNMENT
# -----------------------

@router.post("/assign-permission")
def assign_permission(payload: AssignPermission, db: Session = Depends(get_db)):
    db.execute(role_permissions.insert().values(
        role_id=payload.role_id,
        permission_id=payload.permission_id
    ))
    db.commit()

    return {"message": "Permission assigned"}


@router.post("/remove-permission")
def remove_permission(payload: AssignPermission, db: Session = Depends(get_db)):
    db.execute(
        role_permissions.delete().where(
            (role_permissions.c.role_id == payload.role_id) &
            (role_permissions.c.permission_id == payload.permission_id)
        )
    )
    db.commit()

    return {"message": "Permission removed"}


# -----------------------
# ROLE → PERMISSIONS VIEW
# -----------------------

@router.get("/roles/{role_id}/permissions")
def get_role_permissions(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).get(role_id)

    if not role:
        raise HTTPException(404, "Role not found")

    result = db.execute(
        role_permissions.select().where(
            role_permissions.c.role_id == role.id
        )
    )

    perms = []
    for row in result:
        perm = db.query(Permission).get(row.permission_id)
        perms.append(perm.name)

    return {
        "role": role.name,
        "permissions": perms
    }