from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler, AuthenticatedFileHandler
from tornado import web
import json, os

from ...base import get_directories
from ... import APPLICATION_DATA_DIR

MOUNTED_MESSAGE_BOARDS = get_directories()

class ShowMessage(IPythonHandler):
    @web.authenticated
    def get(self, message_board):
        if message_board in MOUNTED_MESSAGE_BOARDS:
            try:
                with open(os.path.join(APPLICATION_DATA_DIR, message_board, 'messages.html'), 'r') as f:
                    html = f.readlines()
                    html = ''.join(html)
                
                response = {'html': html}
                
                self.write(json.dumps(response))
            except Exception as e:
                raise web.HTTPError(404, f'No messages yet')
    
        else:
            raise web.HTTPError(404, f"Directory = {message_board} doesnt exist!")


def load_jupyter_server_extension(nbapp):
    """
    Called during notebook start
    """
    route_pattern = url_path_join(nbapp.web_app.settings['base_url'], '/nbmessage')
    nbapp.web_app.add_handlers('.*', [
        (url_path_join(route_pattern, r'/render/(\w+)'), ShowMessage)
    ])
    nbapp.web_app.add_handlers('.*', [(route_pattern + '/(.*)', web.StaticFileHandler, {'path': f'{APPLICATION_DATA_DIR}/static/'})])