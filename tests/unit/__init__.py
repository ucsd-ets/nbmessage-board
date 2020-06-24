import unittest, os, shutil

from nbmessage_board import APPLICATION_DATA_DIR



class BaseTester(unittest.TestCase):
    message_board = 'test'

    def setup_dir(self, message_board=message_board):
        try:
            os.mkdir(os.path.join(APPLICATION_DATA_DIR, self.message_board))
        except:
            pass

    def rm_dir(self, message_board=message_board):
        try:
            shutil.rmtree(os.path.join(APPLICATION_DATA_DIR, self.message_board))
        except:
            pass