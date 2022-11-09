import pathlib

from pydantic import BaseSettings


class Settings(BaseSettings):
    model_path: pathlib.Path = pathlib.Path("model.joblib")
    database_url: str = "sqlite:///./sql_app.db"


settings = Settings()