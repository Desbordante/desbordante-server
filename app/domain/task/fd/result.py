from pydantic import BaseModel
from desbordante.fd import FD


class FdModel(BaseModel):
    @classmethod
    def from_fd(cls, fd: FD):
        return cls(lhs_indices=fd.lhs_indices, rhs_index=fd.rhs_index)

    lhs_indices: list[int]
    rhs_index: int


class FdAlgoResult(BaseModel):
    fds: list[FdModel]
