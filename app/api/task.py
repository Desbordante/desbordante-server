from fastapi import APIRouter, HTTPException
from pydantic import UUID4
from typing import Type
import pandas as pd
from uuid import uuid4
from app.domain.task.primitive_factory import PrimitiveName, PrimitiveFactory
from app.domain.task.task_factory import AnyAlgoName
from app.domain.task.abstract_task import AbstractTask, AnyConf, AnyAlgo, AnyRes
from app.domain.common.optional_fields import OptionalFields

router = APIRouter(prefix="/task")

repo = {}


def generate_task_endpoints(
    primitive_name: PrimitiveName,
    algo_name: AnyAlgoName,
    task_cls: Type[AbstractTask[AnyAlgo, AnyConf, AnyRes]],
):
    primitive_router = APIRouter(prefix=f"/{primitive_name}", tags=[primitive_name])

    @primitive_router.post(
        f"/{algo_name}",
        name=f"Set {algo_name} task",
        tags=["set task"],
    )
    def _(config: OptionalFields[task_cls.config_model_cls]) -> UUID4:  # type: ignore
        task = task_cls(
            table=pd.read_csv("tests/datasets/university_fd.csv", sep=",", header=0)
        )
        task_id = uuid4()
        repo[task_id] = (task, config)
        return task_id

    @primitive_router.get("", name=f"Get {primitive_name} result", tags=["get result"])
    def _(task_id: UUID4) -> task_cls.result_model_cls:  # type: ignore
        task, config = repo.get(task_id, (None, None))
        if not task:
            raise HTTPException(404, "Task not found")
        return task.execute(config)

    router.include_router(primitive_router)


for primitive_name in PrimitiveName:
    task_factory = PrimitiveFactory.get_by_name(primitive_name)
    for algo_name in task_factory.enum_used_as_keys:
        task_cls = task_factory.get_by_name(algo_name)
        generate_task_endpoints(primitive_name, algo_name, task_cls)
