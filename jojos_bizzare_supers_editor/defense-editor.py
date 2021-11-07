from os.path import join

from cps3utils.crypt import Cps3CryptoIO
from cps3utils.games import ROMCart, jojoban

from config import rom_folder
from base.int_address_editor import entry as int_mod_entry

__desc__ = '''%s - 角色防御编辑
（防御值越低，角色受到的伤害越少）
''' % jojoban.GAMENAME

def __main__():
    print(__desc__)
    rom_10 = Cps3CryptoIO(open(join(rom_folder, '10'), 'r+b'),ROMCart.locate_ROMCart('10', jojoban.ROMCARTS), jojoban)
    int_mod_entry(
        rom_10, {
            "承太郎": (0x61DAE28, 0x61DAE2C),
            "花京院（普通）": (0x61DAE30, 0x61DAE34),
            "阿布德尔": (0x61DAE38, 0x61DAE3C),
            "波波": (0x61DAE40, 0x61DAE44),
            "老乔": (0x61DAE48, 0x61DAE4C),
            "伊奇": (0x61DAE50, 0x61DAE54),
            "阿雷西": (0x61DAE58, 0x61DAE5C),
            "查卡": (0x61DAE60, 0x61DAE64),
            "迪波": (0x61DAE68, 0x61DAE6C),
            "密朵拉": (0x61DAE78, 0x61DAE7C),
            "DIO": (0x61DAE80, 0x61DAE84),
            "影 DIO": (0x61DAE98, None),
            "夸高二乔": (0x61DAEA0, None),
            "荷尔·荷斯": (0x61DAEA8, None),
            "瓦尼拉·艾斯": (0x61DAEB0, 0x61DAEB4),
            "墨镜花": (0x61DAEB8, 0x61DAEBC),
            "黑波": (0x61DAEC0, None),
            "宠物店": (0x61DAEC8, None),
            "腿姐": (0x61DAED8, None),
            "荷尔·荷斯 & 波因哥": (0x61DAEE0, None),
            "拉巴索": (0x61DAEE8, None),
            "修脚师": (0x61DAEF0, None),
        }, ('防御 (s.Off)', '防御 (s.On)')
    )


if __name__ == '__main__':
    __main__()
