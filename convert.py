import os,sys
from __init__ import *
import __init__

def writeline(s : str):
    sys.stderr.write(s)    

def makedir(dirname: str):
    if os.path.isdir(dirname):
        return True
    os.mkdir(dirname)
    return True

def combined_to_split(game : GameInfo,split_folder,combined_folder):
    '''Converts *combined rom* in `combined_folder` to *split rom* and saves it in `split_folder`'''
    def serial_output(combined,buffers):
        '''
        IN -> A B | C D | E F | G H
        OUT->
            File 1: AB File 2: CD
            File 3: EF File 4: GH
        '''
        idx = game.COMBINED.index(combined)
        for i in range(0,4):
            split_file = game.SIMM[i+4*idx]
            writeline('...Writing %s\n' % split_file)
            with open(os.path.join(split_folder,split_file),'wb') as f:
                f.write(buffers[i])
        return True

    for combined in game.COMBINED[:game.PRG_INDEX]:
        # Splitting from PRG rom
        '''
        IN -> A  B  C  D  E  F  G  H
        OUT-> A E | B F | C G | D H     
        split evenly into 4 chunks   
        '''
        index=0        
        writeline('Splitting rom (PRG / ESS) %s\n' % combined)
        content = open(os.path.join(combined_folder,combined),'rb').read().zfill(0x800000)
        buffers = [bytearray(),bytearray(),bytearray(),bytearray()]
        for b in content:
            buffers[index % 4].append(b)
            index+=1
        serial_output(combined,buffers)

    for combined in game.COMBINED[game.PRG_INDEX:]:
        index=0        
        writeline('Splitting rom (GFX) %s\n' % combined)        
        content = open(os.path.join(combined_folder,combined),'rb').read().zfill(0x800000)
        buffers = [bytearray(),bytearray(),bytearray(),bytearray()]        
        for b in content[:len(content)//2]:
            # processing first half of the file
            '''
            IN -> A  B  C  D  E  F  G  H
            OUT-> A  C  E  G | B  D  F H      
            split evenly into 2 chunks  
            '''
            buffers[index % 2].append(b)
            index+=1
        old_index=index
        index = 0
        for b in content[old_index:len(content)]:
            # the same, but with the last half            
            buffers[index % 2 + 2].append(b)
            index+=1        
        serial_output(combined,buffers)            
    return True

def split_to_combined(game : GameInfo,split_folder,combined_folder):       
    '''Converts *split rom* from `split_folder` to *combined rom* and saves it in `combined_folder`'''    
    simm_index = 0
    for combined in game.COMBINED[:game.PRG_INDEX]:
        '''    
        IN -> A E | B F | C G | D H     
        OUT-> A B C D E F G H
        merge from 4 chunks to 1
        '''        
        writeline('Combining rom (PRG / ESS) %s\n' % combined)
        buffer = bytearray()
        contents = [open(os.path.join(split_folder,split_),'rb').read().zfill(0x200000) for split_ in game.SIMM[simm_index:simm_index+4]]
        for index in range(0,len(contents[0]) * 4):
            buffer.append(contents[index % 4][index // 4])
        with open(os.path.join(combined_folder,combined),'wb') as f:f.write(buffer)
        simm_index += 4
    for combined in game.COMBINED[game.PRG_INDEX:]:      
        writeline('Combining rom (GFX) %s\n' % combined)
        buffer = bytearray()
        contents = [open(os.path.join(split_folder,split_),'rb').read().zfill(0x200000) for split_ in game.SIMM[simm_index:simm_index+4]]
        for index in range(0,len(contents[0]) * 2):
            # first 2 halves
            '''            
            IN-> A  C  E  G | B  D  F H      
            OUT -> A B C D E F G H
            merge from 2 chunks to 1
            '''
            buffer.append(contents[index % 2][index // 2])
        old_index=index+1
        for index in range(old_index,len(contents[0]) * 4):
            # last 2 halves
            buffer.append(contents[(index-old_index) % 2 + 2][(index-old_index) // 2])            
        with open(os.path.join(combined_folder,combined),'wb') as f:f.write(buffer)
        simm_index += 4      
    return True

if __name__ == '__main__':
    parser = create_default_parser('CPS3 ROM conversion utilty')
    parser.add_argument('op',metavar='OPERATION',help='Either to Combine or Split a rom\n  combine : Split to Combined\n    split : Combined to Split')
    parser.add_argument('input',metavar='IN',help='Where to locate the extracted sources')
    parser.add_argument('output',metavar='OUT',help='Where to save')
    args = parser.parse_args()
    args = args.__dict__

    method = None
    if args['op'].lower() == 'combine':
        combined_folder = args['output']
        split_folder = args['input']
        method = split_to_combined
    elif args['op'].lower() == 'split':
        combined_folder = args['input']
        split_folder = args['output']        
        method = combined_to_split
        
    # creating output folder
    makedir(args['output'])
    # locate GameInfo
    game = locate_game_by_name(args['game'])  
    try:
        # perform conversion
        writeline('Converting game rom for : %s\n' % game.GAMENAME)  
        method(game,split_folder,combined_folder) and writeline('Game converted\n')
    except Exception as e:
        writeline('Failed to convert %s\n' % game)
        writeline('%s\n' % e)
        sys.exit(2)