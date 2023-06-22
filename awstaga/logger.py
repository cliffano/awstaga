"""Logger for Awstaga."""
import os
from conflog import Conflog

def init():
    """Initialize logger.
    """
    os.environ['CONFLOG_LEVEL'] = 'info'
    os.environ['CONFLOG_FORMAT'] = '[awstaga] %(levelname)s %(message)s'
    cfl = Conflog()
    return cfl.get_logger(__name__)
