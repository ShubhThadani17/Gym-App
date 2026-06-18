#Loads environment variables.

from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL:str
    TOKEN_EXPIRE_MINUTES:int
    SECRET_KEY:str
    ALGORITHM:str
    EMAIL_ADDRESS:str
    EMAIL_PASSWORD:str

settings = Settings()
