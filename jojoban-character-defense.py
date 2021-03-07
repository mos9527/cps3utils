from dump import *
from __init__ import delayed_prompt, indexed_selector, jojoban
import argparse
def __main__(file10):
    desc = ['Defense (Stand Off)','Defense (Stand On)']
    def read_int_at(addr):
        if addr is None:return 0
        rom.seek(addr - 0x6000000)
        return int.from_bytes(rom.read(4),'big')
    rom = cps3mem(open(file10,'rb').read(),ROMType.PRG_10,jojoban)
    char = indexed_selector(jojoban.ChracterDefenseAddresses,'Select your character')
    char = list(jojoban.ChracterDefenseAddresses.keys())[char]
    defense,defense_s = jojoban.ChracterDefenseAddresses[char]
    print('Character',*desc)
    print('%10s| %d %d' % (char,read_int_at(defense),read_int_at(defense_s)))
    sel = indexed_selector(desc,'What defense value to change (note that the lower the value, the better the defense)')
    addr = jojoban.ChracterDefenseAddresses[char][sel] - 0x6000000
    vel = int(input('Changing %s (0x%x) to:' % (desc[sel],addr)))
    vel = vel.to_bytes(4,'big')
    rom.seek(addr) and rom.write(vel)
    rom.seek(0) or open(file10,'wb').write(rom.read_unmasked())
    delayed_prompt('Saved new character defense value.')

if __name__ == '__main__':
    a = argparse.ArgumentParser(description='Jojo\'s Charcter Stand Gauge value tweak tool')    
    a.add_argument('file10',help='Path to file 10')
    args = a.parse_args()
    while True:__main__(args.__dict__['file10'])