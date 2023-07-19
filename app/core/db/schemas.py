from pydantic import BaseModel


class UserBase(BaseModel):
    nickname: str
    gender: str
    age: int


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class MetaIntBase(BaseModel):
    type: str
    value: int


class MetaInt(MetaIntBase):
    id: int

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    nickname: str
    password: str
    content: str
    sessionid: str


class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True
