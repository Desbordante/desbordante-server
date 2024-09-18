from typing import Protocol, runtime_checkable


@runtime_checkable
class DataStorageContext(Protocol):

    def commit(self) -> None: ...

    def flush(self) -> None: ...

    def rollback(self) -> None: ...

    def close(self) -> None: ...


class UnitOfWork:

    def __init__(self, context: DataStorageContext):
        self._context = context

    def __enter__(self) -> DataStorageContext:
        return self._context

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            self._context.rollback()
        else:
            self._context.commit()
        self._context.close()
