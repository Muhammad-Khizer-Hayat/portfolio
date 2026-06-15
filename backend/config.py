from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    EMAIL_ADDRESS: str = ""
    EMAIL_PASSWORD: str = ""
    OWNER_EMAIL: str = ""
    APP_NAME: str = "My Portfolio"

    class Config:
        env_file = ".env"

settings = Settings()
