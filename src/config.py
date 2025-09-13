from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str

    REDIS_HOST: str
    REDIS_PORT: int

    ADMIN_TELEGRAM_USERNAME: str

    class Config:
        env_file = ".env"


settings = Settings()
