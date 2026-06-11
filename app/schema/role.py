from pydantic import BaseModel
from typing import Optional, List

class Role(BaseModel):
    id: int
    name: str


class UpsertRole(BaseModel):
    name: str


class FindRoleQuery(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[str] = "5"
    ordering: Optional[str] = "id"
    name__eq: Optional[str] = None

# схема для ответа сервера (блок search_options возвращает репозиторий)
class SearchOptions(BaseModel):
    page: int
    page_size: int | str
    ordering: str
    total_count: int


class FindRoleResult(BaseModel):
    founds: List[Role]
    search_options: SearchOptions 