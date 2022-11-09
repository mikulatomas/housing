# from typing import List, Union,
from datetime import datetime

from pydantic import BaseModel

from enums import OceanProximity


class PredictionBase(BaseModel):
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


class PredictionCreate(PredictionBase):
    pass

class Prediction(PredictionBase):
    id: int

    class Config:
        orm_mode = True


class Price(BaseModel):
    price: float

# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: List[Item] = []

#     class Config:
#         orm_mode = True