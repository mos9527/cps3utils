import argparse
from typing import BinaryIO
__version__ = '0.0.5'

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
