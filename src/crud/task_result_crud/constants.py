from src.crud.task_result_crud.query_helpers.ac_query_helper import AcQueryHelper
from src.crud.task_result_crud.query_helpers.adc_query_helper import AdcQueryHelper
from src.crud.task_result_crud.query_helpers.afd_query_helper import AfdQueryHelper
from src.crud.task_result_crud.query_helpers.afd_verification_query_helper import (
    AfdVerificationQueryHelper,
)
from src.crud.task_result_crud.query_helpers.ar_query_helper import ArQueryHelper
from src.crud.task_result_crud.query_helpers.dd_query_helper import DdQueryHelper
from src.crud.task_result_crud.query_helpers.fd_query_helper import FdQueryHelper
from src.schemas.task_schemas.types import PrimitiveName

query_helpers_map = {
    PrimitiveName.FD: FdQueryHelper,
    PrimitiveName.AFD: AfdQueryHelper,
    PrimitiveName.AC: AcQueryHelper,
    PrimitiveName.ADC: AdcQueryHelper,
    PrimitiveName.AFD_VERIFICATION: AfdVerificationQueryHelper,
    PrimitiveName.AR: ArQueryHelper,
    PrimitiveName.DD: DdQueryHelper,
}
