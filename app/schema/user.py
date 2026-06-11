from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.schema.base import FindBase
from app.schema.base import SearchOptions


class BaseUser(BaseModel):
    login: str
    first_name: str 
    last_name: str
    middle_name: str 
    role_id: int

    model_config = {"from_attributes": True} 


class BaseUserWithPassword(BaseUser):
    password_hash: str


class User(BaseUser):
    id: int


class FindUser(FindBase):
    login__eq: str | None = None


class UpsertUser(BaseModel):
    login: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    role_id: int | None = None
    password_hash: str | None = None

    model_config = {"from_attributes": True}


class FindUserResult(BaseModel):
    founds: Optional[List[User]]
    search_options: Optional[SearchOptions]
