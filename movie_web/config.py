# -*- coding: utf-8 -*-
import os
from typing import Optional

from pydantic_settings import BaseSettings

env_file_path = os.path.join(os.getcwd(), 'envs', '.env')


class Settings(BaseSettings):
    SECRET_KEY: Optional[str] = 'SECRET_KEY'
    DEBUG: Optional[int] = 1

    DATABASE_HOST: Optional[str] = 'localhost'
    DATABASE_NAME: Optional[str] = 'DATABASE_NAME'
    DATABASE_USER: Optional[str] = 'DATABASE_USER'
    DATABASE_PASS: Optional[str] = 'DATABASE_PASS'
    DATABASE_PORT: Optional[int] = 5432

    REDIS_HOST: Optional[str] = 'localhost'
    REDIS_PORT: Optional[int] = 6379

    HOST_SERVER_PORT: Optional[int] = 8001
    HOST_DOMAINT: Optional[str] = 'HOST_DOMAINT'

    class Config:
        env_file = env_file_path


sconfigs = Settings()
