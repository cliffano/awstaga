class Tag(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def get_key(self):
        """Return the key of the tag."""
        return self.key
    
    def get_value(self):
        """Return the value of the tag."""
        return self.value