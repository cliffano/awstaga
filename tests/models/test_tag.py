# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
from awstaga.models.tag import Tag


class TestTag(unittest.TestCase):

    def test_getters(self):
        tag = Tag("somekey", "somevalue")
        self.assertEqual(tag.get_key(), "somekey")
        self.assertEqual(tag.get_value(), "somevalue")
        self.assertEqual(str(tag), "somekey=somevalue")
        self.assertEqual(repr(tag), "somekey=somevalue")
