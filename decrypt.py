from ast import parse
from random import choices
from cps3utils import parser_add_argument, create_parser, enter,locate_game_by_name, parser_parse_args
from cps3utils.load import LoadRom,__desc__

def __main__():
    create_parser(__desc__.split('\n')[0])    
    parser_add_argument('input',metavar='IN',help='Encrypted / Decrypted game ROM path', widget='FileChooser')
    parser_add_argument('output',metavar='OUT',help='Decrypted / Encrypted game ROM path', widget='FileSaver')
    parser_add_argument('type',metavar='TYPE',help='ROM Type',choices=['10','20','BIOS'])        
    args = parser_parse_args()
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
if __name__ == '__main__':
    enter(__main__)