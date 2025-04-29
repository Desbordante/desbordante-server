from typing import Literal, assert_never

import pandas
from desbordante.fd_verification import Highlight
from desbordante.fd_verification.algorithms import FDVerifier

from app.domain.task.schemas.base import BaseTask
from app.domain.task.schemas.afd_verification.algo_config import OneOfAfdVerificationAlgoConfig
from app.domain.task.schemas.afd_verification.algo_name import AfdVerificationAlgoName
from app.domain.task.schemas.types import PrimitiveName
from app.schemas.schemas import BaseSchema


class AfdClusterModel(BaseSchema):
    num_distinct_rhs_values: int
    most_frequent_rhs_value_proportion: float
    rows: list[list[str]]


class AfdVerificationModel(BaseSchema):
    error: float # threshold
    num_error_clusters: int
    num_error_rows: int
    clusters: list[AfdClusterModel]
    table_header: list[str]
    lhs_rhs_indices: list[int]


class BaseAfdVerificationTaskModel(BaseSchema):
    primitive_name: Literal[PrimitiveName.AFD_VERIFICATION]


class AfdVerificationTaskConfig(BaseAfdVerificationTaskModel):
    config: OneOfAfdVerificationAlgoConfig


class AfdVerificationTaskResult(BaseAfdVerificationTaskModel):
    result: AfdVerificationModel


class AfdVerificationTask(BaseTask[AfdVerificationTaskConfig, AfdVerificationTaskResult]):
    _algo_map = {
        AfdVerificationAlgoName.FDVerifier: FDVerifier,
    }

    def match_algo_by_name(self, algo_name: AfdVerificationAlgoName) -> FDVerifier:
        if algo_class := self._algo_map.get(algo_name):
            return algo_class()
        assert_never(algo_name)

    def extract_cluster(self, highlight: Highlight, table: pandas.DataFrame) -> AfdClusterModel:

        return AfdClusterModel(num_distinct_rhs_values=highlight.num_distinct_rhs_values,
                               most_frequent_rhs_value_proportion=highlight.most_frequent_rhs_value_proportion,
                               rows=[[str(table.iloc[index][j]) for j in table.columns] for index in highlight.cluster])
    
    def execute(
        self, tables: list[pandas.DataFrame], task_config: AfdVerificationTaskConfig
    ) -> AfdVerificationTaskResult:
        table = tables[0]
        columns = table.columns
        
        algo_config = task_config["config"]
        options = AfdVerificationTaskConfig.model_validate(task_config).config.model_dump(
            exclude_unset=True, exclude={"algo_name"}
        )
        #print(777, options)

        algo = self.match_algo_by_name(algo_config["algo_name"])
        algo.load_data(table=table)
        algo.execute(**options)

        return AfdVerificationTaskResult(
            primitive_name=PrimitiveName.AFD_VERIFICATION,
            result=AfdVerificationModel(error=algo.get_error(), 
                                        num_error_clusters=algo.get_num_error_clusters(),
                                        num_error_rows=algo.get_num_error_rows(),
                                        clusters=[self.extract_cluster(highlight, table) 
                                                  for highlight in algo.get_highlights()],
                                        table_header=columns,
                                        lhs_rhs_indices=options['lhs_indices'] + options['rhs_indices'])
        )
