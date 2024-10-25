from pydantic import BaseModel
from desbordante.ind import IND


class IndModel(BaseModel):
    @classmethod
    def from_ind(cls, ind: IND):
        return cls(lhs=ind.get_lhs(), rhs=ind.get_rhs())

    lhs: tuple[str, ...]
    rhs: tuple[str, ...]


class IndAlgoResult(BaseModel):
    inds: list[IndModel]
