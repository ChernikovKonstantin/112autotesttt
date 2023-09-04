from . import env
from .stand import get_stand_data

__all__ = ["DB_CONFIG"]


class BaseDbConfig:
    # DB_HOST = env.get("DB_HOST", get_stand_data().db)
    # DB_PORT = env.get("DB_PORT", "6432")
    DB_HOST = env.get("DB_HOST", "192.168.10.152")
    DB_PORT = env.get("DB_PORT", "5432")
    DB_USER = env.get("DB_USER", "local")
    DB_PASSWORD = env.get("DB_PASSWORD", "local")
    DB_NAME = None


class DbConfig(BaseDbConfig):
    DB_NAME = env.get("DB_NAME_STAND", "mchs112")


DB_CONFIG = DbConfig
