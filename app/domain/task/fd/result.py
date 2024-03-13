from pydantic import BaseModel
from desbordante.fd import FD


class FDModel(BaseModel):
    @classmethod
    def from_fd(cls, fd: FD):
        return cls(lhs_indices=fd.lhs_indices, rhs_index=fd.rhs_index)

    lhs_indices: list[int]
    rhs_index: int


class FDAlgoResult(BaseModel):
    fds: list[FDModel]
