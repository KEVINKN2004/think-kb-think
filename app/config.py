from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file = ".env", extra = "ignore")
    database_url: str
    embedding_provider: str = "local"
    openai_api_key: str = ""

settings = Settings()