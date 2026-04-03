from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.user import User
from app.models.rbac import Role
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


# ✅ REGISTER
@router.post("/register")
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(400, "Email already registered")

    user = User(
        email=payload.email,
        password=hash_password(payload.password),
        name=payload.name
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # 🔥 AUTO ASSIGN DEFAULT ROLE ("User")
    default_role = db.query(Role).filter(Role.name == "User").first()

    if default_role:
        user.roles.append(default_role)
        db.commit()

    return {"message": "User created"}


# ✅ LOGIN
@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"user_id": user.id})

    return {"access_token": token}