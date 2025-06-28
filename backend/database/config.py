from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    pinecone_api_key: str
    google_api_key: str

    # Tell Pydantic to load environment variables from .env
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()