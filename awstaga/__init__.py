# pylint: disable=too-many-locals
"""
awstaga
=======
Tag any AWS resource via config file.
"""

import json
import boto3
import click
from .config import load
from .logger import init

def apply(conf_file: str, dry_run: bool, batch_size: int) -> None:
    """Apply tags to resources based on configuration file."""

    logger = init(dry_run)

    logger.info(f'Loading configuration file {conf_file}')
    conf = load(conf_file, dry_run)
    tagsets = conf[0]
    resources = conf[1]

    client = boto3.client('resourcegroupstaggingapi')

    batches = {}

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
            # Create a batch of resources with the same tags
            # the batch ID is derived from the tags dump.
            # Tags are purposely not sorted in order to distinguish
            # varying tag orders as defined by the users.
            batch_id = json.dumps(tags)
            if batch_id not in batches:
                batches[batch_id] = {'resource_arns': [], 'tags': tags}
            batches[batch_id]['resource_arns'].append(resource.get_arn())

            logger.info(f'Adding resource {resource.get_arn()} to a batch with tags {tags}')

            # Apply tags to current batch if batch_size is reached,
            # and the batch is then removed.
            if len(batches[batch_id]['resource_arns']) == batch_size:
                if dry_run is False:
                    logger.info(f'Applying {len(batches[batch_id]["resource_arns"])} resource(s) '\
                                f'with tags {batches[batch_id]["tags"]}')
                    client.tag_resources(
                        ResourceARNList=batches[batch_id]['resource_arns'],
                        Tags=batches[batch_id]['tags']
                    )
                batches.pop(batch_id)

    # Apply tags to remaining batches, each batch would have less than batch_size resources.
    for batch_id, batch in batches.items():
        if dry_run is False:
            logger.info(f'Applying {len(batch["resource_arns"])} resource(s) '\
                        f'with tags {batch["tags"]}')
            client.tag_resources(
                ResourceARNList=batch['resource_arns'],
                Tags=batch['tags']
            )

@click.command()
@click.option('--conf-file', default='awstaga.yaml', show_default=True,
              help='Configuration file path')
@click.option('--dry-run', is_flag=True, default=False, show_default=True,
              help='When dry run is enabled, no tags are applied')
@click.option('--batch-size', default=100, show_default=True,
              help='Number of resources to tag in one go per batch')
# @click.option('--force', default=False,
# help='When force is enabled, all tags are applied, existing tags are overwritten')
def cli(conf_file: str, dry_run: bool, batch_size: int) -> None:
    """Python CLI for tagging AWS resources based on a YAML configuration.
    """
    apply(conf_file, dry_run, batch_size)
