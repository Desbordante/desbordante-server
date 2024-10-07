## domain.file module
This module contains core entities for managing and handling files and datasets. It includes abstractions and utilities for working with files and offers ways to represent datasets.

## Usage
### File entity
The `File` class represents a file entity and generates a UUID for each file instance, ensuring that every file is uniquely identifiable.
Example:
```python
from domain.file import File

# Creating a new file instance
file = File()

# Access the file's UUID as a string
print(file.name)

# Access the file's UUID in UUID format
print(file.name_as_uuid)
```
