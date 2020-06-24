"""Shared methods or any shared objects/funcs"""

from abc import ABCMeta, abstractproperty
import os

from . import APPLICATION_DATA_DIR, DATA_DIR_IGNORE_DIRS

def get_directories():
    """list of all nbmessage_board directories"""
    items = os.listdir(APPLICATION_DATA_DIR)

    # ignore certain user defined directories
    for directory_to_ignore in DATA_DIR_IGNORE_DIRS:
        if directory_to_ignore in items:
            ind = items.index(directory_to_ignore)
            items.pop(ind)
    
    return items

