# app/config.py

import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_username = os.environ['MONGO_USERNAME']
    db_password = os.environ['MONGO_PASSWORD']
    db_service = os.environ['MONGO_SERVER']


settings = Settings()
