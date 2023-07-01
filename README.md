<img align="right" src="https://raw.github.com/cliffano/awstaga/main/avatar.jpg" alt="Avatar"/>

[![Build Status](https://github.com/cliffano/awstaga/workflows/CI/badge.svg)](https://github.com/cliffano/awstaga/actions?query=workflow%3ACI)
[![Vulnerabilities Status](https://snyk.io/test/github/cliffano/awstaga/badge.svg)](https://snyk.io/test/github/cliffano/awstaga)
[![Published Version](https://img.shields.io/pypi/v/awstaga.svg)](https://pypi.python.org/pypi/awstaga)
<br/>

Awstaga
-------

Awstaga is a Python CLI for tagging AWS resources based on a YAML configuration.

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
    [awstaga] INFO Updating resource arn:aws:ssm:ap-southeast-2:123456789012:document/high-avail with tags {'CostCentre': 'FIN-123', 'Organisation': 'World Enterprise', 'Description': 'AWS Resource', 'EnvType': 'prod', 'Availability': '24x7', 'Description': 'High availability SSM document'}
    [awstaga] INFO Updating resource arn:aws:s3:::world-enterprise/development/logo.jpg with tags {'CostCentre': 'FIN-123', 'Organisation': 'World Enterprise', 'Description': 'AWS Resource', 'EnvType': 'prod', 'Availability': '24x7', 'Description': 'World Enterprise logo'}

Configuration
-------------

Configuration properties:

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
