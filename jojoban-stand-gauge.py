from dump import *
from __init__ import delayed_prompt, indexed_selector, jojoban
import argparse
def __main__(file10):
    rom = Cps3IO(open(file10,'r+b'),ROMType.PRG_10,jojoban)
    char = indexed_selector(jojoban.StandGaugeCapacityAddresses,'Select your character')
    char = list(jojoban.StandGaugeCapacityAddresses.keys())[char]
    addr = jojoban.StandGaugeCapacityAddresses[char] - 0x6000000

    rom.seek(addr)    
    cap = int.from_bytes(rom.read(2),'big')

    print('Stand gauge capacity: %d' % cap)
    cap = input('New character stand gauge capacity:')
    cap = int(cap).to_bytes(2,'big')
    
    rom.seek(-2,1) and rom.write(cap)
    delayed_prompt('Saved new character stand gauge capacity.')
if __name__ == '__main__':
    a = argparse.ArgumentParser(description='Jojo\'s Charcter Stand Gauge value tweak tool')    
    a.add_argument('file10',help='Path to file 10')
    args = a.parse_args()
    while True:__main__(args.__dict__['file10'])