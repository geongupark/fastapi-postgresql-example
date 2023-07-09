from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException


def create_user(session: Session, user: schemas.UserBase) -> models.Users:
    db_user = models.Users(
        nickname=user.nickname,
        gender=user.gender,
        age=user.age,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def update_user_info(
    session: Session, user_id: int, info_update: schemas.UserBase
) -> models.Users:
    user_info = session.query(models.Users).get(user_id)

    if user_info is None:
        raise HTTPException(status_code=404, detail="ID에 해당하는 User가 없습니다.")

    user_info.nickname = info_update.nickname
    user_info.gender = info_update.gender
    user_info.age = info_update.age

    session.commit()
    session.refresh(user_info)

    return user_info
