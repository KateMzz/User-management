from datetime import date
from typing import List

from base_model import BaseORMModel


class GroupDetail(BaseORMModel):
    id: int
    name: str
    created_at: date
    users: List[str]
