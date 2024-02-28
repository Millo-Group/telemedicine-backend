
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ODOO_API_KEY: str
    DB_NAME: str
    JWT_SECRET_KEY: str
    CRYPTO_KEY: str

    class Config:
        env_file = ".env"
