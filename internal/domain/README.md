# domain module
The `domain` module serves as the core component of the application, encapsulating the fundamental domain logic and entities.

## Purpose
The `domain` module is designed to encapsulate the core business logic and domain entities of the application. By organizing the module into submodules, the architecture maintains a clear separation of concerns, promoting scalability and ease of maintenance.

To extend or modify the domain logic, developers can add new submodules or enhance existing ones while adhering to the principles of clean architecture.


## Submodules

### Common
The `common` submodule contains shared components and utilities used across other submodules. This includes base models and common logic that can be leveraged by user, task, and file entities.

### User
The `user` submodule manages user-related entities and functionalities. It includes classes and configurations for handling user settings, authentication, and authorization, centralizing user management within the domain.

### Task
The `task` submodule provides the foundation for data profiling tasks. It includes abstract base classes and concrete implementations for different profiling algorithms.

### File
The `file` submodule handles file and dataset-related entities and operations.
