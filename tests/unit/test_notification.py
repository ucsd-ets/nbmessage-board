import unittest, datetime, os

from nbmessage_board.notification import Notification

class TestNotification(unittest.TestCase):
    def setUp(self):
        os.system('mkdir /var/lib/nbmessage-board/test')
        self.notification = Notification('test', True, datetime.datetime(2050, 1, 2))
    
    def tearDown(self):
        os.system('rm -rf /var/lib/nbmessage-board/test')
    
    def test_convert_to_dict(self):
        as_dict = dict(self.notification)
        
        assert isinstance(as_dict, dict)
        assert as_dict['expiration_date'] == 'Sun, 02 Jan 2050 12:00:00 UTC'
        assert as_dict['message_board'] == 'test'
        
    def test_expiration_date_throws_if_not_datetime(self):
        with self.assertRaises(TypeError):
            self.notification.expiration_date = 'something'