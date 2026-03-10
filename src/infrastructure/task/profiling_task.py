# import asyncio
# import traceback as tb
# from collections.abc import Coroutine
# from enum import StrEnum, auto
# from typing import Any, TypeVar
# from uuid import UUID

# from celery.exceptions import SoftTimeLimitExceeded, TimeLimitExceeded, WorkerLostError
# from celery.signals import task_failure, task_postrun, task_prerun

# from src.db.session import async_session_factory_without_pool
# from src.infrastructure.task.dependencies import (
#     get_profile_task_use_case,
#     get_update_task_info_use_case,
# )
# from src.infrastructure.task.resource_intensive_task import (
#     ResourceIntensiveTask,
# )
# from src.schemas.base_schemas import TaskStatus
# from src.schemas.task_schemas.base_schemas import OneOfTaskParams
# from src.worker import worker

# T = TypeVar("T")


# def _run_async(coro: Coroutine[Any, Any, T]) -> T:
#     """Запускает асинхронный код в синхронном контексте Celery."""
#     return asyncio.run(coro)


# class TaskFailureReason(StrEnum):
#     MEMORY_LIMIT_EXCEEDED = auto()
#     TIME_LIMIT_EXCEEDED = auto()
#     WORKER_KILLED_BY_SIGNAL = auto()
#     OTHER = auto()


# @worker.task(base=ResourceIntensiveTask, ignore_result=True, max_retries=0)
# def profiling_task(
#     task_id: UUID,
#     dataset_id: UUID,
#     config: OneOfTaskParams,
# ) -> Any:
#     async def _run():
#         async with async_session_factory_without_pool() as session:
#             profile_task = await get_profile_task_use_case(session=session)
#             return await profile_task(dataset_id=dataset_id, config=config)

#     return _run_async(_run())


# @task_prerun.connect(sender=profiling_task)
# def task_prerun_notifier(
#     kwargs,
#     **_,
# ) -> None:
#     async def _run() -> None:
#         async with async_session_factory_without_pool() as session:
#             update_task_info = await get_update_task_info_use_case(session=session)
#             db_task_id: UUID = kwargs["task_id"]
#             await update_task_info(task_id=db_task_id, status=TaskStatus.PROCESSING)

#     _run_async(_run())


# @task_postrun.connect(sender=profiling_task)
# def task_postrun_notifier(
#     kwargs,
#     retval,
#     **_,
# ) -> None:
#     async def _run() -> None:
#         async with async_session_factory_without_pool() as session:
#             update_task_info = await get_update_task_info_use_case(session=session)
#             db_task_id: UUID = kwargs["task_id"]
#             await update_task_info(
#                 task_id=db_task_id,
#                 status=TaskStatus.SUCCESS,
#                 result=retval,
#             )

#     _run_async(_run())


# @task_failure.connect(sender=profiling_task)
# def task_failure_notifier(
#     kwargs,
#     exception: Exception,
#     traceback,
#     **_,
# ) -> None:
#     # TODO: test all possible exceptions
#     task_failure_reason = TaskFailureReason.OTHER
#     if isinstance(exception, (TimeLimitExceeded, SoftTimeLimitExceeded)):
#         task_failure_reason = TaskFailureReason.TIME_LIMIT_EXCEEDED
#     if isinstance(exception, MemoryError):
#         task_failure_reason = TaskFailureReason.MEMORY_LIMIT_EXCEEDED
#     if isinstance(exception, WorkerLostError):
#         task_failure_reason = TaskFailureReason.WORKER_KILLED_BY_SIGNAL

#     formatted_traceback = "".join(
#         tb.format_exception(type(exception), exception, exception.__traceback__)
#     )

#     async def _run() -> None:
#         async with async_session_factory_without_pool() as session:
#             update_task_info = await get_update_task_info_use_case(session=session)
#             db_task_id: UUID = kwargs["task_id"]
#             await update_task_info(
#                 task_id=db_task_id,
#                 status=TaskStatus.FAILED,
#                 raised_exception_name=exception.__class__.__name__,
#                 failure_reason=task_failure_reason,
#                 traceback=formatted_traceback,
#             )

#     _run_async(_run())
