from datetime import datetime
from app.tasks.models.task import TaskStatus
from app.tasks.schema.cfd.config import CFDTaskConfig
from app.tasks.schema.cfd.result import CFDTaskResult
from app.tasks.schema.base_task_config import DBTaskPrimitiveType

config = CFDTaskConfig(
    algorithm_name="name",
    primitive_type=DBTaskPrimitiveType.CFD,
    max_lhs=3,
    min_support_cfd=3,
    min_confidence=0.02,
)

result = CFDTaskResult(
    deps="deps",
    deps_amount=3,
    created_at=datetime.now(),
    deleted_at=None,
    pk_column_indices=None,
    with_patterns=None,
    without_patterns=" ",
    value_dictionary=None,
)

task_data = [
    {
        "user_id": "6d6d3c27-c39f-4fe5-a1f2-be23271e62f1",
        "file_id": "94fd971c-fa7d-4a9b-bedf-781622dc2741",
        "is_private": False,
        "attempt_number": 3,
        "status": TaskStatus.COMPLETED,
        "progres": 3.4,
        "id_executed": False,
        "id": "f0e56cd7-3360-4a30-8509-d62d28922951",
        "phase_name": " ",
        "current_phase": 4,
        "max_phase": 2,
        "error_msg": None,
        "elapsed_time": None,
        "config": config.model_dump_json(),
        "result": result.model_dump_json(),
        "created_at": datetime.now(),
    },
    {
        "user_id": "5e5c3c27-c39f-4fe5-a1f2-be23271e62f1",
        "file_id": "24ed931c-fa7d-4a9b-bedf-781622dc2741",
        "is_private": False,
        "attempt_number": 4,
        "status": TaskStatus.IN_PROCESS,
        "progres": 3.4,
        "id_executed": False,
        "created_at": datetime.now(),
        "id": "cedcb0ca-e8f4-4417-8ac5-e3b3a9c16cb1",
    },
]
