from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RESEND_API_KEY: str = ""
    OWNER_EMAIL: str = ""
    APP_NAME: str = "My Portfolio"

    class Config:
        env_file = ".env"
settings = Settings()