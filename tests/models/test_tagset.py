# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
from awstaga.models.tagset import TagSet
from awstaga.models.tag import Tag

class TestTagSet(unittest.TestCase):

    def test_getters(self):
        tags = [Tag('somekey1', 'somevalue1'), Tag('somekey2', 'somevalue2')]
        tagset = TagSet('sometagset', tags)
        self.assertEqual(tagset.get_name(), 'sometagset')
        self.assertEqual(tagset.get_tags(), tags)
        self.assertEqual(len(tagset.get_tags()), 2)
        self.assertEqual(tagset.get_tags()[0].get_key(), 'somekey1')
        self.assertEqual(tagset.get_tags()[0].get_value(), 'somevalue1')
        self.assertEqual(tagset.get_tags()[1].get_key(), 'somekey2')
        self.assertEqual(tagset.get_tags()[1].get_value(), 'somevalue2')
