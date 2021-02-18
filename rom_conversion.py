import os,gamedata,logging,argparse,sys

combined_folder,split_folder = '',''
# configuration

def cleandir(dirname: str):
    if os.path.isdir(dirname):
        return True
    os.mkdir(dirname)
    return True

def combined_to_split(game : gamedata.__archive):
    '''Converts *combined rom* in `combined_folder` to *split rom* and saves it in `split_folder`

    Args:
        game (gamedata.__archive): Game to be converted
    '''
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
            logging.debug('Writing %s' % split_file)
            with open(os.path.join(split_folder,split_file),'wb') as f:
                f.write(buffers[i])
        return True

    for combined in game.COMBINED[:game.COMBINED_DATA_INDEX]:
        # Splitting from DATA (10) rom
        '''
        IN -> A  B  C  D  E  F  G  H
        OUT-> A E | B F | C G | D H     
        split evenly into 4 chunks   
        '''
        index=0        
        logging.info('Splitting rom (data) %s' % combined)
        content = open(os.path.join(combined_folder,combined),'rb').read()
        buffers = [bytearray(),bytearray(),bytearray(),bytearray()]
        for b in content:
            buffers[index % 4].append(b)
            index+=1
        serial_output(combined,buffers)

    for combined in game.COMBINED[game.COMBINED_DATA_INDEX:]:
        index=0        
        logging.info('Splitting rom (user) %s' % combined)        
        content = open(os.path.join(combined_folder,combined),'rb').read()
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

def split_to_combined(game : gamedata.__archive):        
    '''Converts *split rom* from `split_folder` to *combined rom* and saves it in `combined_folder`

    Args:
        game (gamedata.__archive): Game to be converted
    '''    
    simm_index = 0
    for combined in game.COMBINED[:game.COMBINED_DATA_INDEX]:
        '''    
        IN -> A E | B F | C G | D H     
        OUT-> A B C D E F G H
        merge from 4 chunks to 1
        '''        
        logging.debug('Combining rom (data) %s' % combined)
        buffer = bytearray()
        contents = [open(os.path.join(split_folder,split_),'rb').read() for split_ in game.SIMM[simm_index:simm_index+4]]
        for index in range(0,len(contents[0]) * 4):
            buffer.append(contents[index % 4][index // 4])
        with open(os.path.join(combined_folder,combined),'wb') as f:f.write(buffer)
        simm_index += 4
    for combined in game.COMBINED[game.COMBINED_DATA_INDEX:]:      
        logging.debug('Combining rom (user) %s' % combined)
        buffer = bytearray()
        contents = [open(os.path.join(split_folder,split_),'rb').read() for split_ in game.SIMM[simm_index:simm_index+4]]
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
    logging.getLogger('root').setLevel(0)

    parser = argparse.ArgumentParser(description='CPS3 ROM Converstion tool')
    parser.add_argument('op',metavar='OPERATION',help='Operation : combine (split->combined)  split (combined->split)')
    parser.add_argument('game',metavar='GAME',help='Game name (e.g. Jojo\'s (JPN) is jojoban)')
    parser.add_argument('input',metavar='IN',help='Where to locate the extracted sources')
    parser.add_argument('output',metavar='OUT',help='Where to save')
    args = parser.parse_args()
    args = args.__dict__

    method = None
    if args['op'] == 'combine':
        combined_folder = args['output']
        split_folder = args['input']
        method = split_to_combined
    elif args['op'] == 'split':
        combined_folder = args['input']
        split_folder = args['output']        
        method = combined_to_split

    # cleaning output folder
    logging.info('Cleaning output folder')
    cleandir(args['output'])

    # locate gamedata
    game = args['game']
    try:
        game = getattr(gamedata,game)
    except Exception as e:
        logging.critical('Game %s not supported' % game)
        logging.critical(e)
        sys.exit(2)

    logging.info('====================================')
    logging.info('= GAME     : %s' % game.GAMENAME)
    logging.info('= ZIPNAME  : %s' % game.FILENAME)
    logging.info('====================================')
    # perform action
    try:
        method(game) and logging.info('Conversion succeeded')
    except Exception as e:
        logging.critical('Failed to convert %s' % game)
        logging.critical(e)
        sys.exit(2)