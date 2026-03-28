import os
import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = os.path.join(os.path.dirname(__file__), '.env')


class Settings(BaseSettings):
    database_url: str
    auth_secret_key: str
    token_expire_in_minutes: int = 30
    refresh_token_expire_in_days: int = 7
    algorithm: str = "HS256"
    azure_client_id: str = ""
    azure_tenant_id: str = ""
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")


settings = Settings()
