from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None
