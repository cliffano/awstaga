# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch, call, mock_open
import unittest.mock
import unittest
import yaml
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

CONFIG_WITH_PROPERTIES_HAVING_RESOURCE_WITHOUT_TAGS = '''
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
    tagsetnames:
      - test-tagset
'''

CONFIG_WITH_PROPERTIES_HAVING_RESOURCE_WITHOUT_TAGSETNAMES = '''
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
'''

CONFIG_WITH_PROPERTIES_WITHOUT_TAGSETS = '''
---
resources:
  - arn: test-resource-arn
    type: aws_instance
    tags:
      - key: test-key
        value: test-value
'''

CONFIG_WITH_PROPERTIES_HAVING_INCLUDES = '''
---
tagsets:
  - !include include.d/tagset.yaml
resources: !include include.d/resources.yaml
'''

CONFIG_INCLUDE_TAGSET = '''
---
name: test-tagset
tags:
  - key: test-key
    value: test-value
  - key: test-key2
    value: test-value2
'''

CONFIG_INCLUDE_RESOURCES = '''
---
- arn: test-resource-1a
  type: aws_instance
  tags:
    - key: test-key
      value: test-value-1a
  tagsetnames:
    - test-tagset
- arn: test-resource-1b
  type: aws_instance
  tags:
    - key: test-key
      value: test-value-1b
  tagsetnames:
    - test-tagset
- arn: test-resource-2a
  type: aws_instance
  tags:
    - key: test-key
      value: test-value-2a
  tagsetnames:
    - test-tagset
- arn: test-resource-2b
  type: aws_instance
  tags:
    - key: test-key
      value: test-value-2b
  tagsetnames:
    - test-tagset
- arn: test-resource-2c
  type: aws_instance
  tags:
    - key: test-key
      value: test-value-2c
  tagsetnames:
    - test-tagset
'''

CONFIG_WITHOUT_VALUES = '''
---
tagsets:
resources:
'''

CONFIG_EMPTY = '''
'''

CONFIG_INVALID = '''
foo bar:
  & whoa
'''

class TestConfig(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=CONFIG_WITH_PROPERTIES)
    @patch('awstaga.config.init')
    def test_load_with_properties(self, func_init, func_open): # pylint: disable=unused-argument
        with open('awstaga.yaml', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == CONFIG_WITH_PROPERTIES

        mock_logger = unittest.mock.Mock()

        func_init.return_value = mock_logger

        tagsets, resources = load('awstaga.yaml', False)
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

        self.assertEqual(mock_logger.info.call_count, 2)
        mock_logger.info.assert_has_calls([
            call('Loading 1 tagset(s)...'),
            call('Loading 1 resource(s)...')
        ])

        self.assertEqual(mock_logger.debug.call_count, 2)
        mock_logger.debug.assert_has_calls([
            call('Loaded tagset test-tagset with tags '\
                 '(test-key1=test-value1, test-key2=test-value2)'),
            call('Loaded resource test-resource-arn with tags '\
                 "(test-key=test-value,) and tagsetnames ('test-tagset',)")
        ])

    @patch('builtins.open', new_callable=mock_open,
           read_data=CONFIG_WITH_PROPERTIES_HAVING_RESOURCE_WITHOUT_TAGS)
    @patch('awstaga.config.init')
    def test_load_with_properties_having_resource_without_tags(self, func_init, func_open): # pylint: disable=unused-argument
        with open('awstaga.yaml', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == CONFIG_WITH_PROPERTIES_HAVING_RESOURCE_WITHOUT_TAGS

        mock_logger = unittest.mock.Mock()

        func_init.return_value = mock_logger

        tagsets, resources = load('awstaga.yaml', False)
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
        self.assertEqual(len(resource_tags), 0)

        resource_tagset_names = resources[0].get_tagset_names()
        self.assertEqual(len(resource_tagset_names), 1)
        self.assertEqual(resource_tagset_names[0], 'test-tagset')

        self.assertEqual(mock_logger.info.call_count, 2)
        mock_logger.info.assert_has_calls([
            call('Loading 1 tagset(s)...'),
            call('Loading 1 resource(s)...')
        ])

        self.assertEqual(mock_logger.debug.call_count, 2)
        mock_logger.debug.assert_has_calls([
            call('Loaded tagset test-tagset with tags '\
                 '(test-key1=test-value1, test-key2=test-value2)'),
            call("Loaded resource test-resource-arn with tagsetnames ('test-tagset',)")
        ])

    @patch('builtins.open', new_callable=mock_open,
           read_data=CONFIG_WITH_PROPERTIES_HAVING_RESOURCE_WITHOUT_TAGSETNAMES)
    @patch('awstaga.config.init')
    def test_load_with_properties_having_resource_without_tagsetnames(self, func_init, func_open): # pylint: disable=unused-argument
        with open('awstaga.yaml', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == CONFIG_WITH_PROPERTIES_HAVING_RESOURCE_WITHOUT_TAGSETNAMES

        mock_logger = unittest.mock.Mock()

        func_init.return_value = mock_logger

        tagsets, resources = load('awstaga.yaml', False)
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
        self.assertEqual(len(resource_tagset_names), 0)

        self.assertEqual(mock_logger.info.call_count, 2)
        mock_logger.info.assert_has_calls([
            call('Loading 1 tagset(s)...'),
            call('Loading 1 resource(s)...')
        ])

        self.assertEqual(mock_logger.debug.call_count, 2)
        mock_logger.debug.assert_has_calls([
            call('Loaded tagset test-tagset with tags '\
                 '(test-key1=test-value1, test-key2=test-value2)'),
            call('Loaded resource test-resource-arn with tags '\
                 "(test-key=test-value,)")
        ])

    @patch('builtins.open', new_callable=mock_open,
           read_data=CONFIG_WITH_PROPERTIES_WITHOUT_TAGSETS)
    @patch('awstaga.config.init')
    def test_load_with_properties_without_tagsets(self, func_init, func_open): # pylint: disable=unused-argument
        with open('awstaga.yaml', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == CONFIG_WITH_PROPERTIES_WITHOUT_TAGSETS

        mock_logger = unittest.mock.Mock()

        func_init.return_value = mock_logger

        tagsets, resources = load('awstaga.yaml', False)
        self.assertEqual(tagsets, {})
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0].get_arn(), 'test-resource-arn')

        resource_tags = resources[0].get_tags()
        self.assertEqual(len(resource_tags), 1)
        self.assertEqual(resource_tags[0].get_key(), 'test-key')
        self.assertEqual(resource_tags[0].get_value(), 'test-value')

        resource_tagset_names = resources[0].get_tagset_names()
        self.assertEqual(len(resource_tagset_names), 0)

        self.assertEqual(mock_logger.info.call_count, 1)
        mock_logger.info.assert_has_calls([
            call('Loading 1 resource(s)...')
        ])

        self.assertEqual(mock_logger.debug.call_count, 1)
        mock_logger.debug.assert_has_calls([
            call('Loaded resource test-resource-arn with tags '\
                 "(test-key=test-value,)")
        ])

    @patch('builtins.open', new_callable=mock_open)
    @patch('awstaga.config.init')
    def test_load_with_properties_having_includes(self, func_init, func_open): # pylint: disable=unused-argument
        func_open.side_effect = [
            _mock_file(CONFIG_WITH_PROPERTIES_HAVING_INCLUDES),
            _mock_file(CONFIG_INCLUDE_RESOURCES),
            _mock_file(CONFIG_INCLUDE_TAGSET)
        ]

        tagsets, resources = load('awstaga.yaml', False)
        tagset = tagsets['test-tagset']
        self.assertEqual(tagset.get_name(), 'test-tagset')

        tags = tagset.get_tags()
        self.assertEqual(len(tags), 2)
        self.assertEqual(tags[0].get_key(), 'test-key')
        self.assertEqual(tags[0].get_value(), 'test-value')
        self.assertEqual(tags[1].get_key(), 'test-key2')
        self.assertEqual(tags[1].get_value(), 'test-value2')
        self.assertEqual(len(resources), 5)
        self.assertEqual(resources[0].get_arn(), 'test-resource-1a')
        self.assertEqual(len(resources[0].get_tags()), 1)
        self.assertEqual(resources[0].get_tags()[0].get_key(), 'test-key')
        self.assertEqual(resources[0].get_tags()[0].get_value(), 'test-value-1a')
        self.assertEqual(len(resources[0].get_tagset_names()), 1)
        self.assertEqual(resources[0].get_tagset_names()[0], 'test-tagset')
        self.assertEqual(resources[1].get_arn(), 'test-resource-1b')
        self.assertEqual(resources[1].get_tags()[0].get_key(), 'test-key')
        self.assertEqual(resources[1].get_tags()[0].get_value(), 'test-value-1b')
        self.assertEqual(len(resources[1].get_tagset_names()), 1)
        self.assertEqual(resources[1].get_tagset_names()[0], 'test-tagset')
        self.assertEqual(resources[2].get_arn(), 'test-resource-2a')
        self.assertEqual(resources[2].get_tags()[0].get_key(), 'test-key')
        self.assertEqual(resources[2].get_tags()[0].get_value(), 'test-value-2a')
        self.assertEqual(len(resources[2].get_tagset_names()), 1)
        self.assertEqual(resources[2].get_tagset_names()[0], 'test-tagset')
        self.assertEqual(resources[3].get_arn(), 'test-resource-2b')
        self.assertEqual(resources[3].get_tags()[0].get_key(), 'test-key')
        self.assertEqual(resources[3].get_tags()[0].get_value(), 'test-value-2b')
        self.assertEqual(len(resources[3].get_tagset_names()), 1)
        self.assertEqual(resources[3].get_tagset_names()[0], 'test-tagset')
        self.assertEqual(resources[4].get_arn(), 'test-resource-2c')
        self.assertEqual(resources[4].get_tags()[0].get_key(), 'test-key')
        self.assertEqual(resources[4].get_tags()[0].get_value(), 'test-value-2c')
        self.assertEqual(len(resources[4].get_tagset_names()), 1)
        self.assertEqual(resources[4].get_tagset_names()[0], 'test-tagset')

    @patch('builtins.open', new_callable=mock_open, read_data=CONFIG_WITHOUT_VALUES)
    @patch('awstaga.config.init')
    def test_load_without_values(self, func_init, func_open): # pylint: disable=unused-argument
        with open('awstaga.yaml', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == CONFIG_WITHOUT_VALUES

        mock_logger = unittest.mock.Mock()

        func_init.return_value = mock_logger

        tagsets, resources = load('awstaga.yaml', False)
        self.assertEqual(tagsets, {})
        self.assertEqual(resources, [])

        self.assertEqual(mock_logger.warning.call_count, 2)
        mock_logger.warning.assert_has_calls([
            call('No tagsets found in configuration file'),
            call('No resources found in configuration file')
        ])

    @patch('builtins.open', new_callable=mock_open, read_data=CONFIG_EMPTY)
    def test_load_empty_config(self, func_open): # pylint: disable=unused-argument
        with open('awstaga.yaml', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == CONFIG_EMPTY

        tagsets, resources = load('awstaga.yaml', False)
        self.assertEqual(tagsets, {})
        self.assertEqual(resources, [])

    @patch('builtins.open', new_callable=mock_open, read_data=CONFIG_INVALID)
    def test_load_invalid_config(self, func_open): # pylint: disable=unused-argument
        with open('awstaga.yaml', 'r', encoding='utf8') as file_handle:
            assert file_handle.read() == CONFIG_INVALID
        with self.assertRaises(yaml.scanner.ScannerError):
            load('awstaga.yaml', False)

def _mock_file(file_content):
    mock = mock_open(read_data=file_content)
    mock.return_value.__iter__ = lambda self: iter(self.readline, b'')
    return mock.return_value
