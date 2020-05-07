""""convert markdown to html"""
from markdown2 import Markdown
import os

def read_md(mdpath):
    if not os.path.isfile(mdpath): raise FileNotFoundError(f'markdown path = {mdpath} doesnt exist!')
    if not mdpath.endswith('.md'): raise TypeError(f'file {mdpath} must be an .md file')

    with open(mdpath, 'r') as f:
        mdfile = f.readlines()
        mdfile = ''.join(mdfile)
    
    return mdfile
    
def md2html(md):
    markdowner = Markdown()
    return markdowner.convert(md)

def render_messages():
    basedir = '/etc/nbmessage-board'
    messages = os.listdir(os.path.join(basedir, 'messages'))
    html = ''
    for message in messages:
        md = read_md(os.path.join(basedir, 'messages', message))
        as_html = md2html(md)
        html = html + as_html
        
    return html
    
    