from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, TypeDecorator
from sqlalchemy.orm import relationship

from .database import Base
from .enums import OceanProximity


class IntEnum(TypeDecorator):
    """
    Enables passing in a Python enum and storing the enum's *value* in the db.
    The default would have stored the enum's *name* (ie the string).

    source: https://michaelcho.me/article/using-python-enums-in-sqlalchemy-models
    """
    impl = Integer

    def __init__(self, enumtype, *args, **kwargs):
        super(IntEnum, self).__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, int):
            return value

        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    predicted_at = Column(DateTime, default=datetime.now)
    longtitude = Column(Integer)
    latitude = Column(Integer)
    housing_median_age = Column(Integer)
    total_rooms = Column(Integer)
    total_bedrooms = Column(Integer)
    population = Column(Integer)
    households = Column(Integer)
    median_income = Column(Integer)
    ocean_proximity = Column(IntEnum(OceanProximity))
