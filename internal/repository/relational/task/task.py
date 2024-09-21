from internal.infrastructure.data_storage.relational.model.task import TaskORM
from internal.repository.relational import CRUD
from internal.dto.repository.task import (
    TaskCreateSchema,
    TaskUpdateSchema,
    TaskFindSchema,
    TaskResponseSchema,
)


class TaskRepository(
    CRUD[
        TaskORM, TaskCreateSchema, TaskUpdateSchema, TaskFindSchema, TaskResponseSchema
    ]
):

    def __init__(self):
        super().__init__(orm_model=TaskORM, response_schema=TaskResponseSchema)
