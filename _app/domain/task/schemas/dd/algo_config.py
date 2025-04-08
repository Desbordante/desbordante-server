from typing import Annotated, Literal, Union, Optional

from pydantic import Field

from app.schemas import BaseSchema

from .algo_name import DdAlgoName


NUW_ROWS = 'Use only first N rows of the table'
#difference_table: CSV table containing difference limits for each column
NUM_COLUMNS = 'Use only first N columns of the table'

class SplitConfig(BaseSchema):
    algo_name: Literal[DdAlgoName.Split]
    num_rows: Optional[int] = None # = Field(..., ge=1, description=NUW_ROWS)
    num_columns: Optional[int] = None # = Field(..., ge=1, description=NUM_COLUMNS)

OneOfDdAlgoConfig = Annotated[
    Union[SplitConfig],
    Field(discriminator="algo_name"),
]
