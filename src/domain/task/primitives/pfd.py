from desbordante.pfd.algorithms import PFDTane

from src.domain.task.primitives.base_primitive import BasePrimitive
from src.schemas.dataset_schemas import (
    DatasetType,
    TabularDownloadedDatasetSchema,
)
from src.schemas.task_schemas.primitives.base_schemas import (
    ColumnSchema,
    PrimitiveResultSchema,
)
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
    ],
):
    _algo_map = {
        PfdAlgoName.PFDTane: PFDTane,
    }

    _params_schema_class = PfdTaskParams[TabularDownloadedDatasetSchema]

    allowed_dataset_type = DatasetType.Tabular

    def execute(self, params: PfdTaskParams[TabularDownloadedDatasetSchema]):
        dataset = params.datasets.table
        column_names = dataset.info.column_names

        self._algo.load_data(table=dataset.df)

        options = self._get_algo_options(params)

        self._algo.execute(**options)

        fds = self._algo.get_fds()

        return PrimitiveResultSchema(
            result=PfdTaskResultSchema(
                total_count=len(fds),
            ),
            items=[
                PfdTaskResultItemSchema(
                    lhs_columns=[
                        ColumnSchema(index=index, name=column_names[index])
                        for index in fd.lhs_indices
                    ],
                    rhs_column=ColumnSchema(
                        index=fd.rhs_index,
                        name=column_names[fd.rhs_index],
                    ),
                )
                for fd in fds
            ],
        )
