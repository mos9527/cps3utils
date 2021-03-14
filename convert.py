import os
from cps3utils import create_default_parser,locate_game_by_name
from cps3utils.convert import split_rom,combine_rom,__desc__

if __name__ == '__main__':
    parser = create_default_parser(__desc__)    
    parser.add_argument('op',metavar='OPERATION',help='Either to Combine or Split a rom\n  combine : Split to Combined\n    split : Combined to Split')
    parser.add_argument('input',metavar='IN',help='Where to locate the ROMs')
    parser.add_argument('output',metavar='OUT',help='Where to save')
    args = parser.parse_args()
    args = args.__dict__

    game = locate_game_by_name(args['game'])    
    print('Converting game rom for : %s...' % game.GAMENAME)        
    if args['op'].lower() == 'split':
        # load selected rom in cart
        for romcart in game.ROMCARTS[1:]:# skips BIOS
            print('Loading : %s' % romcart.rom_id)
            combined = open(os.path.join(args['input'],romcart.rom_id)).read()
            for simm,simm_buffer in split_rom(romcart,combined):
                print('Saving : %s' % simm)
                open(os.path.join(args['output'],simm),'wb').write(simm_buffer)
    elif args['op'].lower() == 'combine':
        for romcart in game.ROMCARTS[1:]:
            print('Loading :',*romcart.rom_simms)
            simms = [open(os.path.join(args['input'],simm),'rb').read() for simm in romcart.rom_simms]          
            combined,combine_buffer = combine_rom(romcart,*simms)
            print('Saving : %s' % combined)
            open(os.path.join(args['output'],combined),'wb').write(combine_buffer)