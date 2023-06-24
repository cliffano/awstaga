"""Configuration loader.
"""

from typing import Tuple
import yaml
from .models.resource import Resource
from .models.tag import Tag
from .models.tagset import TagSet
from .logger import init

def load(conf_file: str) -> Tuple[dict, list]:
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
                    if value is not None:
                        logger.info(f'Loading {len(value)} tagset(s)...')
                        _load_tagsets(logger, tagsets, value)
                    else:
                        logger.warning('No tagsets found in configuration file')

                elif key == 'resources':
                    if value is not None:
                        logger.info(f'Loading {len(value)} resource(s)...')
                        _load_resources(logger, resources, value)
                    else:
                        logger.warning('No resources found in configuration file')

    return tagsets, resources

def _load_tagsets(logger, tagsets: dict, tagsets_conf: list) -> None:
    for tagset in tagsets_conf:
        name = tagset['name']
        tags = []
        for tag in tagset['tags']:
            tags.append(Tag(tag['key'], tag['value']))
        logger.debug(f'Loaded tagset {name} with tags {*tags,}')
        tagsets[name] = TagSet(name, tags)

def _load_resources(logger, resources: list, resources_conf: list) -> None:
    for resource in resources_conf:
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
