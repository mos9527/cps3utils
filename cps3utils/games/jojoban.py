from . import GameInfo, ROMCart, ROMType

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
