from pydantic import BaseModel


class BaseORMModel(BaseModel):
    """Configured BaseModel"""

    class Config:
        orm_mode = True
        use_enum_values = True
