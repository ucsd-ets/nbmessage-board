from nbmessage_board.base import *

import unittest, os, sqlite3

DBFILE = '/var/lib/nbmessage-board/test/nbmessage_board.db'
NEWDIR = '/var/lib/nbmessage-board/test2'

class TestGetDirectories(unittest.TestCase):
    def setUp(self):
        self.adddir()

    def tearDown(self):
        self.rmdir()
    
    def adddir(self):
        try:
            os.mkdir(NEWDIR)
        except:
            pass
    
    def rmdir(self):
        try:
            os.rmdir(NEWDIR)
        except:
            pass
    
    def test_get_directories(self):
        self.rmdir()
        directories = get_directories()
        
        assert 'sql' not in directories, 'sql is in the directory'
        assert 'test2' not in directories, 'mock directory is listed'
        
        self.adddir()
        
        directories = get_directories()
        assert 'test2' in directories, 'mock directory needs to be listed'