from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# 🔧 Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# 🧱 Base (MUST come before create_all)
Base = declarative_base()

# 🧪 Session
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# 🔥 Import ALL models BEFORE create_all
# IMPORTANT: this ensures tables are registered
from app.models import user, rbac, skill, match, chat, post, notification, follow  # adjust if needed

# 🚀 Create tables
Base.metadata.create_all(bind=engine)