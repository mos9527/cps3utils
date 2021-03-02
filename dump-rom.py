import sys
from array import array
import gamedata

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

import tqdm
def cps3_mask_rom(u32_buf : array, keys : gamedata.__archive):
    '''decrypts / encrypts ROM buffer (u32) inplace. needs `tqdm` for progress'''
    total=0x1000000 if (len(u32_buf) << 2) > 0x80000 else 0x20000    
    t = tqdm.tqdm(total=total, unit='B',unit_scale=True, desc='Dumping %s data' % ('game' if total == 0x1000000 else 'BIOS'))
    for i in range(0,total,4):
        offset=0x6000000
        if len(u32_buf) == 0x20000:
            # it's the bios we're dealing with; for which the FLASH commands are NOT decrypted            
            if i in range(0x1ff00,0x1ff6b):continue
            offset=0
        # otherwise it's the PRG rom
        u32_buf[i >> 2] = u32_buf[i >> 2] ^ cps3_generate_xor_mask(i + offset, keys.KEY1, keys.KEY2)
        t.update(4)
    t.close()

if __name__ == '__main__': # an argparser would be nice
    data: array = to_unit32(open('bios.u2', 'rb').read(0x1000000))
    cps3_mask_rom(data, gamedata.jojoban)
    sys.stderr.write('Saving dump\n')
    data.byteswap()  # Saving as little-endian
    data.tofile(open('bios_d.u2', 'wb'))
