__desc__ =  '''CPS3 ROM Conversion utilty

Converts ROMs between combined (10,etc) and split (SIMMs) formats

credit:
    mamedev/mame
    GaryButternubs/CPS3-ROM-Conversion
'''
from cps3utils.games import ROMType
from cps3utils import ROMCart, create_parser, enter, parser_add_argument, parser_parse_args
import sys
      
def split_rom(cart : ROMCart,combined_rom : bytearray) -> tuple:
    '''Splits combined-rom into multiple split-rom

    Args:
        cart (ROMCart): The cart of the combined rom
        combined_rom (bytearray): The full content of the combined-rom
    
    Returns:
        tuple: ((<simm name : str>,<simm content : bytearray>),...)
    '''
    buffers = [bytearray(),bytearray(),bytearray(),bytearray()]        
    content = combined_rom.zfill(cart.s8MB)    
    if cart.rom_type is ROMType.GFX:        
        # rail fence cipher - period=2
        sys.stderr.write('Splitting rom (GFX) : %s\n' % cart.rom_id)                        
        for i in range(0,len(content)//2):
            buffers[i % 2].append(content[i])                            
        for i in range(len(content)//2,len(content)):
            buffers[i % 2 + 2].append(content[i])            
    elif cart.rom_type is ROMType.PRG_10 or cart.rom_type is ROMType.PRG_20:            
        # rail fence cipher - period=4
        sys.stderr.write('Splitting rom (PRG) : %s\n' % cart.rom_id)        
        for i in range(0,len(content)):
            buffers[i % 4].append(content[i])            
    else:
        raise Exception("Cannot split this ROMCart (Unsupported Type : 0x%x)" % cart.rom_type)    
    return zip(cart.rom_simms,buffers)

def combine_rom(cart : ROMCart,*simm_roms : bytearray) -> tuple:    
    '''Combines multiple split-rom into one combined-rom 

    Args:
        cart (ROMCart): The cart of the split rom
        *simm_roms : A list (usually a group of 4) of SIMM rom buffers

    Returns:
        tuple: (<combined name>,<combined buffer>)
    '''
    buffer = bytearray()
    contents = [simm.zfill(cart.s2MB) for simm in simm_roms]
    if cart.rom_type is ROMType.GFX:
        sys.stderr.write('Combining rom (GFX) : %s\n' % cart.rom_id)        
        for index in range(0,len(contents[0]) * 2):
            # rail fence cipher - period=2
            buffer.append(contents[index % 2][index // 2])        
        for index in range(len(contents[0]) * 2,len(contents[0]) * 4):
            # rail fence cipher - period=4
            buffer.append(contents[(index-len(contents[0]) * 2) % 2 + 2][(index-len(contents[0]) * 2) // 2])                 
    elif cart.rom_type is ROMType.PRG_10 or cart.rom_type is ROMType.PRG_20:                    
        # rail fence cipher - period=4
        sys.stderr.write('Combining rom (PRG) : %s\n' % cart.rom_id)        
        for index in range(0,len(contents[0]) * 4):
            buffer.append(contents[index % 4][index // 4])
    else:
        raise Exception("Cannot combine this ROMCart (Unsupported Type : 0x%x)" % cart.rom_type)
    return (cart.rom_id,buffer)

def __main__():    
    from cps3utils import locate_game_by_name
    import os
    create_parser(__desc__)    
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
    enter(__main__,__desc__)