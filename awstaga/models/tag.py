"""This module contains the Tag class."""

class Tag():
    """This class represents a tag.
    It contains the key and value pair of the tag.
    """

    def __init__(self, key: str, value: str) -> None:
        """Initialize the Tag object."""
        self.key = key
        self.value = value

    def get_key(self) -> str:
        """Return the key of the tag."""
        return self.key

    def get_value(self) -> str:
        """Return the value of the tag."""
        return self.value

    def __str__(self) -> str:
        """Return the string representation of the Tag object."""
        return f'{self.key}={self.value}'

    def __repr__(self) -> str:
        """Return the string representation of the Tag object."""
        return f'{self.key}={self.value}'
