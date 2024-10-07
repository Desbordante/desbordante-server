# repository module
This module contains implementations of all repositories.
To implement your repository, create a module here for the repository that the repository works with (or use an existing one), and then implement the repository WITHOUT inheriting from interfaces. It is important that in the repository implementation all operations occur through the universal context from the `internal.infrastructure.data_storage` directory.
