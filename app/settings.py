from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    DB_URL:str
    ALGORITHM:str
    SECRET_KEY:str
    model_config={
        'env_file':".env"
    }


settings = Settings()