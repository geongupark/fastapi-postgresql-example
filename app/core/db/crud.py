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


def create_meta_int(session: Session, meta_int: schemas.MetaIntBase) -> models.MetaInts:
    db_user = models.MetaInts(
        type=meta_int.type,
        value=meta_int.value,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def update_meta_int_info(
        session: Session, meta_int_id: int, info_update) -> models.MetaInts:
    meta_int_info = session.query(models.MetaInts).get(meta_int_id)

    if meta_int_info is None:
        raise HTTPException(status_code=404, detail="ID에 해당하는 User가 없습니다.")

    meta_int_info.type = info_update['type']
    meta_int_info.value = info_update['value']

    session.commit()
    session.refresh(meta_int_info)

    return meta_int_info


def create_comment(session: Session, comment: schemas.CommentBase) -> models.Comments:
    db_user = models.Comments(
        nickname=comment.nickname,
        password=comment.password,
        content=comment.content,
        sessionid=comment.sessionid,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def update_comment_info(
        session: Session, comment_id: int, info_update) -> models.Comments:
    comment_id_info = session.query(models.Comments).get(comment_id)

    if comment_id_info is None:
        raise HTTPException(status_code=404, detail="ID에 해당하는 User가 없습니다.")

    comment_id_info.nickname = info_update.nickname
    comment_id_info.password = info_update.password
    comment_id_info.content = info_update.content
    comment_id_info.sessionid = info_update.sessionid

    session.commit()
    session.refresh(comment_id_info)

    return comment_id_info
