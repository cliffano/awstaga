# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
from awstaga.models.resource import Resource
from awstaga.models.tag import Tag


class TestResource(unittest.TestCase):

    def test_getters(self):
        tags = [Tag("somekey1", "somevalue1"), Tag("somekey2", "somevalue2")]
        resource = Resource("somearn", tags, ["sometagsetname1", "sometagsetname2"])
        self.assertEqual(resource.get_arn(), "somearn")
        self.assertEqual(resource.get_tags(), tags)
        self.assertEqual(len(resource.get_tags()), 2)
        self.assertEqual(resource.get_tags()[0].get_key(), "somekey1")
        self.assertEqual(resource.get_tags()[0].get_value(), "somevalue1")
        self.assertEqual(resource.get_tags()[1].get_key(), "somekey2")
        self.assertEqual(resource.get_tags()[1].get_value(), "somevalue2")
        self.assertEqual(
            resource.get_tagset_names(), ["sometagsetname1", "sometagsetname2"]
        )
        self.assertEqual(len(resource.get_tagset_names()), 2)
        self.assertEqual(resource.get_tagset_names()[0], "sometagsetname1")
        self.assertEqual(resource.get_tagset_names()[1], "sometagsetname2")
