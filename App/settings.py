from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL:str
    model_config={
        'env_file':".env"
    }
settings=Settings()