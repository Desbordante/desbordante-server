import pytest
import pandas as pd
import logging
from polyfactory.factories.pydantic_factory import ModelFactory

from internal.domain.task import FdTask
from internal.domain.task.value_objects import FdTaskConfig, PrimitiveName
from internal.domain.task.value_objects.fd import FdAlgoName


@pytest.mark.parametrize("algo_name", [algo_name.value for algo_name in FdAlgoName])
@pytest.mark.parametrize(
    "table",
    [pd.read_csv("tests/datasets/university_fd.csv", sep=",", header=0)],
)
def test_with_default_params(algo_name, table):
    task = FdTask()
    config = FdTaskConfig(
        primitive_name=PrimitiveName.fd,
        config={"algo_name": algo_name},  # type: ignore
    )
    logging.info(config)
    result = task.execute(table, config)
    logging.info(result)


@pytest.mark.parametrize(
    "table", [pd.read_csv("tests/datasets/university_fd.csv", sep=",", header=0)]
)
def test_with_faked_params(table):
    task = FdTask()
    config_factory = ModelFactory.create_factory(FdTaskConfig)
    config = config_factory.build(factory_use_construct=True)
    logging.info(config)
    result = task.execute(table, config)
    logging.info(result)
