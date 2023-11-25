from typing import Generic, Optional, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class IResponse(GenericModel, Generic[T]):
    payload: Optional[T]
    message: Optional[str]
