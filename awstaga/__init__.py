"""
awstaga
=======
Tag any AWS resource via config file.
"""

import boto3
import click
from .config import load

def apply(conf_file: str) -> None:
    """Apply tags to resources based on configuration file."""

    print('Loading configuration ...')
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

        print(f'Tagging resource {resource.get_arn()} with tags {tags} ...')
        client.tag_resources(ResourceARNList=[resource.get_arn()], Tags=tags)

@click.command()
@click.option('--conf-file', default='awstaga.yaml', help='Configuration file')
# @click.option('--dry-run', default=False, help="The person to greet.")
# @click.option('--force', default=False, help="Number of greetings.")
def cli(conf_file: str) -> None:
    """CLI entry point for applying tags to AWS resources
    based on configuration file.
    """
    apply(conf_file)
