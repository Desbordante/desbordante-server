from typing import Annotated

from fastapi import Depends

from src.api.dependencies import FileCrudDep, VerifiedUserDep
from src.usecases.file.upload_file import UploadFileUseCase


def get_upload_file_use_case(
    file_crud: FileCrudDep,
    user: VerifiedUserDep,
) -> UploadFileUseCase:
    return UploadFileUseCase(file_crud=file_crud, user=user)


UploadFileUseCaseDep = Annotated[UploadFileUseCase, Depends(get_upload_file_use_case)]


# def get_get_datasets_use_case(
#     dataset_crud: DatasetCrudDep,
#     user: AuthorizedUserDep,
# ) -> GetDatasetsUseCase:
#     return GetDatasetsUseCase(dataset_crud=dataset_crud, user=user)


# GetDatasetsUseCaseDep = Annotated[
#     GetDatasetsUseCase, Depends(get_get_datasets_use_case)
# ]
