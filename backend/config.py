from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RESEND_API_KEY: str = ""
    OWNER_EMAIL: str = ""
    APP_NAME: str = "My Portfolio"
    OWNER_NAME: str = "Muhammad Khizer"

    # Auto-reply settings
    GROQ_API_KEY: str = ""               # leave blank to always use the static template
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    AUTO_REPLY_FROM: str = "onboarding@resend.dev"  # swap to your verified domain sender when ready
    AUTO_REPLY_ENABLED: bool = True
    AUTO_REPLY_RATE_LIMIT_SECONDS: int = 3600  # min gap between auto-replies to the same email

    class Config:
        env_file = ".env"
settings = Settings()