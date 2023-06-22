# pylint: disable=too-many-locals
"""
awstaga
=======
Tag any AWS resource via config file.
"""

import boto3
import click
from .config import load
from .logger import init

def apply(conf_file: str) -> None:
    """Apply tags to resources based on configuration file."""

    logger = init()

    logger.info(f'Loading configuration file {conf_file}')
    conf = load(conf_file)
    tagsets = conf[0]
    resources = conf[1]

    client = boto3.client('resourcegroupstaggingapi')

    for resource in resources:
        tags = {}

        for tagset_name in resource.get_tagset_names():
            tagset = tagsets[tagset_name]
            for tagset_tag in tagset.get_tags():
                tags[tagset_tag.get_key()] = tagset_tag.get_value()

        for resource_tag in resource.get_tags():
            tags[resource_tag.get_key()] = resource_tag.get_value()

        if not tags:
            logger.warning(f'No tags to apply to resource {resource.get_arn()}')
        else:
            logger.info(f'Updating resource {resource.get_arn()} with tags {tags}')
            client.tag_resources(ResourceARNList=[resource.get_arn()], Tags=tags)

@click.command()
@click.option('--conf-file', default='awstaga.yaml', help='Configuration file path')
# @click.option('--dry-run', default=False, help='When dry run is enabled, no tags are applied')
# @click.option('--force', default=False,
# help='When force is enabled, all tags are applied, existing tags are overwritten')
def cli(conf_file: str) -> None:
    """CLI entry point for applying tags to AWS resources
    based on configuration file.
    """
    apply(conf_file)
