from enum import Enum
import json, typing

from pydantic import BaseModel
from starlette.responses import Response


class ClassEnum(Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"


class ResponsePredict(BaseModel):
    class_name: ClassEnum

    class Config:
        use_enum_values = True


class DataItem(BaseModel):
    review: str
    target: int


class PrettyJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(", ", ": "),
        ).encode("utf-8")
