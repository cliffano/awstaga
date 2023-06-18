# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch, mock_open
import unittest.mock
import unittest
from awstaga.config import load

CONFIG_WITH_PROPERTIES = '''
---
tagsets:
  - name: test-tagset
    tags:
      - key: test-key1
        value: test-value1
      - key: test-key2
        value: test-value2
resources:
  - arn: test-resource-arn
    type: aws_instance
    tags:
      - key: test-key
        value: test-value
    tagsetnames:
      - test-tagset
'''

CONFIG_WITHOUT_VALUES = '''
'''

CONFIG_EMPTY = '''
---
'''

CONFIG_INVALID = '''
foo bar:
  & whoa
'''

class TestConfig(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=CONFIG_WITH_PROPERTIES)
    def test_load_with_properties(self, func): # pylint: disable=unused-argument
        with open('awstaga.yaml', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == CONFIG_WITH_PROPERTIES
        tagsets, resources = load('awstaga.yaml')
        tagset = tagsets['test-tagset']
        self.assertEqual(tagset.get_name(), 'test-tagset')
        tags = tagset.get_tags()
        self.assertEqual(len(tags), 2)
        self.assertEqual(tags[0].get_key(), 'test-key1')
        self.assertEqual(tags[0].get_value(), 'test-value1')
        self.assertEqual(tags[1].get_key(), 'test-key2')
        self.assertEqual(tags[1].get_value(), 'test-value2')
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0].get_arn(), 'test-resource-arn')
        resource_tags = resources[0].get_tags()
        self.assertEqual(len(resource_tags), 1)
        self.assertEqual(resource_tags[0].get_key(), 'test-key')
        self.assertEqual(resource_tags[0].get_value(), 'test-value')
        resource_tagset_names = resources[0].get_tagset_names()
        self.assertEqual(len(resource_tagset_names), 1)
        self.assertEqual(resource_tagset_names[0], 'test-tagset')
