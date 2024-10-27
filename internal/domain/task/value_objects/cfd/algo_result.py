from pydantic import BaseModel
from desbordante.cfd import CFD


class CfdModel(BaseModel):
    lhs_items: list[str | None]
    rhs_item: str | None

    @classmethod
    def from_cfd(cls, cfd: CFD):
        return cls(
            lhs_items=[item.value for item in cfd.lhs_items],
            rhs_item=cfd.rhs_item.value,
        )


class CfdAlgoResult(BaseModel):
    cfds: list[CfdModel]
