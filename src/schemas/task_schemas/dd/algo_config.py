from typing import Annotated, Literal

from pydantic import Field

from src.schemas.base_schemas import BaseSchema

from .algo_name import DdAlgoName

NUW_ROWS = "Use only first N rows of the table"
# difference_table: CSV table containing difference limits for each column
NUM_COLUMNS = "Use only first N columns of the table"


class SplitConfig(BaseSchema):
    algo_name: Literal[DdAlgoName.Split]
    num_rows: int = Field(0, ge=0, description=NUW_ROWS)
    num_columns: int = Field(0, ge=0, description=NUM_COLUMNS)


OneOfDdAlgoConfig = Annotated[
    SplitConfig,
    Field(discriminator="algo_name"),
]
