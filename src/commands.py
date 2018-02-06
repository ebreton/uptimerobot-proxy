"""Management commands

Usage:
    commands.py init-db [-q | -d]
    commands.py -h
    commands.py -v

Options:
    -h, --help         display this message and exit
    -v, --version      display version
    -q, --quiet        set log level to WARNING [default: INFO]
    -d, --debug        set log level to DEBUG [default: INFO]
"""
import logging

from docopt import docopt
from docopt_dispatch import dispatch

from utils import set_logging_config
from hello import app, get_storage
from settings import VERSION


@dispatch.on('init-db')
def init_db(name=None, **kwargs):
    storage = get_storage(app, storage_type="services.storage")
    app.app_context().push()
    storage.init_db()


if __name__ == '__main__':
    kwargs = docopt(__doc__)
    set_logging_config(kwargs)
    logging.debug(kwargs)
    dispatch(__doc__, version=VERSION)
