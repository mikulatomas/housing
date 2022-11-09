from sqlalchemy.orm import Session

from .models import ModelRequest
from .schemas import ModelRequestBase


def get_model_requests(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(ModelRequest)
        .order_by(ModelRequest.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_price_prediction_history(db: Session, limit: int = 1000):
    return (
        db.query(ModelRequest.predicted_at, ModelRequest.predicted_price)
        .order_by(ModelRequest.predicted_at.asc())
        .limit(limit)
        .all()
    )


def create_prediction(db: Session, prediction: ModelRequestBase):
    db_prediction = ModelRequest(**prediction.dict())
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

