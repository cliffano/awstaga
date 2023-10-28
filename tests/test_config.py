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
