# usecase module
This module implements the core business logic, acting as a bridge between domain entities and or infrastructure. This module defines the key use cases, which handle interactions between different components of the system, ensuring that the business logic remains independent of implementation details.

## submodules

`file` - contains usecases and usecases' exceptions related to files and datasets, their creation, management, search, and more.

`task` - contains usecases and usecases' exceptions related to tasks, their creation, launch, verification, and more.

`user` - contains usecases and usecases' exceptions related to the user, authorization and other user actions.

## How to create new usecase
### 1. Create DTO schemas
Create Data Transfer Object (DTO) schemas in `usecase.dto` to standardize the data flow between your use case and the repository.

### 2. Define the Repository Interface Using `Protocol`
All repository interfaces must be created using Python’s `Protocol` to ensure type safety and flexibility in implementation.

### 3. Implement the usecase
Implement the use case. The use case should manage domain entities directly but interact with repositories, services, and external components strictly through interfaces.

### 4. Implement data storage context
Implement interface `DataStorageContext` for your data storage. Place it in the `internal.infrastructure.data_storage` module.

### 4. Implement the repository
If the repository isn't implemented, you will need to provide a concrete implementation for the repository interface. Place this in the `internal.repository` module.
