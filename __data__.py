class __archive():
    FILENAME = '<undefined>'
    GAMENAME = '<undefined>'
    '''SIMM rom names'''
    SIMM = []
    '''Combined rom names'''
    COMBINED = []
    '''Index of PRG rom in COMBINED,usually 2'''
    COMBINED_PRG_INDEX = 0
    '''CPS3 PRG ROM Key'''
    KEY1=0xffffffff
    KEY2=0xffffffff

class jojoban(__archive):
    FILENAME = 'jojoban.zip'
    GAMENAME = '''ジョジョの 奇妙な冒険: 未来への遺産 JoJo's Bizarre Adventure (Japan 990927, NO CD)'''
    SIMM = [
        'jojoba-simm1.0',
        'jojoba-simm1.1',
        'jojoba-simm1.2',
        'jojoba-simm1.3',
        'jojoba-simm2.0',
        'jojoba-simm2.1',
        'jojoba-simm2.2',
        'jojoba-simm2.3',
        'jojoba-simm3.0',
        'jojoba-simm3.1',
        'jojoba-simm3.2',
        'jojoba-simm3.3',
        'jojoba-simm3.4',
        'jojoba-simm3.5',
        'jojoba-simm3.6',
        'jojoba-simm3.7',
        'jojoba-simm4.0',
        'jojoba-simm4.1',
        'jojoba-simm4.2',
        'jojoba-simm4.3',
        'jojoba-simm4.4',
        'jojoba-simm4.5',
        'jojoba-simm4.6',
        'jojoba-simm4.7',
        'jojoba-simm5.0',
        'jojoba-simm5.1',
        'jojoba-simm5.2',
        'jojoba-simm5.3',
        'jojoba-simm5.4',
        'jojoba-simm5.5',
        'jojoba-simm5.6',
        'jojoba-simm5.7',
    ]
    COMBINED = ["10", "20", "30", "31", "40", "41", "50", "51"]
    COMBINED_PRG_INDEX = 2    
    KEY1=0x23323ee3
    KEY2=0x03021972