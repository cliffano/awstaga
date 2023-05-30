# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
import unittest
from awstaga.awstaga import (
    apply_tags,
)

class TestCb(unittest.TestCase):

    def test_get_logger_with_single_conf_file(self): # pylint: disable=unused-argument
        apply_tags(conf_file='tests-integration/fixtures/cb.yaml')