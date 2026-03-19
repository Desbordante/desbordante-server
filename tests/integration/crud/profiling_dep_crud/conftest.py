"""Shared fixtures for profiling dep CRUD tests."""

from src.crud.profiling_dep_crud.profiling_dep_crud import ProfilingDepCrud
from src.schemas.task_schemas.types import PrimitiveName


def profiling_dep_crud_factory(session, *, primitive_name: PrimitiveName):
    return ProfilingDepCrud(session=session, primitive_name=primitive_name)
