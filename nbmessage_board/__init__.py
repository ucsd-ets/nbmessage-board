import os
import sys

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