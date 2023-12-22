from sqlalchemy import select
from app.db import Base
import pytest
from tests.tests_data.code import code_data
from tests.tests_data.user import user_data
from tests.tests_data.role import role_data
from tests.tests_data.permission import permission_data
from tests.tests_data.session import session_data
from tests.tests_data.device import device_data
from tests.tests_data.file_info import file_info_data
from tests.tests_data.file_format import file_format_data
from tests.tests_data.task import task_data
from tests.tests_data.feedback import feedback_data
from app.db.models.user.code import Code
from app.db.models.user.device import Device
from app.db.models.user.feedback import Feedback
from app.db.models.user.permission import Permission
from app.db.models.user.role import Role
from app.db.models.user.session import Session
from app.db.models.user.user import User
from app.db.models.file.file_info import FileInfo
from app.db.models.file.file_format import FileFormat
from app.tasks.models.task import Task


@pytest.mark.parametrize(
    "table, data",
    [
        (User, user_data),
        (Permission, permission_data),
        (Device, device_data),
        (Code, code_data),
        (Role, role_data),
        (Session, session_data),
        (Feedback, feedback_data),
        (FileInfo, file_info_data),
        (FileFormat, file_format_data),
        (Task, task_data),
    ],
)
def test_database_queries(
    table: Base,
    data: list[dict],
    get_test_session,
):
    for i in range(len(data)):
        with get_test_session() as session:
            new = table(**data[i])
            session.add(new)

    with get_test_session() as session:
        query = select(table)
        data = session.execute(query).scalars().all()
        fetched_data = data

    assert len(data) == len(fetched_data)

    str_data = [{str(k): str(v) for k, v in entry.items()} for entry in data]
    for d in str_data:
        exists_in_fetched = False
        for fetched_obj in fetched_data:
            fetched_dict = {str(k): str(getattr(fetched_obj, k)) for k in d}
            if fetched_dict == d:
                exists_in_fetched = True
                break
        assert exists_in_fetched, f"Data {d} and is not found in fetched data"

    for fetched_obj in fetched_data:
        exists_in_data = False
        for d in str_data:
            fetched_dict = {str(k): str(getattr(fetched_obj, k)) for k in d}
            if fetched_dict == d:
                exists_in_data = True
                break
        assert (
            exists_in_data
        ), f"Fetched data {fetched_obj} is not found in the original data"
