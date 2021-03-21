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
    
GAMES = []
def locate_game_by_name(sname: str) -> GameInfo:
    '''Locates a game by its shortname,e.g. jojoban'''
    for game in GAMES:
        if game.__name__.split('.')[-1] == sname:
            return game
    raise Exception("Game not supported : %s" % sname)

'''BEGIN GAME INFO'''
class jojoban(GameInfo):
    FILENAME = 'jojoban.zip'
    GAMENAME = '''ジョジョの 奇妙な冒険: 未来への遺産 JoJo's Bizarre Adventure (Japan 990927, NO CD)'''
    ROMCARTS = (
        ROMCart(ROMType.BIOS, 'jojoba_japan_nocd.29f400.u2', ()),
        ROMCart(ROMType.PRG_10, '10', ('jojoba-simm1.0','jojoba-simm1.1', 'jojoba-simm1.2', 'jojoba-simm1.3',)),
        ROMCart(ROMType.PRG_20, '20', ('jojoba-simm2.0','jojoba-simm2.1', 'jojoba-simm2.2', 'jojoba-simm2.3',)),
        ROMCart(ROMType.GFX, '30', ('jojoba-simm3.0', 'jojoba-simm3.1','jojoba-simm3.2', 'jojoba-simm3.3',)),
        ROMCart(ROMType.GFX, '31', ('jojoba-simm3.4', 'jojoba-simm3.5','jojoba-simm3.6', 'jojoba-simm3.7',)),
        ROMCart(ROMType.GFX, '40', ('jojoba-simm4.0', 'jojoba-simm4.1','jojoba-simm4.2', 'jojoba-simm4.3',)),
        ROMCart(ROMType.GFX, '41', ('jojoba-simm4.4', 'jojoba-simm4.5','jojoba-simm4.6', 'jojoba-simm4.7',)),
        ROMCart(ROMType.GFX, '50', ('jojoba-simm5.0', 'jojoba-simm5.1','jojoba-simm5.2', 'jojoba-simm5.3',)),
        ROMCart(ROMType.GFX, '51', ('jojoba-simm5.4','jojoba-simm5.5', 'jojoba-simm5.6', 'jojoba-simm5.7',))
    )
    KEY1 = 0x23323ee3
    KEY2 = 0x03021972    
GAMES.append(jojoban)
