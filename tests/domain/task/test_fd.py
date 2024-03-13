from app.domain.task.fd import fd_factory
import pytest
import pandas as pd
import logging
from polyfactory.factories.pydantic_factory import ModelFactory


@pytest.mark.parametrize("task_cls", fd_factory.get_all())
@pytest.mark.parametrize(
    "table", [pd.read_csv("tests/datasets/university_fd.csv", sep=",", header=0)]
)
def test_with_default_params(task_cls, table):
    task = task_cls(table)
    result = task.execute()
    logging.info(result)


@pytest.mark.parametrize("task_cls", fd_factory.get_all())
@pytest.mark.parametrize(
    "table", [pd.read_csv("tests/datasets/university_fd.csv", sep=",", header=0)]
)
def test_with_faked_params(task_cls, table):
    task = task_cls(table)
    config_factory = ModelFactory.create_factory(model=task_cls.config_model_cls)
    config = config_factory.build(factory_use_construct=True)
    logging.info(config)
    result = task.execute(config)
    logging.info(result)
