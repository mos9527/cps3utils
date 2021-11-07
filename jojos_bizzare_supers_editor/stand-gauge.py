from os.path import join

from cps3utils.crypt import Cps3CryptoIO
from cps3utils.games import ROMCart, jojoban
from config import rom_folder
from base.int_address_editor import entry as int_mod_entry


__desc__ = '''%s - 替身槽耐久编辑''' % jojoban.GAMENAME

def __main__():
    print(__desc__)
    rom_10 = Cps3CryptoIO(open(join(rom_folder, '10'), 'r+b'),ROMCart.locate_ROMCart('10', jojoban.ROMCARTS), jojoban)
    int_mod_entry(
        rom_10,
        {
            "承太郎": (0x61DD950,),
            "花京院（普通）": (0x61DD952,),
            "阿布德尔": (0x61DD954,),
            "波波": (0x61DD956,),
            "老乔": (0x61DD958,),
            "伊奇": (0x61DD95A,),
            "阿雷西": (0x61DD95C,),
            "查卡": (0x61DD95E,),
            "迪波": (0x61DD960,),
            "密朵拉": (0x61DD964,),
            "DIO": (0x61DD966,),
            "瓦尼拉·艾斯": (0x61DD972,),
            "墨镜花": (0x61DD974,),
        }, ('替身槽耐久',), 2
    )

if __name__ == '__main__':
    __main__()
