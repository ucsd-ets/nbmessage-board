from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler, AuthenticatedFileHandler
from tornado import web


def load_jupyter_server_extension(nbapp):
    """
    Called during notebook start
    """
    route_pattern = url_path_join(nbapp.web_app.settings['base_url'], '/nbmessage')
    nbapp.web_app.add_handlers('.*', [(route_pattern + '/(.*)', web.StaticFileHandler, {'path': '/etc/nbmessage-board/static/'})])