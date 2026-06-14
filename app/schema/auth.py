from datetime import datetime

from pydantic import BaseModel, Field

from app.schema.user import User


class SignIn(BaseModel):
    login: str
    password: str
    # first_name: str
    # last_name: str
    # middle_name: str
    # role_id: int


class SignUp(BaseModel):
    login: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    middle_name: str = Field(..., max_length=100)
    role_id: int = Field(..., ge=1)

class Payload(BaseModel):
    id: int
    login: str
    first_name: str
    last_name: str
    middle_name: str
    role_id: int


class SignInResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"  # Стандарт для OAuth2/JWT в FastAPI
    expiration: datetime
    user_info: User

class FindUserByLogin(BaseModel):
    login__eq: str 
