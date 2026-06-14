from pydantic import BaseModel
from typing import Optional, List

class Role(BaseModel):
    id: int
    name: str
    description: str


class UpsertRole(BaseModel):
    name: str | None = None
    description: str | None = None


class FindRoleQuery(BaseModel):
    page: int | None = 1
    page_size: str | int | None = 5
    ordering: str | None = "id"
    name__eq: str | None = None

# схема для ответа сервера (блок search_options возвращает репозиторий)
class SearchOptions(BaseModel):
    page: int
    page_size: int | str
    ordering: str
    total_count: int


class FindRoleResult(BaseModel):
    founds: List[Role]
    search_options: SearchOptions 