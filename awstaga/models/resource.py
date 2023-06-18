"""This module contains the Resource class."""

class Resource():
    """This class represents the resource to be tagged.
    It contains the ARN of the resource, the tags to be applied to the resource,
    and the names of the TagSets to be applied to the resource.
    """

    def __init__(self, arn: str, tags: list, tagset_names: list) -> None:
        """Initialize the Resource object."""
        self.arn = arn
        self.tags = tags
        self.tagsetnames = tagset_names

    def get_arn(self) -> str:
        """Return the ARN of the resource."""
        return self.arn

    def get_tags(self) -> list:
        """Return the tags that should be applied to this resource."""
        return self.tags

    def get_tagset_names(self) -> list:
        """Return the names of the tag sets which contain the tags that
        should be applied to this resource."""
        return self.tagsetnames
