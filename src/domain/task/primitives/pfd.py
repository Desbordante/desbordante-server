from desbordante.pfd.algorithms import PFDTane

from src.domain.task.primitives.base_primitive import BasePrimitive
from src.schemas.dataset_schemas import (
    DatasetType,
    TabularDownloadedDatasetSchema,
)
from src.schemas.task_schemas.primitives.base_schemas import PrimitiveResultSchema
from src.schemas.task_schemas.primitives.pfd.algo_name import PfdAlgoName
from src.schemas.task_schemas.primitives.pfd.task_params import (
    PfdTaskParams,
)
from src.schemas.task_schemas.primitives.pfd.task_result import (
    PfdTaskResultItemSchema,
    PfdTaskResultSchema,
)


class PfdPrimitive(
    BasePrimitive[
        PFDTane,
        PfdAlgoName,
        PfdTaskParams[TabularDownloadedDatasetSchema],
        PrimitiveResultSchema[PfdTaskResultSchema, PfdTaskResultItemSchema],
    ]
):
    _algo_map = {
        PfdAlgoName.PFDTane: PFDTane,
    }

    _params_schema_class = PfdTaskParams[TabularDownloadedDatasetSchema]

    allowed_dataset_type = DatasetType.Tabular

    def execute(self, params: PfdTaskParams[TabularDownloadedDatasetSchema]):
        dataset = params.datasets.table
        table = dataset.df
        columns = dataset.info.column_names

        self._algo.load_data(table=table)

        options = self._get_algo_options(params)

        self._algo.execute(**options)

        return PrimitiveResultSchema[PfdTaskResultSchema, PfdTaskResultItemSchema](
            result=PfdTaskResultSchema(
                total_count=len(self._algo.get_fds()),
            ),
            items=[
                PfdTaskResultItemSchema(
                    lhs=[columns[index] for index in fd.lhs_indices],
                    rhs=[columns[fd.rhs_index]],
                )
                for fd in self._algo.get_fds()
            ],
        )
