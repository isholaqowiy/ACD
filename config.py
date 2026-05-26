import sys
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    BOT_TOKEN: str = Field(..., validation_alias="BOT_TOKEN")
    OPENAI_API_KEY: str = Field(..., validation_alias="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4o-mini", validation_alias="OPENAI_MODEL")
    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./data/bot.db", validation_alias="DATABASE_URL")
    ADMIN_IDS: str = Field(default="", validation_alias="ADMIN_IDS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def get_admin_ids(self) -> list[int]:
        if not self.ADMIN_IDS:
            return []
        return [int(i.strip()) for i in self.ADMIN_IDS.split(",") if i.strip()]

try:
    settings = Settings()
except Exception as e:
    print(f"CRITICAL: Missing environment variables: {e}")
    sys.exit(1)
