from desbordante.ar.algorithms import Apriori

from src.domain.task.primitives.base_primitive import BasePrimitive
from src.schemas.dataset_schemas import (
    DatasetType,
    TransactionalDownloadedDatasetSchema,
)
from src.schemas.task_schemas.primitives.ar.algo_name import ArAlgoName
from src.schemas.task_schemas.primitives.ar.task_params import (
    ArTaskParams,
)
from src.schemas.task_schemas.primitives.ar.task_result import (
    ArTaskResultItemSchema,
    ArTaskResultSchema,
)
from src.schemas.task_schemas.primitives.base_schemas import PrimitiveResultSchema


class ArPrimitive(
    BasePrimitive[
        Apriori,
        ArAlgoName,
        ArTaskParams[TransactionalDownloadedDatasetSchema],
        PrimitiveResultSchema[ArTaskResultSchema, ArTaskResultItemSchema],
    ]
):
    _algo_map = {
        ArAlgoName.Apriori: Apriori,
    }

    _params_schema_class = ArTaskParams[TransactionalDownloadedDatasetSchema]

    allowed_dataset_type = DatasetType.Transactional

    def execute(self, params: ArTaskParams[TransactionalDownloadedDatasetSchema]):
        dataset = params.datasets.table
        table = dataset.df

        self._algo.load_data(
            table=table, input_format=dataset.params.transactional_params.itemset_format
        )

        options = self._get_algo_options(params)

        self._algo.execute(**options)

        return PrimitiveResultSchema[ArTaskResultSchema, ArTaskResultItemSchema](
            result=ArTaskResultSchema(
                total_count=len(self._algo.get_ars()),
            ),
            items=[
                ArTaskResultItemSchema(
                    left=ar.left,
                    right=ar.right,
                    support=ar.support,
                    confidence=ar.confidence,
                )
                for ar in self._algo.get_ars()
            ],
        )
