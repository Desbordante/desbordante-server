# data_storage module
This module is responsible for managing the configuration and settings related to data storage in the application. It serves as a central place for handling all database-related configurations and ensures that the rest of the application can access these configurations seamlessly.

## Structure
### settings
`settings.py` contains all the settings for working with the data store. Through them you can get the URL to connect to the database, file paths, and so on.

### context
This module(`data_storage`) and all its submodules that represent some kind of storage must contain an implementation of the context - a “bridge” between the repositories and the data storage system. The context accumulates data within itself and provides transactions

`context.py` contains a unique context that encapsulates the logic of all other contexts.

### relational
The `flat` module contains the logic for interacting with local file storages. [Read more.](flat/README.md)

### relational
The `relational` module contains the logic for interacting with relational databases using SQLAlchemy. [Read more.](relational/README.md)

## Extensibility
If you need to add a new database or other data storage, simply create the appropriate module with the implementation in this module, and also write all the necessary settings in `settings.py`.
You should also implement a context for your repository and extend a unique context for it.
