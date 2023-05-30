import boto3
from awstaga.config import load as load_config

def apply_tags(conf_file):

    conf = load_config(conf_file)
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

        print(f'Tagging resource {resource.arn} with tags {tags} ...')
        client.tag_resources(ResourceARNList=[resource.arn], Tags=tags)
