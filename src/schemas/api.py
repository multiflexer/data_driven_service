from enum import Enum
from pydantic import BaseModel


class ClassEnum(Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"


class ResponsePredict(BaseModel):
    class_name: ClassEnum

    class Config:
        use_enum_values = True
