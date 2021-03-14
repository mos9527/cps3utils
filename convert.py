import os
from cps3utils import create_parser,locate_game_by_name,enter, parser_add_argument, parser_parse_args
from cps3utils.convert import split_rom,combine_rom,__desc__

def __main__():
    parser = create_parser(__desc__.split('\n')[0])    
    parser_add_argument('op',metavar='OPERATION',help='Either to Combine or Split a rom',choices=['split','combine'])
    parser_add_argument('input',metavar='IN',help='Where to locate the ROMs',widget='DirChooser')
    parser_add_argument('output',metavar='OUT',help='Where to save',widget='DirChooser')
    args = parser_parse_args()
    args = args.__dict__

    game = locate_game_by_name(args['game'])    
    print('Converting game rom for : %s...' % game.GAMENAME)        
    if args['op'].lower() == 'split':
        # load selected rom in cart
        for index,romcart in enumerate(game.ROMCARTS[1:],1):# skips BIOS
            print('Loading : %s (%d / %d)' % (romcart.rom_id,index,len(game.ROMCARTS) - 1))
            combined = open(os.path.join(args['input'],romcart.rom_id),'rb').read()
            for simm,simm_buffer in split_rom(romcart,combined):
                print('Saving : %s' % simm)
                open(os.path.join(args['output'],simm),'wb').write(simm_buffer)
    elif args['op'].lower() == 'combine':
        for index,romcart in enumerate(game.ROMCARTS[1:],1):# skips BIOS
            print('Loading :',*romcart.rom_simms,'(%d / %d)' % (index,len(game.ROMCARTS) - 1))
            simms = [open(os.path.join(args['input'],simm),'rb').read() for simm in romcart.rom_simms]          
            combined,combine_buffer = combine_rom(romcart,*simms)
            print('Saving : %s' % combined)
            open(os.path.join(args['output'],combined),'wb').write(combine_buffer)
        
if __name__ == '__main__':
    enter(__main__)