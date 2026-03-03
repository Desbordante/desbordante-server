# domain.task module

This module provides the foundational components for defining and executing data profiling tasks. It includes abstract base classes for tasks and specific implementations for different types of algorithms.

## Usage

### Task Entity

The `Task` class is an abstract base class that serves as the foundation for specific data profiling tasks. It defines the essential methods for executing algorithms and handling their results.

#### Methods:
- **`_match_algo_by_name(algo_name)`**: This method is responsible for matching and returning the appropriate algorithm instance based on the given algorithm name. This method must be implemented by subclasses to handle specific algorithms.

- **`_collect_result(algo)`**: This method processes the result obtained from the executed algorithm and returns it in a standardized format. It must be implemented by subclasses to handle the result processing specific to each task type.

- **`execute(table: pandas.DataFrame, task_config: C) -> R`**: This method runs the algorithm on the provided data table using the given configuration and returns the result. It orchestrates the workflow of loading data, executing the algorithm, and collecting results.

The `Task` class is designed to be extended by specific task implementations.
To add a new primitive to an application, implement a schema for the configuration and result of task execution, and then inherit from Task class, implementing methods **`_match_algo_by_name(algo_name)`** and **`_collect_result(algo)`**.

### FD Task Entity

The `FdTask` class is a specific implementation of the `Task` class designed for Functional Dependency (FD) profiling.

The `FdTask` class enables the execution of different FD algorithms and processes their results into the appropriate format for further use.

#### Example:
```python
from internal.domain.task import FdTask
from internal.domain.task.value_objects import FdTaskConfig, PrimitiveName
from internal.domain.task.value_objects.fd import FdAlgoName
from some_storage import table  # read dataset

task = FdTask()
config = FdTaskConfig(
    primitive_name=PrimitiveName.fd,
    config={"algo_name": FdAlgoName.FdMine},
)
result = task.execute(table, config)
```

### AFD Task Entity
The `AfdTask` class is a specific implementation of the `Task` class designed for Approximate Functional Dependency (AFD) profiling.
All capabilities are similar to the previous one, just for AFD.
#### Example:
```python
from internal.domain.task import AfdTask
from internal.domain.task.value_objects import AfdTaskConfig, PrimitiveName
from internal.domain.task.value_objects.afd import AfdAlgoName
from some_storage import table  # read dataset

task = AfdTask()
config = AfdTaskConfig(
    primitive_name=PrimitiveName.afd,
    config={"algo_name": AfdAlgoName.Pyro},
)
result = task.execute(table, config)

```
