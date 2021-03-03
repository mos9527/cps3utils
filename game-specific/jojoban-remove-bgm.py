import sys,os
if __name__ == '__main__':
    try:
        if len(sys.argv)==2:
            file_30 = sys.argv[1]
            fsize   = os.stat(file_30).st_size            
            assert fsize == 8 * 1<<20 # File 30 should always be 8 mebibytes            
            with open(file_30,'r+b') as f:
                f.write(b'\x00' * 0x100000)                                        
        else:
            raise ValueError('''usage:
    %s 30    

30 being your ROM's file 30 (ROM needs to be combined,otherwise,use `rom_conversion.py` to convert it first)
        ''' % sys.argv[0])
    except ValueError as e:    
        sys.stderr.write('%s'%e)