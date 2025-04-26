from enum import StrEnum

from _app.schemas.schemas import BaseSchema


class DatasetSeparator(StrEnum):
    Comma = ","
    Semicolon = ";"
    Pipe = "|"


class DatasetCreate(BaseSchema):
    separator: DatasetSeparator
    has_header: bool = False
