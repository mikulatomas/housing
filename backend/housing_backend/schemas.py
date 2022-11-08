# from typing import List, Union,
from datetime import datetime

from pydantic import BaseModel

from .enums import OceanProximity


class Prediction(BaseModel):
    id: int
    predicted_at: datetime
    longtitude: int
    latitude: int
    housing_median_age: int
    total_rooms: int
    total_bedrooms: int
    population: int
    households: int
    median_income: int
    ocean_proximity: OceanProximity

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