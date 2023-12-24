from uuid import UUID

from pydantic import BaseModel


class BaseORMModel(BaseModel):
    """Configured BaseModel"""

    class ConfigDict:
        from_attributes = True
        use_enum_values = True
        json_encoders = {UUID: lambda v: v.hex}
