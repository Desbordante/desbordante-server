## Data transfer objects
This module contains the schemas and exceptions used to transfer data from usecase application layer to another.

### repository
The `repostory` submodule contains schemas for passing data between usecases and repositories - objects that provide an abstraction for working with data stores.

In order to comply with some regularity, when creating new schemes in this submodule, we recommend starting the name of the scheme with a noun - describing the entity to which the scheme relates. For example: **FileCreateSchema**.

### worker
The `worker` submodule contains circuits for passing data between usecases and the worker, an object that provides an abstraction for working with background tasks.

In order to follow a certain pattern, when creating new schemes in this submodule, we recommend starting the name of the scheme with a verb - describing the action of the background task to which the scheme relates. For example: **ProfilingTaskCreateSchema**.
