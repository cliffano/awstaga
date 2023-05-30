class TagSet(object):
    def __init__(self, name, tags):
        """Initialize the TagSet object."""
        self.name = name
        self.tags = tags

    def get_name(self):
        """Return the name of the tag set."""
        return self.name

    def get_tags(self):
        """Return the tags."""
        return self.tags
