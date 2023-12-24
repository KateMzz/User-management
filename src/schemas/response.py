from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class IResponse(BaseModel, Generic[T]):
    payload: T
    message: Optional[str]
