"""Configuration loader.
"""

from typing import Tuple
import yaml
from .models.resource import Resource
from .models.tag import Tag
from .models.tagset import TagSet
from .logger import init

def load(conf_file: str) -> Tuple[dict, list]: # pylint: disable=too-many-locals
    """Load configuration values from file.
    """

    logger = init()

    tagsets = {}
    resources = []
    with open(conf_file, 'r', encoding='utf-8') as stream:
        conf_yaml = yaml.safe_load(stream)
        if conf_yaml is not None:
            for key, value in conf_yaml.items():

                if key == 'tagsets':
                    logger.info('Loading tagsets...')
                    for tagset in value:
                        name = tagset['name']
                        tags = []
                        for tag in tagset['tags']:
                            tags.append(Tag(tag['key'], tag['value']))
                        logger.debug(f'Loaded tagset {name} with tags {*tags,}')
                        tagsets[name] = TagSet(name, tags)

                elif key == 'resources':
                    logger.info('Loading resources...')
                    for resource in value:
                        arn = resource['arn']
                        tags = []
                        for tag in resource['tags']:
                            tags.append(Tag(tag['key'], tag['value']))
                        tagset_names = []
                        for tagsetname in resource['tagsetnames']:
                            tagset_names.append(tagsetname)
                        logger.debug(f'Loaded resource {arn} with '\
                                     f'tags {*tags,} and tagsetnames {*tagset_names,}')
                        resources.append(Resource(arn, tags, tagset_names))

    return tagsets, resources
