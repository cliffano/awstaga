<img align="right" src="https://raw.github.com/cliffano/awstaga/main/avatar.jpg" alt="Avatar"/>

[![Build Status](https://github.com/cliffano/awstaga/workflows/CI/badge.svg)](https://github.com/cliffano/awstaga/actions?query=workflow%3ACI)
[![Security Status](https://snyk.io/test/github/cliffano/awstaga/badge.svg)](https://snyk.io/test/github/cliffano/awstaga)
[![Published Version](https://img.shields.io/pypi/v/awstaga.svg)](https://pypi.python.org/pypi/awstaga)
<br/>

Awstaga
-------

Awstaga is a Python CLI for tagging AWS resources based on a YAML configuration.

This package is intended as a companion for [AWS Tag Editor](https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging-resources.html). While AWS Tag Editor is useful for tagging multiple resources in one go, it has no easy way to re-run the tagging since you have to use the AWS console UI, and its resource filtering capability is quite limited, making it hard to select resources with-more-than basic logic.

Using Awstaga, you can easily re-run the tagging by running the CLI again. And with its support of YAML configuration, it allows you to define multiple tagsets which you can reuse and mix and match with the resources, you can construct your own mapping between the resources and the relevant tags and tagsets. You can generate your own YAML configuration using Python scripts, or any other programming language, allowing you to construct a more complex filtering logic.

Installation
------------

    pip3 install awstaga

Usage
-----

Create a configuration file, e.g. `awstaga.yaml`:

    ---
    tagsets:
      - name: common
        tags:
          - key: CostCentre
            value: FIN-123
          - key: Organisation
            value: World Enterprise
          - key: Description
            value: AWS Resource
      - name: prod
        tags:
          - key: EnvType
            value: prod
          - key: Availability
            value: 24x7
      - name: nonprod
        tags:
          - key: EnvType
            value: non-prod
          - key: Availability
            value: on-demand
    resources:
      - arn: 'arn:aws:ssm:ap-southeast-2:123456789012:document/high-avail'
        tags:
          - key: Description
            value: High availability SSM document
        tagsetnames:
          - common
          - prod
      - arn: 'arn:aws:s3:::world-enterprise/development/logo.jpg'
        tags:
          - key: Description
            value: World Enterprise logo
        tagsetnames:
          - common
          - nonprod

And then run `awstaga` CLI and pass the configuration file path:

    awstaga --conf-file awstaga.yaml

It will write the log messages to stdout:

    [awstaga] INFO Loading configuration file awstaga.yaml
    [awstaga] INFO Loading 3 tagset(s)...
    [awstaga] INFO Loading 2 resource(s)...
    [awstaga] INFO Adding resource arn:aws:ssm:ap-southeast-2:123456789012:document/high-avail to a batch with tags {'CostCentre': 'FIN-123', 'Organisation': 'World Enterprise', 'Description': 'AWS Resource', 'EnvType': 'prod', 'Availability': '24x7', 'Description': 'High availability SSM document'}
    [awstaga] INFO Adding resource arn:aws:s3:::world-enterprise/development/logo.jpg to a batch with tags {'CostCentre': 'FIN-123', 'Organisation': 'World Enterprise', 'Description': 'AWS Resource', 'EnvType': 'prod', 'Availability': '24x7', 'Description': 'World Enterprise logo'}

And if the tagging failed (e.g. due to rate exceeded), it will log the following error messages:

    [awstaga] ERROR Failed to apply tags to 1 resource(s):
    [awstaga] ERROR arn:aws:ssm:ap-southeast-2:123456789012:document/high-avail: 400 - Throttling - Rate exceeded
    [awstaga] ERROR arn:aws:s3:::world-enterprise/development/logo.jpg: 400 - Throttling - Rate exceeded

### Dry run

You can also run Awstaga in dry-run mode by adding `--dry-run` flag:

    awstaga --conf-file awstaga.yaml --dry-run

During dry-run mode, Awstaga log messages will be labeled with `[dry-run]`:

    [dry-run] [awstaga] INFO Loading configuration file awstaga.yaml
    [dry-run] [awstaga] INFO Loading 3 tagset(s)...
    [dry-run] [awstaga] INFO Loading 2 resource(s)...
    [dry-run] [awstaga] INFO Adding resource arn:aws:ssm:ap-southeast-2:123456789012:document/high-avail to a batch with tags {'CostCentre': 'FIN-123', 'Organisation': 'World Enterprise', 'Description': 'AWS Resource', 'EnvType': 'prod', 'Availability': '24x7', 'Description': 'High availability SSM document'}

### YAML includes

Awstaga supports YAML includes using , so you can split your configuration into multiple files:

    ---
    tagsets:
      - !include include.d/tagset.yaml
    resources: !include include.d/resources.yaml

Include files should be put under `include.d/`` folder relative to the configuration file.

The included tagset file `include.d/tagset.yaml`:

    ---
    name: common
    tags:
      - key: CostCentre
        value: FIN-123
      - key: Organisation
        value: World Enterprise
      - key: Description
        value: AWS Resource

The included resources file `include.d/resources.yaml`:

    ---
    - arn: 'arn:aws:ssm:ap-southeast-2:123456789012:document/high-avail'
      tags:
        - key: Description
          value: High availability SSM document
      tagsetnames:
        - common
        - prod
    - arn: 'arn:aws:s3:::world-enterprise/development/logo.jpg'
      tags:
        - key: Description
          value: World Enterprise logo
      tagsetnames:
        - common
        - nonprod

### Batch size

In order to optimise the number of API calls, resources with identical tags are put into batches. By default, the batch size is 20.
You can run Awstaga with a custom batch size `--batch-size <number>` flag:

    awstaga --conf-file awstaga.yaml --batch-size 10

### Delay

In order to avoid rate exceeded error, you can run Awstaga with a custom delay `--delay <number>` flag:

    awstaga --conf-file awstaga.yaml --delay 5

By default, the delay is 2 seconds.

Configuration
-------------

These are the configuration properties that you can use with `awstaga` CLI.
Some example configuration files are available on [examples](examples) folder.

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `tagsets[]` | Array | A list of one or more tagsets. Any tagset can be associated with any resource, and the resource will include the tags specified in the tagset. | |
| `tagsets[].name` | String | The name of the tagset. | `common` |
| `tagsets[].tags[]` | Array | A list of one or more key-value pair tags within the tagset. | |
| `tagsets[].tags[].key` | String | The tag key. | `CostCentre` |
| `tagsets[].tags[].value` | String | The tag value. | `FIN-123` |
| `resources[]` | Array | A list of one or more AWS resources. Each of the resource has a corresponding list of tags, along with the tags from tagsets. | |
| `resources[].arn` | String | AWS resource [ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html). | `arn:aws:s3:::world-enterprise/development/logo.jpg` |
| `resources[].tags[]` | Array | A list of one or more key-value pair tags of the resource. | |
| `resources[].tags[].key` | String | The tag key. | `Description` |
| `resources[].tags[].value` | String | The tag value. | `Some description` |
| `resources[].tagsetnames[]` | Array | A list of one or more tagset names. All tags within the tagsets specified are included in the resource. | |

Colophon
--------

[Developer's Guide](https://cliffano.github.io/developers_guide.html#python)

Build reports:

* [Lint report](https://cliffano.github.io/awstaga/lint/pylint/index.html)
* [Code complexity report](https://cliffano.github.io/awstaga/complexity/wily/index.html)
* [Unit tests report](https://cliffano.github.io/awstaga/test/pytest/index.html)
* [Test coverage report](https://cliffano.github.io/awstaga/coverage/coverage/index.html)
* [Integration tests report](https://cliffano.github.io/awstaga/test-integration/pytest/index.html)
* [API Documentation](https://cliffano.github.io/awstaga/doc/sphinx/index.html)
