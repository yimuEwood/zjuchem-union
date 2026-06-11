import os

DATA_DIR = os.environ.get("DATA_DIR", os.path.join(os.path.dirname(__file__), "..", "..", "data"))

class Settings:
    APP_NAME: str = "浙大化学系学生会工作站"
    DATABASE_URL: str = f"sqlite:///{DATA_DIR}/zjuchem.db"
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "change-me-to-a-strong-random-key-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

settings = Settings()
