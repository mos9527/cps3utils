import os,argparse
if __name__ == '__main__':
    a = argparse.ArgumentParser(description='Jojo\'s BGM Removal tool')
    a.epilog = 'This script mutes music in jojoban by wiping out the first 1MB of its rom 30'
    a.add_argument('file30',help='Path to file 30')
    args = a.parse_args()
    file_30 = args.__dict__['file30']
    fsize   = os.stat(file_30).st_size
    with open(file_30,'r+b') as f:
        f.write(b'\x00' * 0x100000)