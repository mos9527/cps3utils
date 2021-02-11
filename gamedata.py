class __archive():
    FILENAME = ''
    GAMENAME = ''
    SIMM = list()
    COMBINED = list()
    COMBINED_DATA_INDEX = 0


class jojoban(__archive):
    FILENAME = 'jojoban.zip'
    GAMENAME = '''JoJo no Kimyou na Bouken'''
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
        'jojoba_japan_nocd.29f400.u2'
    ]

    COMBINED = [
        "10", "20"  # data (PRG)
      , "30", "31", "40", "41", "50", "51" # user (CHR,etc)
    ]
    COMBINED_DATA_INDEX = 2