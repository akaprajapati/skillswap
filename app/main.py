from fastapi import FastAPI
from app.api import auth
from app.db.session import Base, engine
from app.api import auth, rbac
from app.api import skills
from app.api import match
from app.api import chat
from app.api import notification
from app.api import notification_ws
# Base.metadata.create_all(bind=engine)


app = FastAPI(title="SkillSwap API")

app.include_router(auth.router)
app.include_router(skills.router)
app.include_router(auth.router)
app.include_router(rbac.router)
app.include_router(match.router)
app.include_router(chat.router)
app.include_router(notification.router)
app.include_router(notification_ws.router)

@app.get("/")
def root():
    return {"message": "SkillSwap API Running"}



