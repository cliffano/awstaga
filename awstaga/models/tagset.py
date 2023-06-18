"""This module contains the TagSet class."""

class TagSet():
    """This class represents a TagSet.
    It contains the name of the TagSet and the tags that belong to .
    """

    def __init__(self, name: str, tags: list) -> None:
        """Initialize the TagSet object."""
        self.name = name
        self.tags = tags

    def get_name(self) -> str:
        """Return the name of the tag set."""
        return self.name

    def get_tags(self) -> list:
        """Return the tags on this tag set."""
        return self.tags
