"""Logger for Awstaga."""
from conflog import Conflog

def init():
    """Initialize logger.
    """
    cfl = Conflog(
        conf_dict={
            'level': 'info',
            'format': '[awstaga] %(levelname)s %(message)s'
        }
    )
    return cfl.get_logger(__name__)
