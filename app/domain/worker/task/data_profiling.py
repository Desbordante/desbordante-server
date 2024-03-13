from app.worker import worker
from app.domain.task.abstract_task import AbstractTask, Conf
import logging


@worker.task(bind=True)
def data_profiling_task(self, task: AbstractTask, config: Conf):
    result = task.execute(config)
    return result
