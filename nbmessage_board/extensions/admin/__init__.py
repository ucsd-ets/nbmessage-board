from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from tornado import web
import os, json, functools, logging

from ...base import get_directories
from ...utils import *
from ...markdown import *
from ...users import Admin
from ...message import Message, MessageContainer

def check_xsrf(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        _ = self.xsrf_token
        return f(self, *args, **kwargs)
    return wrapper

MOUNTED_MESSAGE_BOARDS = get_directories()

class AdminHandler(IPythonHandler):
    # admin = Admin()
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

            response = {}
            
            if body['message_operation'] == 'Add':
                selected_message_board = body['select_message_board']
                logging.info(f'Creating a message for {selected_message_board}')
                
                admin = Admin(selected_message_board)
                message_id = body['message_id']
                message_body = body['message_body']
                author = body['author']
                base_url = body['base_url']
                
                admin.add_message(message_id, message_body, author, base_url)
                
                response.update({
                    'preview_message_html': admin.render_messages()
                })
                
                logging.info(f'Successfully created message for {selected_message_board}')

            # set the title
            # if body['tabTitle'] != '':
            #     self.admin.set_tab_title(parse_url_path(body['tabTitle']))
            
            # # add a message
            # if body['messageOperation'] == 'Add':
            #     self.add_message(body)

            # TODO delete a message
            
            # render message back to user only if mode='staging'

            response.update({'status_code': 200})
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(response))

        except Exception as e:
            self.set_header('Content-Type', 'application/json')
            error = json.dumps({'error': str(e), 'message': self.error_message})
            logging.error(error)
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
    @check_xsrf
    def post(self, message_board):
        
        # check that the directory exists first
        if message_board not in MOUNTED_MESSAGE_BOARDS:
            raise web.HTTPError(404, f"Directory = {message_board} doesnt exist!")
        
        # breakdown the body
        body = json.loads(self.request.body.decode('utf-8'))
        # body = parse_body(body)
        
        if body['operation'] == 'add' and body['status'] == 'preview':
            # preview the message
            admin = Admin(message_board)
            message = Message(body['message_id'], body['message_body'], body['author'], base_url='/')
            admin.messages.append(message)
            self.write(admin.messages.render())
        
        elif body['operation'] == 'add' and body['status'] == 'submit':
            
            # update the message object
            admin = Admin(message_board)
            admin.messages.load_messages()
            message = Message(body['message_id'], body['message_body'], body['author'], base_url='/')
            admin.messages.append(message)
            admin.messages.sort()
            admin.messages.save()
            
            admin.save_message_file()
            self.write(f'message_id = {body["message_id"]} has been saved.')

            
    @web.authenticated
    @check_xsrf
    def delete(self, subroute):
        try:
            print(subroute)
            print('HERE')

        except Exception as e:
            logging.error(e)
            self.write({'error': str(e)})
            
class DirectoryHandler(IPythonHandler):
    @web.authenticated
    def get(self):
        self.write(json.dumps(MOUNTED_MESSAGE_BOARDS))

def load_jupyter_server_extension(nbapp):
    """
    Called during notebook start
    """
    route_pattern = url_path_join(nbapp.web_app.settings['base_url'], '/nbmessage')
    nbapp.web_app.add_handlers('.*', [
        (url_path_join(route_pattern, '/admin'), AdminHandler),
        (url_path_join(route_pattern, '/directories'), DirectoryHandler),
        (url_path_join(route_pattern, r'/messages/(\w+)'), MessagesHandler)
    ])
