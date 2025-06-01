# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import logging
import unittest
from awstaga.logger import init


class TesLogger(unittest.TestCase):

    def test_init(self):

        logger = init(False)
        assert isinstance(logger, logging.LoggerAdapter) is True

    def test_init_with_enabled_dry_run(self):

        logger = init(True)
        assert isinstance(logger, logging.LoggerAdapter) is True
