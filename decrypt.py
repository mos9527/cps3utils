from cps3utils import create_default_parser,locate_game_by_name
from cps3utils.load import LoadRom,__desc__

if __name__ == '__main__':
    parser = create_default_parser(__desc__)    
    parser.add_argument('input',metavar='IN',help='Encrypted / Decrypted game ROM path')
    parser.add_argument('output',metavar='OUT',help='Decrypted / Encrypted game ROM path')
    parser.add_argument('type',metavar='TYPE',help='ROM Type (10,20,or BIOS)',default='10')    
    args = parser.parse_args()
    args = args.__dict__    

    game = locate_game_by_name(args['game'])    
    romcart = None
    print('Dumping game rom for : %s...' % game.GAMENAME)        
    if args['type']=='10':
        print('ROM Type : ROM 10')
        romcart = game.ROMCARTS[1]
    elif args['type']=='20':
        print('ROM Type : ROM 20')
        romcart = game.ROMCARTS[2]
    else:
        print('ROM Type : BIOS')
        romcart = game.ROMCARTS[0]
    cps3 = LoadRom(open(args['input'],'rb'),romcart,game)
    data = cps3.read(show_progress=True)
    data.tofile(open(args['output'], 'wb'))
