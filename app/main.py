from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, rbac, skills, match, chat, notification, notification_ws, post, follow
from app.db.session import Base, engine

# Base.metadata.create_all(bind=engine)

app = FastAPI(title="SkillSwap API")


# 🔥 CORS CONFIG (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ ROUTES
app.include_router(auth.router)
app.include_router(rbac.router)
app.include_router(skills.router)
app.include_router(match.router)
app.include_router(chat.router)
app.include_router(notification.router)
app.include_router(notification_ws.router)
app.include_router(post.router)
app.include_router(follow.router)


# ✅ ROOT
@app.get("/")
def root():
    return {"message": "SkillSwap API Running"}