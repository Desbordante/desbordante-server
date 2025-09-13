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
    EmptyArTaskResultSchema,
    NotEmptyArTaskResultSchema,
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

    def execute(
        self, params: ArTaskParams[TransactionalDownloadedDatasetSchema]
    ) -> PrimitiveResultSchema[ArTaskResultSchema, ArTaskResultItemSchema]:
        dataset = params.datasets.table
        table = dataset.df

        self._algo.load_data(
            table=table, input_format=dataset.params.transactional_params.itemset_format
        )

        options = self._get_algo_options(params)

        self._algo.execute(**options)

        ars = self._algo.get_ars()
        has_ars = len(ars) > 0

        if not has_ars:
            return PrimitiveResultSchema(
                result=EmptyArTaskResultSchema(
                    total_count=0,
                    has_ars=False,
                ),
                items=[],
            )

        return PrimitiveResultSchema[ArTaskResultSchema, ArTaskResultItemSchema](
            result=NotEmptyArTaskResultSchema(
                total_count=len(ars),
                has_ars=True,
                min_support=min(ar.support for ar in ars),
                max_support=max(ar.support for ar in ars),
                min_confidence=min(ar.confidence for ar in ars),
                max_confidence=max(ar.confidence for ar in ars),
            ),
            items=[
                ArTaskResultItemSchema(
                    lhs_values=ar.left,
                    rhs_values=ar.right,
                    support=ar.support,
                    confidence=ar.confidence,
                )
                for ar in ars
            ],
        )
