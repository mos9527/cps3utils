import sys
from array import array
from __init__ import *
import __init__

def to_unit32(u8_buf: array):
    '''copies file buffer (u8) into another buffer (u32)'''
    arr = array('I')
    arr.frombytes(u8_buf)
    arr.byteswap()  # values are in big-endian,swap them
    return arr

def rotate_bits(v, n=2):
    '''bit rotation in both directions,n>0 goes left-wise (u16)'''
    v = v & 0xffff
    if n > 0:
        v = (v << n) | (v >> (16-n))
    else:
        v = (v >> abs(n)) | (v << (16-abs(n)))
    return v & 0xffff

def rotate_xor(v, x):
    '''rotation xor (u16)'''
    r = (v+rotate_bits(v, 2)) & 0xffff
    r = rotate_bits(r, 4) ^ (r & (v ^ x))
    return r & 0xffff

def cps3_generate_xor_mask(addr, key1, key2):
    '''cps3 rotation xor masker (u32)'''
    addr ^= key1
    v = (addr & 0xffff) ^ 0xffff
    v = rotate_xor(v, key2 & 0xffff)
    v ^= (addr >> 16) ^ 0xffff
    v = rotate_xor(v, key2 >> 16)
    v ^= (addr & 0xffff) ^ (key2 & 0xffff)
    return (v | (v << 16)) & 0xffffffff

def cps3_mask_rom(u32_buf : array, game : GameInfo , prg_offset=GameInfo.PRG_OFFSET10):
    '''decrypts / encrypts ROM buffer (u32) inplace. needs `tqdm` for progress

    Args:
        u32_buf (array): buffer for the ROM in 32bits
        game (GameInfo): the game of the rom
        prg_offset (hexadecimal, optional): PRG rom mask offset - dependent on the ROM (10 or 20). Defaults to GameInfo.PRG_OFFSET10.        
    '''
    total=0x800000 if (len(u32_buf) << 2) > 0x80000 else 0x80000 # determining ROM type,  0x80000 (512KB)   -> BIOS
                                                                 # anything larger will be 0x80000 (8MB)    -> PRG 
    chunk,desc=total>>8,'Dumping %s data' % ('PRG ROM' if total == 0x800000 else 'BIOS') # reports progress 2^8 times
    for i in range(0,total,4):
        offset=prg_offset
        if len(u32_buf) == 0x20000: # allegedly from FB's source,one should NOT decode FLASH commands
                                    # of BIOS which are located in range 0x1ff00,0x1ff6b
            offset=0 # usually no offset is there for BIOS
            if i in range(0x1ff00,0x1ff6b):continue
        u32_buf[i >> 2] = u32_buf[i >> 2] ^ cps3_generate_xor_mask(i + offset, game.KEY1, game.KEY2)        
        if i % chunk == 0:
            sys.stderr.write('%s : %.2f%%\r' % (desc,i*100/total))
    sys.stderr.write('Dumping is complete                     \n')

if __name__ == '__main__':
    parser = create_default_parser('CPS3 ROM Decryption / Encryption tool')    
    parser.add_argument('input',metavar='IN',help='Encrypted / Decrypted game ROM path')
    parser.add_argument('output',metavar='OUT',help='Decrypted / Encrypted game ROM path')
    parser.add_argument('type',metavar='TYPE',help='ROM Type (either 10 or 20,leave as is for file 10 & BIOS)',default=10,type=int)

    args = parser.parse_args()
    args = args.__dict__    

    data: array = to_unit32(open(args['input'], 'rb').read())
    game = locate_game_by_name(args['game'])

    sys.stderr.write('Dumping game rom for : %s\n' % game.GAMENAME)    
    if args['type']==10:
        sys.stderr.write('ROM Type : ROM 10 / BIOS (0x%x / 0x00)\n' % game.PRG_OFFSET10)
        cps3_mask_rom(data, game,prg_offset=game.PRG_OFFSET10)    
    else:
        sys.stderr.write('ROM Type : ROM 20 (0x%x)\n' % game.PRG_OFFSET20)
        cps3_mask_rom(data, game,prg_offset=game.PRG_OFFSET20)    

    data.byteswap()  # Saving as little-endian
    data.tofile(open(args['output'], 'wb'))
