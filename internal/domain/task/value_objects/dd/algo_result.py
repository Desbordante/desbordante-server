from pydantic import BaseModel
from desbordante.dd import DD


class DdModel(BaseModel):
    description: str

    @classmethod
    def from_dd(cls, dd: DD):
        return cls(description=str(dd))


class DdAlgoResult(BaseModel):
    dds: list[DdModel]
