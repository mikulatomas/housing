
import datetime
from typing import List

import joblib
import numpy as np
from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session

from .crud import get_model_requests, get_price_prediction_history, create_prediction
from .enums import OceanProximity
from .models import Base
from .schemas import Price, ModelRequestBase, ModelRequest, PricePredictionHistory
from .database import SessionLocal, engine
from .settings import settings


Base.metadata.create_all(bind=engine)

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
    median_income: float,
    ocean_proximity: OceanProximity,
    db: Session = Depends(get_db),
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

    input_values.extend(ocean_proximity.one_hot())
    input_values = np.array(input_values).reshape(1, -1)

    prediction = model.predict(input_values)[0]

    create_prediction(
        db,
        prediction=ModelRequestBase(
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
            predicted_at=datetime.datetime.now(),
        ),
    )

    return {"price": prediction}


@app.get("/model_requests", response_model=List[ModelRequest])
def model_requests(limit: int = 10, skip: int = 0, db: Session = Depends(get_db)):
    return get_model_requests(db, limit=limit, skip=skip)


@app.get("/price_prediction_history", response_model=List[PricePredictionHistory])
def price_prediction_history(limit: int = 10, db: Session = Depends(get_db)):
    return get_price_prediction_history(db, limit=limit)


# @app.get("/random")
# def random(db: Session = Depends(get_db)):
#     import random
    
#     for i in range(100, 0, -1):
#         print(i)
#         latitude = random.randint(-90, 90)
#         longtitude = random.randint(-180, 180)
#         housing_median_age = random.randint(1, 60)
#         total_rooms = random.randint(2, 20000)
#         total_bedrooms = random.randint(1, 10000)
#         population = random.randint(1, 100000)
#         households = random.randint(1, 5000)
#         median_income = random.randint(5, 100) / 10
#         ocean_proximity = OceanProximity(random.randint(0, 4))

#         input_values = [
#             longtitude,
#             latitude,
#             housing_median_age,
#             total_rooms,
#             total_bedrooms,
#             population,
#             households,
#             median_income,
#         ]

#         input_values.extend(ocean_proximity.one_hot())
#         input_values = np.array(input_values).reshape(1, -1)

#         prediction = model.predict(input_values)[0]

#         crud.create_prediction(
#             db,
#             prediction=PredictionBase(
#                 longtitude=longtitude,
#                 latitude=latitude,
#                 housing_median_age=housing_median_age,
#                 total_rooms=total_rooms,
#                 total_bedrooms=total_bedrooms,
#                 population=population,
#                 households=households,
#                 median_income=median_income,
#                 ocean_proximity=ocean_proximity,
#                 predicted_price=prediction,
#                 predicted_at=datetime.datetime.now() - datetime.timedelta(days=i),
#             ),
#         )
    
#     return "ytes"
