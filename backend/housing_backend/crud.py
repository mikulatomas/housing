from sqlalchemy.orm import Session

import models, schemas


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


def get_predictions(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Prediction)
        .order_by(models.Prediction.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_predictions_history(db: Session, limit: int = 1000):
    return (
        db.query(models.Prediction.predicted_at, models.Prediction.predicted_price)
        .order_by(models.Prediction.predicted_at.asc())
        .limit(limit)
        .all()
    )


def create_prediction(db: Session, prediction: schemas.PredictionBase):
    db_prediction = models.Prediction(**prediction.dict())
    # db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
