import argparse
from random import choices
from typing import BinaryIO
__version__ = '0.0.2'
class ArrayIO(BinaryIO):
    '''In-place BinaryIO Wrapper for bytearray and alikes'''
    n = 0
    def __init__(self,array : bytearray) -> None:
        self.array = array
    def seek(self,offset,whence=0):
        self.n = self.n * whence + offset
    def tell(self):
        return self.n
    def read(self,n=-1):
        n = n if n >= 0 and self.tell() + n <= len(self.array) else len(self.array) - self.tell()                
        slice_ = self.array[self.tell():self.tell() + n]
        self.n += n
        return slice_
    def write(self,b):
        b = b if self.tell() + len(b) <= len(self.array) else b[:len(self.array) - self.tell()]
        self.array[self.tell():len(b)] = b
        return len(b)    
from .games import *
'''CLI Utilites - compatibility for enviorments with or without Gooey'''
gooey_installed = False
try:
    from gooey import Gooey,GooeyParser
    gooey_installed = True
except:pass
parser = None
def create_parser(description='<default tool name>'):
    '''Creates an `rgparser` with `game` as its first positional argument'''    
    global parser
    if gooey_installed:
        parser = GooeyParser(description=description)
    else:
        parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('game', metavar='GAME',help='CPS3 Game shortname',choices=[game.__name__.split('.')[-1] for game in GAMES])
    return parser
gooey_whitelist = {'widget'}
def parser_add_argument(*a,**kw):
    if not gooey_installed:kw = {k:v for k,v in kw.items if k not in gooey_whitelist}
    return parser.add_argument(*a,**kw)
def parser_parse_args():
    return parser.parse_args()
def enter(main_func):
    if gooey_installed:        
        Gooey(
            progress_regex=r"(?P<curr>(?:\d*)) */ *(?P<all>(?:\d*))",
            progress_expr="curr * 100 / all"
        )(main_func)()
    else:
        main_func()