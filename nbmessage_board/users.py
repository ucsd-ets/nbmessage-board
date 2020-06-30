"""Facades/Composites for handling server operations"""

import os, shutil, json
from bs4 import BeautifulSoup

from .etc import Config
from .message import MessageContainer, Message
from .markdown import md2html, md2bs4, html2bs4
from .notification import Notification

from . import APPLICATION_DATA_DIR

class Admin:
    def __init__(self, message_board):
        self.message_board = message_board
        self.message_container = MessageContainer(self.message_board)
    
    @property
    def messages(self):
        return self.message_container
    
    def save_message_state(self):
        self.messages.sort()
        self.messages.save()
    
    def add_message(self, message):
        self.messages.append(message)
    
    def save_message_file(self):
        self.message_container.load()
        self.message_container.sort()
        if len(self.message_container) == 0:
            html = '<div class="container nbmessage-render">No messages yet</div>'
        else:
            html = self.message_container.render()
        
        with open(os.path.join(APPLICATION_DATA_DIR, self.message_board, 'messages.html'), 'w') as f:
            f.write(html)
            
    def get_messages_for_delete(self):
        try:
            self.message_container.load()
            message_ids = self.message_container.message_ids
            rendered_message_bodies = [self.message_container.get(message_id) for message_id in message_ids]
            rendered_message_bodies = [message.render() for message in rendered_message_bodies]
            
            return dict(zip(message_ids, rendered_message_bodies))
        
        except FileNotFoundError:
            return []
    
    def delete_message(self, message_id):
        try:
            self.message_container.load()
            self.message_container.delete(message_id)
            self.message_container.save()
            self.save_message_file()
            return {'success': f'Successfully removed message ID = {message_id}'}

        except FileNotFoundError:
            return {'error': f'could not delete message ID = {message_id}'}
        

class Basic:
    def __init__(self, message_board):
        self.message_board = message_board
        self.notification = Notification(message_board)
        
    def get_notification(self):
        try:
            self.notification.load()
            return dict(self.notification)

        except FileNotFoundError:
            return {'notify': False}