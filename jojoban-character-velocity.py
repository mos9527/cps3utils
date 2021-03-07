from dump import *
from __init__ import delayed_prompt, indexed_selector, jojoban
import argparse
def __main__(file10):
    desc = ['Forward Dash (Stand Off)','Backward Dash (Stand Off)','Forward Dash (Stand On)','Backward Dash (Stand On)']
    def read_int_at(addr):
        if addr is None:return 0
        rom.seek(addr - 0x6000000)
        return int.from_bytes(rom.read(4),'big')

    rom = Cps3IO(open(file10,'r+b'),ROMType.PRG_10,jojoban)
    
    char = indexed_selector(jojoban.CharacterDashVelocityAddresses,'Select your character')
    char = list(jojoban.CharacterDashVelocityAddresses.keys())[char]

    fdash,bdash,fdash_s,bdash_s = jojoban.CharacterDashVelocityAddresses[char]

    print('Character',*desc)
    print('%10s| %d %d %d %d' % (char,read_int_at(fdash),read_int_at(bdash),read_int_at(fdash_s),read_int_at(bdash_s)))

    sel = indexed_selector(desc,'What velocity to change')
    addr = jojoban.CharacterDashVelocityAddresses[char][sel] - 0x6000000

    vel = int(input('Changing %s (0x%x) to:' % (desc[sel],addr)))
    vel = vel.to_bytes(4,'big')
    
    rom.seek(addr) and rom.write(vel)
    delayed_prompt('Saved new character velocity.')

if __name__ == '__main__':
    a = argparse.ArgumentParser(description='Jojo\'s Charcter Stand Gauge value tweak tool')    
    a.add_argument('file10',help='Path to file 10')
    args = a.parse_args()
    while True:__main__(args.__dict__['file10'])