"""Helper functions for dataset CRUD tests."""

from uuid import uuid4

from src.models.dataset_models import DatasetModel, PreprocessingTaskModel
from src.schemas.dataset_schemas import (
    DatasetSeparator,
    DatasetType,
    TabularDatasetParams,
    TabularTransactionalParams,
    TransactionalDatasetParams,
)


def make_dataset_entity(
    *,
    owner_id: int,
    name: str = "test_dataset.csv",
    size: int = 100,
    path: str | None = None,
    is_public: bool = False,
    type: DatasetType = DatasetType.TABULAR,
) -> DatasetModel:
    if type == DatasetType.TABULAR:
        params = TabularDatasetParams(
            has_header=True,
            separator=DatasetSeparator.COMMA,
        )
    else:
        params = TransactionalDatasetParams(
            has_header=False,
            separator=DatasetSeparator.COMMA,
            transactional_params=TabularTransactionalParams(
                itemset_format="tabular",
                has_transaction_id=False,
            ),
        )
    return DatasetModel(
        type=type,
        name=name,
        size=size,
        path=path or f"{owner_id}/{uuid4()}",
        params=params,
        owner_id=owner_id,
        is_public=is_public,
        preprocessing=PreprocessingTaskModel(),
    )
