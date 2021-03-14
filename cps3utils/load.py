__desc__ = '''CPS3 ROM Encryption utilty

credit:
    http://andreasnaive.blogspot.com/2007/06/cps-3-7.html 
    mamedev/mame        
'''
from array import array
from typing import BinaryIO
from . import ArrayIO,GameInfo,ROMCart,ROMType
import sys

def rotate(v, n=2):        
    v = v & 0xffff
    if n > 0:
        v = (v << n) | (v >> (16-n))
    else:
        v = (v >> abs(n)) | (v << (16-abs(n)))
    return v & 0xffff    
def rotxor(v, x):
    r = (v+rotate(v, 2)) & 0xffff
    r = rotate(r, 4) ^ (r & (v ^ x))
    return r & 0xffff
def cps3_encryption_mask(addr, key1, key2):        
    addr ^= key1
    v = (addr & 0xffff) ^ 0xffff
    v = rotxor(v, key2 & 0xffff)
    v ^= (addr >> 16) ^ 0xffff
    v = rotxor(v, key2 >> 16)
    v ^= (addr & 0xffff) ^ (key2 & 0xffff)
    return (v | (v << 16)) & 0xffffffff    
progress_rate = 5 # rate: 2**progress_rate times during entire conversion
class LoadRom(BinaryIO):
    '''CP System III built-in encryption wrapper'''
    def __init__(self,stream : BinaryIO,cart : ROMCart,game : GameInfo):       
        '''Initalizes the wrapper with another stream. All the modifications
        will be made to the said stream.

        Args:
            stream (BinaryIO): A stream of the ROM. e.g. FileIO, BinaryIO
            cart (ROMCart): The ROMCart object correspond to the stream
            game (GameInfo): The game of the ROM
        '''                
        self.game = game 
        self.cart = cart
        if isinstance(stream,bytes) or isinstance(stream,bytearray):            
            self.stream = ArrayIO(stream) # ArrayIO allows us to make modifications in-place
        else:
            self.stream = stream        
    def mask_bytes(self,offset,buffer,progress=None):        
        '''masks bytes inplace'''
        start_offset = -(offset % 4)
        bi,mi,length = 0,0,len(buffer) # buffer index,mask index,buffer length
        while bi < length:
            u32 = cps3_encryption_mask(mi + self.cart.rom_type + offset + start_offset,self.game.KEY1,self.game.KEY2)
            if start_offset < 0:start_offset += 1 # to skip some unused bytes
            elif bi < length:
                buffer[bi] = buffer[bi] ^ (u32 >> 24 & 0xff) ; bi+=1
            if start_offset < 0:start_offset += 1
            elif bi < length:
                buffer[bi] = buffer[bi] ^ (u32 >> 16 & 0xff) ; bi+=1
            if start_offset < 0:start_offset += 1
            elif bi < length:
                buffer[bi] = buffer[bi] ^ (u32 >> 8 & 0xff) ; bi+=1
            if start_offset < 0:start_offset += 1
            elif bi < length:
                buffer[bi] = buffer[bi] ^ (u32 >> 0 & 0xff) ; bi+=1                    
            mi += 4
            if progress and bi % (length >> progress_rate) == 0:progress(bi,length) # reports 2^4 times
    '''API methods'''
    def read(self,n=-1,show_progress=False,mask_non_gfx=True) -> array:
        '''Reads certain amount of bytes at current cursor

        Args:
            n (int): Length to be read
            show_progress (bool): Report progress while *masking*. Defaults to False
            mask_non_gfx (bool): Masks the PRG / BIOS buffer. Set to false if no decryption is needed. Defaults to True
        '''                    
        offset = self.stream.tell()
        buffer = array('B',self.stream.read(n))
        if not self.cart.rom_type is ROMType.GFX and mask_non_gfx: # don't mask GFX roms
            self.mask_bytes(offset,buffer,lambda now,all:sys.stderr.write('Reading : %s / %s\n' % (now,all)) if show_progress else None)
        return buffer
    def write(self, buffer,show_progress=False,mask_non_gfx=True) -> int:        
        '''Write certain amount of bytes at current cursor,overrides existing content

        Args:
            buffer (bytes): What to be written
            show_progress (bool): Report progress while *masking*. Defaults to False
            mask_non_gfx (bool): Masks the PRG / BIOS buffer. Set to false if no decryption is needed. Defaults to True
        '''                    
        offset = self.stream.tell()
        buffer = array('B',buffer)
        if not self.cart.rom_type is ROMType.GFX and mask_non_gfx:
            self.mask_bytes(offset,buffer,lambda now,all:sys.stderr.write('Writing : %s / %s\n' % (now * 100 / all)) if show_progress else None)
        return self.stream.write(buffer)
    '''fallback API methods'''
    fallback = {'close','closed','fileno','flush','isatty','mode','name','readable','seek','seekable','tell','truncate','writable'}
    def __getattribute__(self, name: str):
        if name in LoadRom.fallback:            
            return self.stream.__getattribute__(name)
        else:
            return super().__getattribute__(name)        