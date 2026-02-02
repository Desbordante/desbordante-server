from desbordante.fd import FD

from src.schemas.base_schemas import BaseSchema


class FdModel(BaseSchema):
    @classmethod
    def from_fd(cls, fd: FD):
        return cls(lhs_indices=fd.lhs_indices, rhs_index=fd.rhs_index)

    lhs_indices: list[int]
    rhs_index: int


class FdAlgoResult(BaseSchema):
    fds: list[FdModel]
