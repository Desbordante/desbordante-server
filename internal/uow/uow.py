from typing import Protocol, runtime_checkable


@runtime_checkable
class DataStorageContext(Protocol):
    def commit(self) -> None: ...

    def flush(self) -> None: ...

    def rollback(self) -> None: ...

    def close(self) -> None: ...


class DataStorageContextMaker(Protocol):
    def __call__(self) -> DataStorageContext: ...


class UnitOfWork:
    def __init__(self, context_maker: DataStorageContextMaker):
        self._context_maker: DataStorageContextMaker = context_maker
        self._context: DataStorageContext | None = None

    def __enter__(self) -> DataStorageContext:
        self._context = self._context_maker()
        return self._context

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._context is not None:
            if exc_type:
                self._context.rollback()
            else:
                self._context.commit()
            self._context.close()
            self._context = None
