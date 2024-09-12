from uuid import uuid4, UUID


class File:
    """
    A class that represents a file with a unique identifier.
    """

    def __init__(self):
        """
        Initializes a new file instance with a unique UUID as the file's name.
        """
        self._name = uuid4()

    @property
    def name(self) -> str:
        """
        Returns the file's UUID as a string.

        Returns:
            str: The UUID of the file in string format.
        """
        return str(self._name)

    @property
    def name_as_uuid(self) -> UUID:
        """
        Returns the file's UUID as a UUID object.

        Returns:
            UUID: The UUID of the file in UUID format.
        """
        return self._name
