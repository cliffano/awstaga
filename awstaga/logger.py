"""Logger for Awstaga."""
from conflog import Conflog

def init(dry_run: bool):
    """Initialize logger.
    """

    labels = ''
    if dry_run:
        labels = '[dry-run] '

    cfl = Conflog(
        conf_dict={
            'level': 'info',
            'format': f'{labels}[awstaga] %(levelname)s %(message)s'
        }
    )

    return cfl.get_logger(__name__)
