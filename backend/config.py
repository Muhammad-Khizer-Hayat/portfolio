from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RESEND_API_KEY: str = ""
    OWNER_EMAIL: str = ""
    APP_NAME: str = "portfolio"

    class Config:
        env_file = ".env"

settings = Settings()