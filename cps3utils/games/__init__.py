class ROMType:
    '''Type of the ROM. The values are actually thier offsets in CPS3's address space'''
    BIOS   = 0x0
    PRG_10 = 0x6000000
    PRG_20 = 0x6800000
    GFX    = 0xfffffff # ...except for this one

class ROMCart:    
    '''Defines a CPS3 cartridge , named by thier `combined rom` ID'''
    s8MB = 0x800000
    s2MB = 0x200000
    s512KB = 0x80000

    rom_type : ROMType = 0x0 
    rom_id = ''
    rom_simms = ()
    def __init__(self,rom_type:ROMType,rom_id:str,simm:tuple) -> None:        
        self.rom_type = rom_type
        self.rom_id = rom_id
        self.rom_simms = simm
    @staticmethod
    def locate_ROMCart(fname : str,romcarts : tuple):
        for romcart in romcarts:            
            if romcart.rom_id == fname:return romcart            
            if fname in romcart.rom_simms:return romcart
    
class GameInfo:
    '''Stub class for game archives'''
    FILENAME = '<undefined>'
    GAMENAME = '<undefined>'
    '''SIMM rom names'''
    ROMCARTS = ()
    '''A list of `RomCart`'''
    PRG_INDEX = 0
    '''CPS3 PRG ROM Key'''
    KEY1 = 0xffffffff
    KEY2 = 0xffffffff
    
'''BEGIN GAME INFO'''
from . import jojoban
GAMES = [jojoban.jojoban]

def locate_game_by_name(sname: str) -> GameInfo:
    '''Locates a game by its shortname,e.g. jojoban'''
    for game in GAMES:
        if game.__name__.split('.')[-1] == sname:
            return game
    raise Exception("Game not supported : %s" % sname)