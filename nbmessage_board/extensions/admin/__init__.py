from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from tornado import web
import os, json, functools

from ...utils import *
from ...markdown import *
from ...users import Admin

def check_xsrf(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        _ = self.xsrf_token
        return f(self, *args, **kwargs)
    return wrapper

class AdminHandler(IPythonHandler):
    admin = Admin()
    error_message = ''

    @web.authenticated
    @check_xsrf
    def post(self):
        """
        Calculate and return current resource usage metrics
        """
        # 1. validate file path
        # 2. if valid, copy file to dir
        # 3. validate 2
        # 4. send ok response and html if true
        try:
            body = self.request.body.decode('utf-8')
            body = parse_body(body)
            print(body)
            
            # set the title
            if body['tabTitle'] != '':
                self.admin.set_tab_title(parse_url_path(body['tabTitle']))
            
            # add a message
            if body['messageOperation'] == 'Add':
                self.add_message(body)

            # TODO delete a message
            
            # render message back to user only if mode='staging'

            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps({'success': 200}))

        except Exception as e:
            self.set_header('Content-Type', 'application/json')
            error = json.dumps({'error': str(e), 'message': self.error_message})
            self.write(error)
        
    def get(self):
        yaml = load_yaml('/etc/nbmessage-board/nbmessage-board-config.yaml');
        title = yaml.pop('tab_title')
        self.write(json.dumps(title))
    
    def add_message(self, body):
        try:
            filepath = parse_url_path(body['newMessageFilePath'])
            self.admin.add_message(filepath)

        except Exception as e:
            self.error_message = str(e)
            raise Exception('newMessageFilePath')


class MessagesHandler(IPythonHandler):
    @web.authenticated
    def get(self):
        messages = os.listdir('/etc/nbmessage-board/messages')
        self.write(json.dumps(messages))

def load_jupyter_server_extension(nbapp):
    """
    Called during notebook start
    """
    route_pattern = url_path_join(nbapp.web_app.settings['base_url'], '/nbmessage')
    
    nbapp.web_app.add_handlers('.*', [(url_path_join(route_pattern, '/admin'), AdminHandler)])
    nbapp.web_app.add_handlers('.*', [(url_path_join(route_pattern, '/messages'), MessagesHandler)])