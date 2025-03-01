from decouple import config, Config, RepositoryEnv
from pydantic_settings import BaseSettings
import logging

config = Config(RepositoryEnv(".env"))

class Settings(BaseSettings):
    DATABASE_NAME: str = config("DATABASE_NAME")
    DATABASE_IP: str = config("DATABASE_IP")
    DATABASE_USER: str = config("DATABASE_USER")
    DATABASE_PASSWORD: str = config("DATABASE_PASSWORD")
    DATABASE_PORT: str = config("DATABASE_PORT")
    LOG_LEVEL: str = "DEBUG"

settings = Settings()
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)