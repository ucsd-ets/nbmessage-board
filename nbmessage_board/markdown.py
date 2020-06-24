""""convert markdown to html"""
from markdown2 import Markdown
from typing import List
from dateutil import parser
from bs4 import BeautifulSoup
import os, bs4, time

from .etc import Config
from . import APPLICATION_DATA_DIR

def read_md(mdpath) -> str:
    if not os.path.isfile(mdpath): raise FileNotFoundError(f'markdown path = {mdpath} doesnt exist!')
    if not mdpath.endswith('.md'): raise TypeError(f'file {mdpath} must be an .md file')

    with open(mdpath, 'r') as f:
        mdfile = f.readlines()
        mdfile = ''.join(mdfile)
    
    return mdfile
    
def md2html(md) -> str:
    markdowner = Markdown()
    return markdowner.convert(md)

def md2bs4(md: str) -> BeautifulSoup:
    md = md2html(md)
    return BeautifulSoup(md, 'html.parser')

def html2bs4(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, 'html.parser')

def decorate_message(html, author, timestamp, base_url):
    decorated_message = f"""
    <div class="row col-md-8 padding-bottom-sm main-border">
        {html}
        <div class="col-xs-4 nbmessage-background">
            <div class="col-xs-12 user-fmt">
                <p><i id="timestamp">{timestamp}</i></p>
            </div>
            <div class="col-xs-2 nbmessage-thumbnail">
                <img src="{os.path.join(base_url, 'nbmessage/images/ucsd-0.png')}" class="img-fluid img-thumbnail" alt="...">
            </div>
            <div class="col-xs-10" style="padding-top: .3em">
                <h4 class="user-fmt">{author}</h4>
            </div>
        </div>
    </div>
    """
    return decorated_message
        
