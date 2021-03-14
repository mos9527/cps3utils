from . import GameInfo,ROMCart,ROMType
class jojoban(GameInfo):
    FILENAME = 'jojoban.zip'
    GAMENAME = '''ジョジョの 奇妙な冒険: 未来への遺産 JoJo's Bizarre Adventure (Japan 990927, NO CD)'''
    ROMCARTS = (
        ROMCart(ROMType.BIOS  ,'jojoba_japan_nocd.29f400.u2',()),
        ROMCart(ROMType.PRG_10,'10',('jojoba-simm1.0','jojoba-simm1.1','jojoba-simm1.2','jojoba-simm1.3',)),
        ROMCart(ROMType.PRG_20,'20',('jojoba-simm2.0','jojoba-simm2.1','jojoba-simm2.2','jojoba-simm2.3',)),
        ROMCart(ROMType.GFX   ,'30',('jojoba-simm3.0','jojoba-simm3.1','jojoba-simm3.2','jojoba-simm3.3',)),
        ROMCart(ROMType.GFX   ,'31',('jojoba-simm3.4','jojoba-simm3.5','jojoba-simm3.6','jojoba-simm3.7',)),
        ROMCart(ROMType.GFX   ,'40',('jojoba-simm4.0','jojoba-simm4.1','jojoba-simm4.2','jojoba-simm4.3',)),
        ROMCart(ROMType.GFX   ,'41',('jojoba-simm4.4','jojoba-simm4.5','jojoba-simm4.6','jojoba-simm4.7',)),
        ROMCart(ROMType.GFX   ,'50',('jojoba-simm5.0','jojoba-simm5.1','jojoba-simm5.2','jojoba-simm5.3',)),
        ROMCart(ROMType.GFX   ,'51',('jojoba-simm5.4','jojoba-simm5.5','jojoba-simm5.6','jojoba-simm5.7',))
    )
    KEY1 = 0x23323ee3
    KEY2 = 0x03021972
    '''The following data is dedicated to jojoban'''
    # note: the following addreses are offseted by +0x6000000 in file 10
    StandGaugeCapacityAddresses = {
        # u16
        "Jotaro": 0x61DD950,
        "Kakyoin": 0x61DD952,
        "Avdol": 0x61DD954,
        "Polnareff": 0x61DD956,
        "Joseph": 0x61DD958,
        "Iggy": 0x61DD95A,
        "Alessi": 0x61DD95C,
        "Chaka": 0x61DD95E,
        "Devo": 0x61DD960,
        "Midler": 0x61DD964,
        "DIO": 0x61DD966,
        "Vanilla Ice": 0x61DD972,
        "New Kakyoin": 0x61DD974,
    }
    CharacterDashVelocityAddresses = {
        # u32
        # Character | Forward Dash (Stand Off) | Backward Dash (Stand Off) | Forward Dash (Stand On) | Backward Dash (Stand On)
        "Jotaro": (0x61DB0C4, 0x61DB0D4, 0x61DB0C4, 0x61DB0D4),
        "Kakyoin": (0x61DB104, 0x61DB104, 0x61DB104, 0x61DB104),
        "Avdol": (0x61CC374, 0x61CC37C, 0x61CE4FC, 0x61CE50C),
        "Polnareff": (0x61CC634, 0x61CC634, 0x61CE9E8, 0x61CE9E8),
        "Old Joseph": (0x6058FC8, 0x60590CC, 0x60A6884, 0x60A688C),
        "Iggy": (0x61DB144, 0x61DB154, 0x61DB144, 0x61DB154),
        "Alessi": (0x605FD84, 0x60600E0, 0x605FD84, 0x60600E0),
        "Chaka": (0x61CCb0C, 0x61CCb1C, 0x61CEDF4, 0x61CEE04),
        "Devo": (0x61CCDD4, 0x61CCDDC, 0x61CF3B4, 0x61CF3B4),
        "Midler": (0x61CCF58, 0x61CCF60, 0x61CF7FC, 0x61CF80C),
        "DIO": (0x61DB1C4, 0x61DB1C4, 0x61DB1C4, 0x61DB1D4),
        "Shadow Dio": (0x61CD374, 0x61CD37C, None, None),
        "Young Joseph": (0x6072BB0, 0x6072BB4, None, None),
        "Hol Horse": (0x61DB304, 0x61DB304, None, None),
        "Vanilla Ice": (0x61CD9E0, 0x61CD9E8, 0x61CFF6C, 0x61CFF74),
        "New Kakyoin": (0x61DB244, 0x61DB244, 0x61DB244, 0x61DB244),
        "Black Polnareff": (0x61CDDB0, 0x61CDDB0, None, None),
        "Petshop": (0x61CDEEC, 0x61CDEF4, None, None),
        "Mariah": (0x61DB284, 0x61DB284, None, None),
        "Hol & Boingo": (0x61DB284, 0x61DB284, None, None),
        "Rubber Soul": (0x61DB284, 0x61DB294, None, None),
        "Khan": (0x61DB0C4, 0x61DB0D4, None, None),
    }
    ChracterDefenseAddresses = {
        "Jotaro": (0x61DAE28, 0x61DAE2C),
        "Kakyoin": (0x61DAE30, 0x61DAE34),
        "Avdol": (0x61DAE38, 0x61DAE3C),
        "Polnareff": (0x61DAE40, 0x61DAE44),
        "Old Joseph": (0x61DAE48, 0x61DAE4C),
        "Iggy": (0x61DAE50, 0x61DAE54),
        "Alessi": (0x61DAE58, 0x61DAE5C),
        "Chaka": (0x61DAE60, 0x61DAE64),
        "Devo": (0x61DAE68, 0x61DAE6C),
        "Midler": (0x61DAE78, 0x61DAE7C),
        "DIO": (0x61DAE80, 0x61DAE84),
        "Shadow Dio": (0x61DAE98, None),
        "Young Joseph": (0x61DAEA0, None),
        "Hol Horse": (0x61DAEA8, None),
        "Vanilla Ice": (0x61DAEB0, 0x61DAEB4),
        "New Kakyoin": (0x61DAEB8, 0x61DAEBC),
        "Black Polnareff": (0x61DAEC0, None),
        "Petshop": (0x61DAEC8, None),
        "Mariah": (0x61DAED8, None),
        "Hol Horse & Boingo": (0x61DAEE0, None),
        "Rubber Soul": (0x61DAEE8, None),
        "Khan": (0x61DAEF0, None),
    }

