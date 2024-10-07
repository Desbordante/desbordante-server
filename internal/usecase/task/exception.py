class TaskNotFoundException(Exception):
    """
    Exception raised when a task is not found in data storage.

    This exception does not require any additional attributes beyond the default message.
    """

    def __init__(self):
        """
        Initializes an instance of TaskNotFoundException without any specific message.

        The default message "Task not found" is used.
        """
        super().__init__("Task not found")
