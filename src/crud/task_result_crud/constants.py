from src.crud.task_result_crud.query_helpers.ac_query_helper import AcQueryHelper
from src.crud.task_result_crud.query_helpers.afd_query_helper import AfdQueryHelper
from src.crud.task_result_crud.query_helpers.fd_query_helper import FdQueryHelper
from src.schemas.task_schemas.types import PrimitiveName

query_helpers_map = {
    PrimitiveName.FD: FdQueryHelper,
    PrimitiveName.AFD: AfdQueryHelper,
    PrimitiveName.AC: AcQueryHelper,
}
