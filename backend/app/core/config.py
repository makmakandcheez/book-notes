from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Book Notes"
    debug: bool = False
    database_url: str | None = None
    secret_key: SecretStr
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    cors_origins: list[str] = []

    # model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")




settings = Settings()
