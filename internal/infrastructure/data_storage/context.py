from typing import Any

from sqlalchemy.orm import sessionmaker, Session

from internal.infrastructure.data_storage.flat import (
    FlatContext,
    get_flat_context_maker,
    FlatContextMaker,
)
from internal.infrastructure.data_storage.relational.postgres import (
    get_postgres_context_maker,
    get_postgres_context_maker_without_pool,
)
from internal.infrastructure.data_storage.flat import (
    FlatAddModel,
    FlatDeleteModel,
)
from internal.infrastructure.data_storage.relational import (
    RelationalAddModel,
    RelationalDeleteModel,
    RelationalContextType,
)


class Context:

    def __init__(
        self, postgres_context: RelationalContextType, flat_context: FlatContext
    ):
        self._postgres_context = postgres_context
        self._flat_context = flat_context

    @property
    def flat_context(self):
        return self._flat_context

    @property
    def postgres_context(self):
        return self._postgres_context

    def commit(self):
        self._postgres_context.commit()
        self._flat_context.commit()

    def rollback(self):
        self._postgres_context.rollback()
        self._flat_context.rollback()

    def close(self):
        self._postgres_context.close()
        self._flat_context.close()

    def flush(self):
        self._postgres_context.flush()
        self._flat_context.flush()

    async def async_flush(self):
        self._postgres_context.flush()  # async calling not supported
        await self._flat_context.async_flush()

    def add(self, model: RelationalAddModel | FlatAddModel):
        if isinstance(model, RelationalAddModel):
            self._postgres_context.add(model)
        if isinstance(model, FlatAddModel):
            self._flat_context.add(model)

    def delete(self, model: RelationalDeleteModel | FlatDeleteModel):
        if isinstance(model, RelationalDeleteModel):
            self._postgres_context.delete(model)
        if isinstance(model, FlatDeleteModel):
            self._flat_context.delete(model)

    def execute(self, *args) -> Any:
        # Only for relational storages.
        return self._postgres_context.execute(*args)


class ContextMaker:

    def __init__(
        self,
        *,
        use_pool: bool = True,
        postgres_context_maker: sessionmaker[Session] | None = None,
        flat_context_maker: FlatContextMaker | None = None,
    ):
        if use_pool:
            self._postgres_context_maker = (
                postgres_context_maker
                if postgres_context_maker
                else get_postgres_context_maker()
            )
        else:
            self._postgres_context_maker = (
                postgres_context_maker
                if postgres_context_maker
                else get_postgres_context_maker_without_pool()
            )
        self._flat_context_maker = (
            flat_context_maker if flat_context_maker else get_flat_context_maker()
        )

    def __call__(self) -> Context:
        postgres_context = self._postgres_context_maker()
        flat_context = self._flat_context_maker()
        return Context(postgres_context, flat_context)


def get_context_maker():
    return ContextMaker()


def get_context_maker_without_pool():
    return ContextMaker(use_pool=False)


def get_context():
    maker = get_context_maker()
    return maker()


def get_context_without_pool():
    maker = get_context_maker_without_pool()
    return maker()
