from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from internal.rest.http.file.di import get_retrieve_dataset_use_case
from internal.usecase.file import RetrieveDataset

router = APIRouter()


class ResponseSchema(BaseModel):
    id: UUID
    file_id: UUID
    separator: str
    header: list[int]


@router.post("/dataset/{dataset_id}", response_model=ResponseSchema)
def retrieve_dataset(
    dataset_id: UUID,
    retrieve_dataset_use_case: RetrieveDataset = Depends(get_retrieve_dataset_use_case),
) -> ResponseSchema:
    dataset = retrieve_dataset_use_case(dataset_id=dataset_id)

    return ResponseSchema(
        id=dataset.id,
        file_id=dataset.file_id,
        separator=dataset.separator,
        header=dataset.header,
    )
