import os, shutil
from bs4 import BeautifulSoup

from .etc import Config
from .message import MessageContainer, Message
from .markdown import md2html, md2bs4, html2bs4
from . import APPLICATION_DATA_DIR

class Admin:
    def __init__(self, message_board):
        self.message_board = message_board
        self.message_container = MessageContainer(self.message_board)
    
    @property
    def messages(self):
        return self.message_container
    
    def save_message_file(self):
        self.message_container.load()
        self.message_container.sort()
        html = self.message_container.render()
        
        with open(os.path.join(APPLICATION_DATA_DIR, self.message_board, 'messages.html'), 'w') as f:
            f.write(html)
        
