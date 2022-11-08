import pathlib

import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseSettings

from enums import OceanProximity
from schemas import Price


class Settings(BaseSettings):
    model_path: pathlib.Path = pathlib.Path("model.joblib")
    database_url: str = "sqlite:///./sql_app.db"


settings = Settings()
app = FastAPI()
model = joblib.load(settings.model_path)


@app.get("/predict", response_model=Price)
def predict(
    longtitude: float,
    latitude: float,
    housing_median_age: float,
    total_rooms: float,
    total_bedrooms: float,
    population: float,
    households: float,
    median_income: float,
    ocean_proximity: OceanProximity,
):
    """Predict house price"""
    input_values = [
        longtitude,
        latitude,
        housing_median_age,
        total_rooms,
        total_bedrooms,
        population,
        households,
        median_income,
    ]
    print(input_values)
    input_values.extend(ocean_proximity.one_hot())
    input_values = np.array(input_values).reshape(1, -1)

    return {"price": model.predict(input_values)[0]}
