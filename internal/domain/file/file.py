from uuid import uuid4, UUID


class File:
    """
    A class that represents a file with a unique identifier.
    """

    def __init__(self):
        """
        This constructor generates a new UUID and assigns it as the file's name.
        """
        self._name = uuid4()

    @property
    def name(self) -> str:
        """
        Returns:
            str: The UUID of the file in string format.
        """
        return str(self._name)

    @property
    def name_as_uuid(self) -> UUID:
        """
        Returns:
            UUID: The file's name as a UUID object.
        """
        return self._name
