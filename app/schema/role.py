from pydantic import BaseModel

class Role(BaseModel):
    id: int
    name: str

class UpsertRole(BaseModel):
    name: str
