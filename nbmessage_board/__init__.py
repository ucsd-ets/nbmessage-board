import os
import sys
from .etc import Config
__version__ = '0.1.0'

APPLICATION_DATA_DIR = '/var/lib/nbmessage-board'
CONFIG_DIR = '/etc/nbmessage-board'

_config = Config().config
DATA_DIR_IGNORE_DIRS = _config['data_dirs_to_ignore']

def _jupyter_nbextension_paths():
    paths = [
        dict(
            section="tree",
            src=os.path.join('nbextensions', 'message'),
            dest="message",
            require="message/main"
        ),
        dict(
            section="tree",
            src=os.path.join('nbextensions', 'admin'),
            dest="admin",
            require="admin/main"
        )
    ]

    return paths


def _jupyter_server_extension_paths():
    paths = [
        dict(module="nbmessage_board.extensions.message"),
        dict(module="nbmessage_board.extensions.admin")
    ]

    return paths