from src.schemas.base_schemas import BaseSchema
from src.schemas.dataset_schemas import DatasetsStatsSchema


class AccountStatsSchema(BaseSchema):
    datasets: DatasetsStatsSchema
    storage_limit: int
