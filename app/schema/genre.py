from pydantic import BaseModel
from typing import List


class GenreBase(BaseModel):
    name: str
    
    model_config = {"from_attributes": True}


class Genre(GenreBase):
    id: int


class UpsertGenre(GenreBase):
    ...


class FindGenreQuery(BaseModel):
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


class FindGenreResult(BaseModel):
    founds: List[Genre]
    search_options: SearchOptions 