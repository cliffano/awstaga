"""Configuration loader.
"""
from typing import Tuple
import yaml
from .models.resource import Resource
from .models.tag import Tag
from .models.tagset import TagSet

def load(conf_file: str) -> Tuple[dict, list]:
    """Load configuration values from file.
    """
    tagsets = {}
    resources = []
    with open(conf_file, 'r', encoding='utf-8') as stream:
        conf_yaml = yaml.safe_load(stream)
        if conf_yaml is not None:
            for key, value in conf_yaml.items():
                if key == 'tagsets':
                    for tagset in value:
                        name = tagset['name']
                        tags = []
                        for tag in tagset['tags']:
                            tags.append(Tag(tag['key'], tag['value']))
                        tagsets[name] = TagSet(name, tags)
                elif key == 'resources':
                    for resource in value:
                        arn = resource['arn']
                        tags = []
                        for tag in resource['tags']:
                            tags.append(Tag(tag['key'], tag['value']))
                        tagsetnames = []
                        for tagsetname in resource['tagsetnames']:
                            tagsetnames.append(tagsetname)
                        resources.append(Resource(arn, tags, tagsetnames))
    return tagsets, resources
