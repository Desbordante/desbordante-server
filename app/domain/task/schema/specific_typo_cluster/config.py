from pydantic import UUID4
from app.domain.task.schema.base_config import BaseTaskConfig


class SpecificTypoClusterTaskConfig(BaseTaskConfig):
    parent_task_id: UUID4
    cluster_id: UUID4
