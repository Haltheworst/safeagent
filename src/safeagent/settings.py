from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SAFEAGENT_", env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./runtime/safeagent.db"
    policy_path: Path = Path("config/default.json")
