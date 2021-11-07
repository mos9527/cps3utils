from os.path import join

from cps3utils.crypt import Cps3CryptoIO
from cps3utils.games import ROMCart, jojoban

from config import rom_folder

from base.int_address_editor import entry as int_mod_entry

__desc__ = '''%s - 角色移速编辑''' % jojoban.GAMENAME


def __main__():
    print(__desc__)
    rom_10 = Cps3CryptoIO(open(join(rom_folder, '10'), 'r+b'),ROMCart.locate_ROMCart('10', jojoban.ROMCARTS), jojoban)
    int_mod_entry(
        rom_10, {
            "承太郎": (0x61DB0C4, 0x61DB0D4, 0x61DB0C4, 0x61DB0D4),
            "花京院（普通）": (0x61DB104, 0x61DB104, 0x61DB104, 0x61DB104),
            "阿布德尔": (0x61CC374, 0x61CC37C, 0x61CE4FC, 0x61CE50C),
            "波波": (0x61CC634, 0x61CC634, 0x61CE9E8, 0x61CE9E8),
            "老乔": (0x6058FC8, 0x60590CC, 0x60A6884, 0x60A688C),
            "伊奇": (0x61DB144, 0x61DB154, 0x61DB144, 0x61DB154),
            "阿雷西": (0x605FD84, 0x60600E0, 0x605FD84, 0x60600E0),
            "查卡": (0x61CCb0C, 0x61CCb1C, 0x61CEDF4, 0x61CEE04),
            "迪波": (0x61CCDD4, 0x61CCDDC, 0x61CF3B4, 0x61CF3B4),
            "密朵拉": (0x61CCF58, 0x61CCF60, 0x61CF7FC, 0x61CF80C),
            "DIO": (0x61DB1C4, 0x61DB1C4, 0x61DB1C4, 0x61DB1D4),
            "影 DIO": (0x61CD374, 0x61CD37C, None, None),
            "夸高二乔": (0x6072BB0, 0x6072BB4, None, None),
            "荷尔·荷斯": (0x61DB304, 0x61DB304, None, None),
            "瓦尼拉·艾斯": (0x61CD9E0, 0x61CD9E8, 0x61CFF6C, 0x61CFF74),
            "墨镜花": (0x61DB244, 0x61DB244, 0x61DB244, 0x61DB244),
            "黑波": (0x61CDDB0, 0x61CDDB0, None, None),
            "宠物店": (0x61CDEEC, 0x61CDEF4, None, None),
            "腿姐": (0x61DB284, 0x61DB284, None, None),
            "荷尔·荷斯 & 波因哥": (0x61DB284, 0x61DB284, None, None),
            "拉巴索": (0x61DB284, 0x61DB294, None, None),
            "修脚师": (0x61DB0C4, 0x61DB0D4, None, None),
         }, 
        ('前冲 (s.Off)', '后退 (s.Off)', '前冲 (s.On)', '后退 (s.On)')
    )

if __name__ == '__main__':
    __main__()
