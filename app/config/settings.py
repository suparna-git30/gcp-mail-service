from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
#from pathlib import Path

#BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    app_name: str
    app_version: str
    environment: str
    log_level: str

    model_config = SettingsConfigDict(
        #env_file=BASE_DIR / ".env",
        env_file=".env",
        case_sensitive=False,
    )
settings = Settings()

@lru_cache
def get_settings() -> Settings:
    return Settings()