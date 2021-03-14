__desc__ =  '''CPS3 ROM Conversion utilty

credit:
    mamedev/mame
    GaryButternubs/CPS3-ROM-Conversion
'''
from .games import ROMType
from . import ROMCart
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
