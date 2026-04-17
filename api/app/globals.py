import os

TG_TOKEN = os.getenv("TG_TOKEN")
ADMIN_TG_ID = os.getenv("ADMIN_TG_ID")
BOT_API_KEY = os.getenv("BOT_API_KEY")
API_ALLOW_ORIGINS = os.getenv("API_ALLOW_ORIGINS").split(",")

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
JWT_EXP_SECONDS = 1800

PG_USER = os.getenv("POSTGRES_USER")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@postgres/bot"
