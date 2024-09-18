# Unit of Work (UoW)
This module implements the Unit of Work (UoW) pattern, which is designed to manage transactions across multiple operations. It ensures that all changes within a transaction are either successfully committed or completely rolled back in case of an error.

## What is UoW?
The Unit of Work pattern manages transactional operations within a business process. It groups multiple changes to a data store into a single logical transaction, ensuring that either all operations succeed or none do. This is particularly useful for preventing partial updates, ensuring data integrity, and managing rollbacks in case of errors.

## Implementation
The Unit Of Work class works with a DataStorageContext interface, which defines essential methods like commit, flush, rollback, and close. This allows different types of data storage (e.g., relational databases, file systems) to be plugged in while adhering to a unified transaction control mechanism.

To use UoW in your use case, you need to implement the DataStorageContext interface for your data store (if not already done), and you also need to have a repository implementation that supports working with your DataStorageContext.

### Example
```python

from typing import Protocol
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from internal.uow import UnitOfWork, DataStorageContext

class DatasetRepo(Protocol):
    def create(self, file_id: UUID, context: DataStorageContext) -> None: ...

def create_uow(context: Session) -> UnitOfWork:
    return UnitOfWork(context=context)

def create_two_datasets(
        uow: UnitOfWork,
        dataset_repo: DatasetRepo
) -> None:
    with uow as context:
        dataset_repo.create(uuid4(), context=context)
        dataset_repo.create(uuid4(), context=context)
```
