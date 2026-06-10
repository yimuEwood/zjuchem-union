from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "浙大化学系学生会工作站"
    DATABASE_URL: str = "mysql+pymysql://zjuchem:zjuchem2024@mysql:3306/zjuchem_union"
    SECRET_KEY: str = "change-me-to-a-strong-random-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    class Config:
        env_file = ".env"

settings = Settings()
