from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")

class PaginationParams(BaseModel):
    page: int = 1
    limit: int = 20

class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    total: int
    page: int
    limit: int
    total_pages: int
