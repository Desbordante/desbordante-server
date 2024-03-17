from fastapi import APIRouter, HTTPException, Depends
from pydantic import UUID4
from typing import Type, Annotated
import pandas as pd
from uuid import uuid4
from app.domain.task.primitive_factory import PrimitiveName, PrimitiveFactory
from app.domain.task.task_factory import AnyAlgoName
from app.domain.task.abstract_task import AnyTask, AnyRes
from app.domain.common.optional_fields import OptionalFields

router = APIRouter(prefix="/task")

repo = {}


def get_df_by_file_id(file_id: UUID4) -> pd.DataFrame:
    return pd.read_csv("tests/datasets/university_fd.csv", sep=",", header=0)


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
        df: Annotated[pd.DataFrame, Depends(get_df_by_file_id)],
        config: OptionalFields[task_cls.config_model_cls],
    ) -> UUID4:
        task = task_cls(df)
        task_id = uuid4()
        repo[task_id] = (task, config)
        return task_id

    router.include_router(primitive_router)


def generate_get_task_result_endpoint(
    primitive_name: PrimitiveName, result_cls: Type[AnyRes]
):
    primitive_router = APIRouter(prefix=f"/{primitive_name}", tags=[primitive_name])

    @primitive_router.get("", name=f"Get {primitive_name} result", tags=["get result"])
    def _(task_id: UUID4) -> result_cls:
        task, config = repo.get(task_id, (None, None))
        if not task:
            raise HTTPException(404, "Task not found")
        return task.execute(config)

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
