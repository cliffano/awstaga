class Resource(object):
    def __init__(self, arn, tags, tagset_names):
        self.arn = arn
        self.tags = tags
        self.tagsetnames = tagset_names
    
    def get_arn(self):
        """Return the ARN of the resource."""
        return self.arn

    def get_tags(self):
        """Return the tags."""
        return self.tags
  
    def get_tagset_names(self):
        """Return the TagSet names."""
        return self.tagsetnames
