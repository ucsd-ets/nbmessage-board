import os, shutil
from .etc import Config

class Admin:
    def __init__(self):
        self.publish_mode = 'blah'

    def remove_message(self, name):
        pass
    
    def get_messages(self):
        pass
    
    def add_message(self, message_fp):
        if not os.path.exists(message_fp): raise FileNotFoundError(f'Could not find file at {message_fp}')
        if not message_fp.endswith('.md'): raise TypeError('File must have .md extension')
        
        basefile = os.path.basename(message_fp)
        
        shutil.copyfile(message_fp, f'/etc/nbmessage-board/messages/{basefile}')
        
    
    def remove_all_messages(self):
        pass
    
    def set_tab_title(self, tab_title):
        if tab_title == '': raise TypeError('tab_title must not be an empty string')
        
        c = Config()
        c.update_config({'tab_title': tab_title})
