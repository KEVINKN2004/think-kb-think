from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file = ".env", extra = "ignore")
    database_url: str
    embedding_provider: str = "local"
    openai_api_key: str = ""

    anthropic_api_key: str = ""
    generation_model: str = "claude-sonnet-4-6"
    min_similarity_threshold: float = 0.3

    admin_api_key: str = ""
    rate_limit_ask: str = "10/minute"
    rate_limit_search: str = "30/minute"
    max_chunks_per_document: int = 200

settings = Settings()