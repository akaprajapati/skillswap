from fastapi import Depends, HTTPException, Header
from jose import jwt
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.user import User
from app.models.rbac import role_permissions, Permission
from app.core.security import SECRET_KEY, ALGORITHM


def get_current_user(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).get(payload.get("user_id"))
        return user
    except:
        return None


def require_permission(permission_name: str):
    def dependency(
        authorization: str = Header(None),  # 🔥 FIX HERE
        db: Session = Depends(get_db)
    ):
        if not authorization:
            raise HTTPException(401, "Authorization header missing")

        # 🔥 Extract token from "Bearer xxx"
        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise Exception()
        except:
            raise HTTPException(401, "Invalid Authorization format")

        user = get_current_user(token, db)

        if not user:
            raise HTTPException(401, "Unauthorized")

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

        if permission_name not in permissions:
            raise HTTPException(403, "Forbidden")

        return user

    return dependency