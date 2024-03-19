from fastapi import APIRouter, HTTPException
from pydantic import UUID4
from typing import Type
from app.domain.task.primitive_factory import PrimitiveName, PrimitiveFactory
from app.domain.task.task_factory import AnyAlgoName
from app.domain.task.abstract_task import AnyTask, AnyRes
from app.domain.worker.task.data_profiling_task import data_profiling_task

router = APIRouter(prefix="/task")


def generate_set_task_endpoint(
    primitive_name: PrimitiveName,
    algo_name: AnyAlgoName,
    task_cls: Type[AnyTask],
):
    primitive_router = APIRouter(prefix=f"/{primitive_name}", tags=[primitive_name])

    @primitive_router.post(
        f"/{algo_name}",
        name=f"Set {algo_name} task",
        tags=["set task"],
    )
    def _(
        file_id: UUID4,
        config: task_cls.config_model_cls,
    ) -> UUID4:
        async_result = data_profiling_task.delay(
            primitive_name, algo_name, file_id, config
        )
        return async_result.id

    router.include_router(primitive_router)


def generate_get_task_result_endpoint(
    primitive_name: PrimitiveName, result_cls: Type[AnyRes]
):
    primitive_router = APIRouter(prefix=f"/{primitive_name}", tags=[primitive_name])

    @primitive_router.get("", name=f"Get {primitive_name} result", tags=["get result"])
    def _(task_id: UUID4) -> result_cls:
        raise HTTPException(418, "Not implemented yet")

    router.include_router(primitive_router)


for primitive_name in PrimitiveFactory.get_names():
    task_factory = PrimitiveFactory.get_by_name(primitive_name)
    for algo_name in task_factory.get_names():
        task_cls = task_factory.get_by_name(algo_name)
        generate_set_task_endpoint(primitive_name, algo_name, task_cls)

for primitive_name in PrimitiveFactory.get_names():
    task_factory = PrimitiveFactory.get_by_name(primitive_name)
    generate_get_task_result_endpoint(
        primitive_name, task_factory.general_task_cls.result_model_cls
    )
