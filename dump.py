import sys
from array import array
from typing import BinaryIO,IO

from __init__ import GameInfo,create_default_parser,locate_game_by_name

class ROMType:
    BIOS   = 0x0
    PRG_10 = 0x6000000
    PRG_20 = 0x6800000

class Cps3IO(BinaryIO):
    '''CP System III built-in encryption wrapper'''
    def __init__(self,stream : BinaryIO,rom_type : ROMType,game : GameInfo):       
        '''Initalizes the wrapper with another stream. All the modifications
        will be made to the said stream.

        Args:
            stream (BinaryIO): A stream of the ROM. e.g. FileIO, BinaryIO
            rom_type (ROMType): The type of the encrypted ROM
            game (GameInfo): The game of the ROM
        '''
        self.init_offset = rom_type        
        self.game = game 
        self.stream = stream       
        super().__init__()    
    @staticmethod
    def rotate_bits_16(v, n=2):
        '''bit rotation in both directions,n>0 goes left-wise'''
        v = v & 0xffff
        if n > 0:
            v = (v << n) | (v >> (16-n))
        else:
            v = (v >> abs(n)) | (v << (16-abs(n)))
        return v & 0xffff
    @staticmethod
    def rotate_xor_16(v, x):
        '''rotation xor'''
        r = (v+Cps3IO.rotate_bits_16(v, 2)) & 0xffff
        r = Cps3IO.rotate_bits_16(r, 4) ^ (r & (v ^ x))
        return r & 0xffff
    @staticmethod
    def cps3_generate_xor_mask_32(addr, key1, key2):
        '''cps3 rotation xor masker'''
        addr ^= key1
        v = (addr & 0xffff) ^ 0xffff
        v = Cps3IO.rotate_xor_16(v, key2 & 0xffff)
        v ^= (addr >> 16) ^ 0xffff
        v = Cps3IO.rotate_xor_16(v, key2 >> 16)
        v ^= (addr & 0xffff) ^ (key2 & 0xffff)
        return (v | (v << 16)) & 0xffffffff
    def masks(self,offset,length,func,big=True):
        '''create u8 masks,calls func for each mask value. `big` means the masks will be outputed in big-endian'''
        start_offset = -(offset % 4)
        read,i = 0,0
        while read < length:
            u32 = self.cps3_generate_xor_mask_32(i + self.init_offset + offset + start_offset,self.game.KEY1,self.game.KEY2)
            if start_offset < 0:start_offset += 1 # the following bytes are outputed in big-endian order
            elif read < length:
                func(u32 >> (0+big*24) & 0xff)
                read+=1
            if start_offset < 0:start_offset += 1
            elif read < length:
                func(u32 >> (8+big*8) & 0xff)
                read+=1
            if start_offset < 0:start_offset += 1
            elif read < length:
                func(u32 >> (16-big*8) & 0xff)
                read+=1
            if start_offset < 0:start_offset += 1
            elif read < length:
                func(u32 >> (24-big*24) & 0xff)
                read+=1                    
            i += 4
    '''API methods'''
    def read_unmasked(self,n=-1):
        '''`read()` without masking the data'''    
        return self.stream.read(n)
    def write_unmasked(self,v):
        '''`write()` without masking the data'''    
        return self.stream.write(v)
    def read(self,n=-1,show_progress=False) -> array:
        '''`read()` from the stream, then mask the output'''
        offset = self.stream.tell()
        buffer = array('B',self.stream.read(n)) # read fisrt , then return the buffer        
        n = 0
        def mask(m):            
            nonlocal n
            buffer[n] = buffer[n] ^ m
            n += 1    
            if show_progress:
                if n % (len(buffer) >> 8) == 0:
                    sys.stderr.write('Reading : %.2f%%           \r' % (n * 100 / len(buffer)))
        self.masks(offset,len(buffer),mask)            
        return buffer
    def write(self, buffer,show_progress=False) -> int:
        '''`write()` to the stream, then mask the output'''
        offset = self.stream.tell()
        buffer = array('B',buffer) # mask first,then overwrite the buffer    
        n = 0
        def mask(m):
            nonlocal n
            buffer[n] = buffer[n] ^ m
            n += 1
            if show_progress:
                if n % (len(buffer) >> 8) == 0:
                    sys.stderr.write('Writing : %.2f%%            \r' % (n * 100 / len(buffer)))
        self.masks(offset,len(buffer),mask) 
        return self.stream.write(buffer)
    fallback = {'close','closed','fileno','flush','isatty','mode','name','readable','seek','seekable','tell','truncate','writable'}
    def __getattribute__(self, name: str):
        if name in Cps3IO.fallback:            
            return self.stream.__getattribute__(name)
        else:
            return super().__getattribute__(name)        

if __name__ == '__main__':
    parser = create_default_parser('CPS3 ROM Decryption / Encryption tool')    
    parser.add_argument('input',metavar='IN',help='Encrypted / Decrypted game ROM path')
    parser.add_argument('output',metavar='OUT',help='Decrypted / Encrypted game ROM path')
    parser.add_argument('type',metavar='TYPE',help='ROM Type (10,20,or BIOS)',default='10')

    args = parser.parse_args()
    args = args.__dict__    

    game = locate_game_by_name(args['game'])    
    romtype = 0x00
    sys.stderr.write('Dumping game rom for : %s...' % game.GAMENAME)        
    if args['type']=='10':
        sys.stderr.write('ROM Type : ROM 10\n')
        romtype = ROMType.PRG_10
    elif args['type']=='20':
        sys.stderr.write('ROM Type : ROM 20\n')
        romtype = ROMType.PRG_20
    else:
        sys.stderr.write('ROM Type : BIOS\n')
        romtype = ROMType.BIOS
    cps3 = Cps3IO(open(args['input'],'rb'),romtype,game)
    data = cps3.read(show_progress=True)
    data.tofile(open(args['output'], 'wb'))
