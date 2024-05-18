import typing as tp

from pydantic import BaseModel


class UserInfo(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    surname: str
    roles: tp.List[str]
