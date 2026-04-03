import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True

    REDIS_URL = os.getenv("REDIS_URL")

settings = Settings()