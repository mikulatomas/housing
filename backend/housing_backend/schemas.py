from datetime import datetime

from pydantic import BaseModel

from .enums import OceanProximity


class ModelRequestBase(BaseModel):
    longtitude: float
    latitude: float
    housing_median_age: int
    total_rooms: int
    total_bedrooms: int
    population: int
    households: int
    median_income: float
    ocean_proximity: OceanProximity
    predicted_price: float
    predicted_at: datetime


class ModelRequestCreate(ModelRequestBase):
    pass


class ModelRequest(ModelRequestBase):
    id: int

    class Config:
        orm_mode = True


class Price(BaseModel):
    price: float


class PricePredictionHistory(BaseModel):
    predicted_at: datetime
    predicted_price: float
