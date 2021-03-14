'''CLI Utilites'''
import argparse
gooey_installed = False
try:
    from gooey import Gooey,GooeyParser
    gooey_installed = True
except:pass
parser = None
def create_parser(description='<default tool name>'):
    '''Creates an `rgparser` with `game` as its first positional argument'''    
    from .games import GAMES
    global parser
    if gooey_installed:
        parser = GooeyParser(description=description)
    else:
        parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('game', metavar='GAME',help='CPS3 Game shortname',choices=[game.__name__.split('.')[-1] for game in GAMES])
    return parser
gooey_whitelist = {'widget'}
def parser_add_argument(*a,**kw):
    if not gooey_installed:kw = {k:v for k,v in kw.items() if k not in gooey_whitelist}
    return parser.add_argument(*a,**kw)
def parser_parse_args():
    return parser.parse_args()
def enter(main_func):
    if gooey_installed:        
        Gooey(
            program_name='cps3utils',
            progress_regex=r"(?P<curr>(?:\d*)) */ *(?P<all>(?:\d*))",
            progress_expr="curr * 100 / all"
        )(main_func)()
    else:
        main_func()
'''Subroutines'''
def sub_convert():
    import os
    from cps3utils import locate_game_by_name
    from cps3utils.convert import split_rom,combine_rom,__desc__
    create_parser(__desc__.split('\n')[0])    
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
        
def sub_decrypt():
    from cps3utils import locate_game_by_name
    from cps3utils.load import LoadRom,__desc__    
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
subroutines = {'convert':sub_convert,'decrypt':sub_decrypt}
if __name__ == '__main__':
    prompt = '%s' % '/'.join(list(subroutines.keys()))
    import sys
    if not len(sys.argv) > 1:
        sys.stderr.write('HELP : %s [%s] [arguments] [keyword arguments]' % (sys.argv[0],prompt))
        sys.exit(0)
    operation = sys.argv.pop(1).lower()
    if not operation in subroutines:
        sys.stderr.write('ERROR : Supported subrotines are [%s]\n' % prompt)
        sys.exit(2)
    else:
        subroutine = subroutines[operation]
        enter(subroutine)
