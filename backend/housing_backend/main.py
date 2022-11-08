import pathlib
import datetime
from typing import List

import joblib
import numpy as np
from fastapi import FastAPI, Depends
from pydantic import BaseSettings
from sqlalchemy.orm import Session

import crud
import models
from enums import OceanProximity
from schemas import Price, PredictionBase, Prediction
from database import SessionLocal, engine


class Settings(BaseSettings):
    model_path: pathlib.Path = pathlib.Path("model.joblib")
    database_url: str = "sqlite:///./sql_app.db"


models.Base.metadata.create_all(bind=engine)
settings = Settings()
app = FastAPI()
model = joblib.load(settings.model_path)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/predict", response_model=Price)
def predict(
    longtitude: float,
    latitude: float,
    housing_median_age: int,
    total_rooms: int,
    total_bedrooms: int,
    population: int,
    households: int,
    median_income: int,
    ocean_proximity: OceanProximity,
    db: Session = Depends(get_db)
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

    prediction = model.predict(input_values)[0]

    crud.create_prediction(db, prediction=PredictionBase(
            longtitude=longtitude,
            latitude=latitude,
            housing_median_age=housing_median_age,
            total_rooms=total_rooms,
            total_bedrooms=total_bedrooms,
            population=population,
            households=households,
            median_income=median_income,
            ocean_proximity=ocean_proximity,
            predicted_price=prediction,
            predicted_at=datetime.datetime.now()
        ))

    return {"price": prediction}


@app.get("/history", response_model=List[Prediction])
def history(db: Session = Depends(get_db)):
    return crud.get_predictions(db)
