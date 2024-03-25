from app.domain.task.fd import FdTask, FdTaskConfig
import pytest
import pandas as pd
import logging
from polyfactory.factories.pydantic_factory import ModelFactory

# TODO: change when optional fields are suported
# @pytest.mark.parametrize(
#     "table", [pd.read_csv("tests/datasets/university_fd.csv", sep=",", header=0)]
# )
# def test_with_default_params(task_cls, table):
#     task = FdTask()
#     result = task.execute(table)
#     logging.info(result)


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
