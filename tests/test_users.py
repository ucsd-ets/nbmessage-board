from nbmessage_board.users import *

import unittest, os

class TestAdmin(unittest.TestCase):
    def setUp(self):
        self.admin = Admin()
    
    def tearDown(self):
        try:
            os.remove('/etc/nbmessage-board/messages/test-markdown.md')
        except:
            pass
    
    def test_add_message(self):
        # make sure the test doesn't have the output in the output folder yet
        files = os.listdir('/etc/nbmessage-board/messages')
        assert 'test-markdown.md' not in files
        
        testfile = '/opt/nbmessage-board/tests/mocks/test-markdown.md'
        self.admin.add_message(testfile)
        
        # test the postiive case
        files = os.listdir('/etc/nbmessage-board/messages')
        assert 'test-markdown.md' in files

        with self.assertRaises(FileNotFoundError):
            self.admin.add_message('/fake/path/test.md')
        
        with self.assertRaises(TypeError):
            self.admin.add_message('/opt/nbmessage-board/tests/mocks/something.txt')