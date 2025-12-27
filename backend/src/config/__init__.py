"""Application configuration settings"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  """Application settings for async database operations."""

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="allow",
  )

  # Application Settings
  ENVIRONMENT_PROPOGATION_VALUE: str = "UNCONFIGURED"
  ENVIRONMENT: str = "development"

  API_PORT: int = 8000

  # OpenAI API - Compliant Server Settings
  OPENAI_API_BASE_URL: str = "http://localhost:1234/v1"
  OPENAI_API_MODEL_ID: str = "qwen/qwen3-14b"
  OPENAI_API_KEY: str = "placeholder"

  @property
  def is_production(self) -> bool:
    """Check if running in production environment."""
    return self.ENVIRONMENT.lower() == "production"


settings = Settings()
