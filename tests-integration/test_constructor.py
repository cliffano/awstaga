# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import os
import unittest
import botocore
from awstaga import apply

class TestConstructor(unittest.TestCase):

    def setUp(self):
        os.unsetenv('AWS_DEFAULT_REGION')
        if 'AWS_DEFAULT_REGION' in os.environ:
            os.environ.pop('AWS_DEFAULT_REGION')
        os.unsetenv('AWS_ACCESS_KEY_ID')
        if 'AWS_ACCESS_KEY_ID' in os.environ:
            os.environ.pop('AWS_ACCESS_KEY_ID')
        os.unsetenv('AWS_SECRET_ACCESS_KEY')
        if 'AWS_SECRET_ACCESS_KEY' in os.environ:
            os.environ.pop('AWS_SECRET_ACCESS_KEY')

    def test_constructor_without_aws_region(self):
        # should raise no region error
        with self.assertRaises(botocore.exceptions.NoRegionError):
            apply('tests-integration/fixtures/awstaga.yaml')

    def test_constructor_with_aws_region_without_keys(self):
        os.environ['AWS_DEFAULT_REGION'] = 'ap-southeast-2'
        # should raise client error
        with self.assertRaises(botocore.exceptions.ClientError):
            apply('tests-integration/fixtures/awstaga.yaml')

    def test_constructor_with_aws_region_with_invalid_keys(self):
        os.environ['AWS_DEFAULT_REGION'] = 'ap-southeast-2'
        os.environ['AWS_ACCESS_KEY_ID'] = 'someaccesskeyid'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'somesecretaccesskey'
        # should raise client error
        with self.assertRaises(botocore.exceptions.ClientError):
            apply('tests-integration/fixtures/awstaga.yaml')
