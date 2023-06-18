# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch
import unittest.mock
import unittest
from awstaga import apply

class TestAwstaga(unittest.TestCase):

    @patch('boto3.client')
    @patch('awstaga.load')
    def test_apply( # pylint: disable=too-many-arguments
            self,
            func_load,
            func_client):

        mock_client = unittest.mock.Mock()
        mock_tagset = unittest.mock.Mock()
        mock_resource = unittest.mock.Mock()
        mock_tagset_tag = unittest.mock.Mock()
        mock_resource_tag = unittest.mock.Mock()

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

        apply('awstaga.yaml')
        mock_client.tag_resources.assert_called_once_with(
            ResourceARNList=['somearn'],
            Tags={'sometagkey': 'sometagvalue', 'someresourcekey': 'someresourcevalue'}
        )
