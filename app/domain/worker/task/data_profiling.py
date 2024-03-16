from app.worker import worker
from app.domain.task.abstract_task import AbstractTask, AnyAlgo, AnyConf, AnyRes


@worker.task(bind=True)
def data_profiling_task(
    self, task: AbstractTask[AnyAlgo, AnyConf, AnyRes], config: AnyConf
):
    result = task.execute(config)
    return result
