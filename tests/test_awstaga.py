# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch, call
import unittest.mock
import unittest
from awstaga import apply

class TestAwstaga(unittest.TestCase):

    @patch('time.sleep')
    @patch('boto3.client')
    @patch('awstaga.load')
    @patch('awstaga.init')
    def test_apply( # pylint: disable=too-many-arguments
            self,
            func_init,
            func_load,
            func_client,
            func_sleep):

        mock_logger = unittest.mock.Mock()
        mock_client = unittest.mock.Mock()
        mock_tagset = unittest.mock.Mock()
        mock_resource = unittest.mock.Mock()
        mock_tagset_tag = unittest.mock.Mock()
        mock_resource_tag = unittest.mock.Mock()

        func_init.return_value = mock_logger
        func_client.return_value = mock_client
        func_load.return_value = (
            { 'sometagsetname': mock_tagset },
            [mock_resource]
        )

        mock_resource.get_arn.return_value = 'somearn'
        mock_resource_tag.get_key.return_value = 'someresourcekey'
        mock_resource_tag.get_value.return_value = 'someresourcevalue'
        mock_tagset_tag.get_key.return_value = 'sometagkey'
        mock_tagset_tag.get_value.return_value = 'sometagvalue'
        mock_resource.get_tagset_names.return_value = ['sometagsetname']
        mock_tagset.get_tags.return_value = [mock_tagset_tag]
        mock_resource.get_tags.return_value = [mock_resource_tag]
        mock_client.tag_resources.return_value = {}

        apply(conf_file='awstaga.yaml', dry_run=False, batch_size=20, delay=3)

        self.assertEqual(mock_logger.info.call_count, 3)
        mock_logger.info.assert_has_calls([
            call('Loading configuration file awstaga.yaml'),
            call('Adding resource somearn to a batch with tags ' \
                "{'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}"),
            call("Applying 1 resource(s) with tags "\
                 "{'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}")
        ])
        # should call tag_resources once as part of remaining batches
        mock_client.tag_resources.assert_called_once_with(
            ResourceARNList=['somearn'],
            Tags={'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}
        )
        func_sleep.assert_called_once_with(3)

    @patch('time.sleep')
    @patch('boto3.client')
    @patch('awstaga.load')
    @patch('awstaga.init')
    def test_apply_with_enabled_dry_run( # pylint: disable=too-many-arguments
            self,
            func_init,
            func_load,
            func_client,
            func_sleep):

        mock_logger = unittest.mock.Mock()
        mock_client = unittest.mock.Mock()
        mock_tagset = unittest.mock.Mock()
        mock_resource = unittest.mock.Mock()
        mock_tagset_tag = unittest.mock.Mock()
        mock_resource_tag = unittest.mock.Mock()

        func_init.return_value = mock_logger
        func_client.return_value = mock_client
        func_load.return_value = (
            { 'sometagsetname': mock_tagset },
            [mock_resource]
        )

        mock_resource.get_arn.return_value = 'somearn'
        mock_resource_tag.get_key.return_value = 'someresourcekey'
        mock_resource_tag.get_value.return_value = 'someresourcevalue'
        mock_tagset_tag.get_key.return_value = 'sometagkey'
        mock_tagset_tag.get_value.return_value = 'sometagvalue'
        mock_resource.get_tagset_names.return_value = ['sometagsetname']
        mock_tagset.get_tags.return_value = [mock_tagset_tag]
        mock_resource.get_tags.return_value = [mock_resource_tag]

        apply(conf_file='awstaga.yaml', dry_run=True, batch_size=20, delay=2)

        self.assertEqual(mock_logger.info.call_count, 2)
        mock_logger.info.assert_has_calls([
            call('Loading configuration file awstaga.yaml'),
            call('Adding resource somearn to a batch with tags ' \
                "{'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}")
        ])
        mock_client.tag_resources.assert_not_called()
        func_sleep.assert_not_called()

    @patch('time.sleep')
    @patch('boto3.client')
    @patch('awstaga.load')
    @patch('awstaga.init')
    def test_apply_with_batch_size_2( # pylint: disable=too-many-arguments
            self,
            func_init,
            func_load,
            func_client,
            func_sleep):

        mock_logger = unittest.mock.Mock()
        mock_client = unittest.mock.Mock()
        mock_tagset = unittest.mock.Mock()
        mock_resource1 = unittest.mock.Mock()
        mock_resource2 = unittest.mock.Mock()
        mock_resource3 = unittest.mock.Mock()
        mock_resource4 = unittest.mock.Mock()
        mock_tagset_tag = unittest.mock.Mock()
        mock_resource_tag = unittest.mock.Mock()

        func_init.return_value = mock_logger
        func_client.return_value = mock_client
        func_load.return_value = (
            { 'sometagsetname': mock_tagset },
            [mock_resource1, mock_resource2, mock_resource3, mock_resource4]
        )

        mock_resource1.get_arn.return_value = 'somearn1'
        mock_resource2.get_arn.return_value = 'somearn2'
        mock_resource3.get_arn.return_value = 'somearn3'
        mock_resource4.get_arn.return_value = 'somearn4'
        mock_resource_tag.get_key.return_value = 'someresourcekey'
        mock_resource_tag.get_value.return_value = 'someresourcevalue'
        mock_tagset_tag.get_key.return_value = 'sometagkey'
        mock_tagset_tag.get_value.return_value = 'sometagvalue'
        mock_resource1.get_tagset_names.return_value = ['sometagsetname']
        mock_resource2.get_tagset_names.return_value = ['sometagsetname']
        mock_resource3.get_tagset_names.return_value = ['sometagsetname']
        mock_resource4.get_tagset_names.return_value = ['sometagsetname']
        mock_tagset.get_tags.return_value = [mock_tagset_tag]
        mock_resource1.get_tags.return_value = [mock_resource_tag]
        mock_resource2.get_tags.return_value = [mock_resource_tag]
        mock_resource3.get_tags.return_value = [mock_resource_tag]
        mock_resource4.get_tags.return_value = [mock_resource_tag]
        mock_client.tag_resources.return_value = {}

        apply(conf_file='awstaga.yaml', dry_run=False, batch_size=2, delay=2)

        self.assertEqual(mock_logger.info.call_count, 7)
        mock_logger.info.assert_has_calls([
            call('Loading configuration file awstaga.yaml'),
            call('Adding resource somearn1 to a batch with tags ' \
                "{'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}"),
            call('Adding resource somearn2 to a batch with tags ' \
                "{'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}"),
            call('Applying 2 resource(s) with tags '\
                 "{'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}"),
            call('Adding resource somearn3 to a batch with tags ' \
                "{'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}"),
            call('Adding resource somearn4 to a batch with tags ' \
                "{'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}"),
            call('Applying 2 resource(s) with tags '\
                 "{'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}")
        ])
        # should call tag_resources twice as part of the batches
        mock_client.tag_resources.assert_has_calls([
            call(ResourceARNList=['somearn1', 'somearn2'],
                 Tags={'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}),
            call(ResourceARNList=['somearn3', 'somearn4'],
                 Tags={'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'})
        ])
        func_sleep.assert_has_calls([
            call(2),
            call(2)
        ])

    @patch('time.sleep')
    @patch('boto3.client')
    @patch('awstaga.load')
    @patch('awstaga.init')
    def test_apply_with_error( # pylint: disable=too-many-arguments
            self,
            func_init,
            func_load,
            func_client,
            func_sleep):

        mock_logger = unittest.mock.Mock()
        mock_client = unittest.mock.Mock()
        mock_tagset = unittest.mock.Mock()
        mock_resource = unittest.mock.Mock()
        mock_tagset_tag = unittest.mock.Mock()
        mock_resource_tag = unittest.mock.Mock()

        func_init.return_value = mock_logger
        func_client.return_value = mock_client
        func_load.return_value = (
            { 'sometagsetname': mock_tagset },
            [mock_resource]
        )

        mock_resource.get_arn.return_value = 'somearn'
        mock_resource_tag.get_key.return_value = 'someresourcekey'
        mock_resource_tag.get_value.return_value = 'someresourcevalue'
        mock_tagset_tag.get_key.return_value = 'sometagkey'
        mock_tagset_tag.get_value.return_value = 'sometagvalue'
        mock_resource.get_tagset_names.return_value = ['sometagsetname']
        mock_tagset.get_tags.return_value = [mock_tagset_tag]
        mock_resource.get_tags.return_value = [mock_resource_tag]
        mock_client.tag_resources.return_value = {
            'FailedResourcesMap': {
                'somearn': {
                    'StatusCode': 400,
                    'ErrorCode': 'Throttling',
                    'ErrorMessage': 'Rate exceeded'
                }
            }
        }

        apply(conf_file='awstaga.yaml', dry_run=False, batch_size=20, delay=2)

        self.assertEqual(mock_logger.info.call_count, 3)
        mock_logger.info.assert_has_calls([
            call('Loading configuration file awstaga.yaml'),
            call('Adding resource somearn to a batch with tags ' \
                "{'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}"),
            call("Applying 1 resource(s) with tags "\
                 "{'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}")
        ])
        mock_logger.error.assert_has_calls([
            call('Failed to apply tags to 1 resource(s):'),
            call('somearn: 400 - Throttling - Rate exceeded')
        ])
        # should call tag_resources once as part of remaining batches
        mock_client.tag_resources.assert_called_once_with(
            ResourceARNList=['somearn'],
            Tags={'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}
        )
        func_sleep.assert_called_once_with(2)
