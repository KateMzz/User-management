from pydantic import BaseModel


class BaseORMModel(BaseModel):
    """Configured BaseModel"""

    class Config:
        from_attributes = True
        use_enum_values = True
