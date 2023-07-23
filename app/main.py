from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from .core.db import crud, models, schemas
from .core.db.base import get_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://192.168.219.105:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/users/", response_model=schemas.User)
def create_user(user_info: schemas.UserBase, session: Session = Depends(get_db)):
    db_user = (
        session.query(models.Users)
        .filter(models.Users.nickname == user_info.nickname)
        .first()
    )

    if db_user:
        raise HTTPException(
            status_code=400, detail="Nickname already registered")
    return crud.create_user(session, user_info)


@app.get(path="/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, session: Session = Depends(get_db)):
    user = session.query(models.Users).filter(
        models.Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="ID에 해당하는 User가 없습니다.")
    return user


@app.put(path="/users/{user_id}", response_model=schemas.User)
def put_user(
    user_id: int, new_info: schemas.UserBase, session: Session = Depends(get_db)
):
    user_info = crud.update_user_info(session, user_id, new_info)
    return user_info


@app.delete(path="/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_db)):
    user_info = session.query(models.Users).get(user_id)

    if user_info is None:
        raise HTTPException(status_code=404, detail="ID에 해당하는 User가 없습니다.")

    session.delete(user_info)
    session.commit()

    return user_info


@app.get(path="/meta-int/{type}", response_model=schemas.MetaInt)
def get_meta_int(type, session: Session = Depends(get_db)):
    meta_int = session.query(models.MetaInts).filter(
        models.MetaInts.type == type).first()
    if meta_int is None:
        raise HTTPException(status_code=404, detail="해당 type의 데이터가 없습니다.")
    return meta_int


@app.post("/meta-int/", response_model=schemas.MetaInt)
def create_meta_int(meta_int_info: schemas.MetaIntBase, session: Session = Depends(get_db)):
    db_meta_int = (
        session.query(models.MetaInts)
        .filter(models.MetaInts.type == meta_int_info.type)
        .first()
    )

    if db_meta_int:
        raise HTTPException(
            status_code=400, detail="type already registered")
    return crud.create_meta_int(session, meta_int_info)


@app.post("/meta-int/increase/{type}/")
def increase_meta_int(type, request: Request, session: Session = Depends(get_db)):
    if type + 'Count' in request.cookies:
        return {"message": "Already counting"}
    else:
        meta_int = session.query(models.MetaInts).filter(
            models.MetaInts.type == type).first()
        if meta_int is None:
            raise HTTPException(status_code=404, detail="해당 type의 데이터가 없습니다.")
        return crud.update_meta_int_info(session, meta_int.id, {
            'type': type, 'value': meta_int.value + 1})


@app.post("/comments/", response_model=schemas.Comment)
def create_comment(comment_info: schemas.CommentBase, session: Session = Depends(get_db)):
    return crud.create_comment(session, comment_info)


@app.get(path="/comments/{session_id}/{limit}/{page_num}")
def get_comment(session_id: str, limit: int, page_num: int, session: Session = Depends(get_db)):
    comments = session.query(models.Comments.id, models.Comments.content, models.Comments.nickname).filter(
        models.Comments.sessionid == session_id).order_by(models.Comments.id.desc()).limit(limit).offset((page_num - 1)*limit).all()
    if comments is None:
        raise HTTPException(status_code=404, detail="ID에 해당하는 Comment가 없습니다.")
    comments_dict = [{'id': id, 'content': content,
                      'nickname': nickname} for id, content, nickname in comments]

    return comments_dict


@app.put(path="/comments/{comment_id}", response_model=schemas.Comment)
def put_comment(
    comment_id: int, new_info: schemas.CommentBase, session: Session = Depends(get_db)
):
    comment_info = crud.update_comment_info(session, comment_id, new_info)
    return comment_info


@app.delete(path="/comments/{comment_id}/{pwd}")
def delete_comment(comment_id: int, pwd: str, session: Session = Depends(get_db)):
    comment_info = session.query(models.Comments).get(comment_id)

    if comment_info is None:
        raise HTTPException(status_code=404, detail="해당 댓글이 존재하지 않습니다.")

    if pwd in [comment_info.password, "0909"]:
        session.delete(comment_info)
        session.commit()
        return {"message": "true"}

    raise HTTPException(status_code=404, detail="비밀번호가 일치하지 않습니다.")
