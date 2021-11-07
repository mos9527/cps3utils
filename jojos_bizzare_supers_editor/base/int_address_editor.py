from cps3utils.crypt import Cps3CryptoIO
from inquirer import List, prompt
from base import input_int

def read(rom_10 : Cps3CryptoIO,addr,length=4):
    if addr is None:return 0
    rom_10.seek(addr - 0x6000000)
    return int.from_bytes(rom_10.read(length),'big')

def write(rom_10 : Cps3CryptoIO,addr,value,length=4):
    if addr is None:return 0
    rom_10.seek(addr - 0x6000000)
    return rom_10.write(int.to_bytes(value,length,'big'))

def entry(rom : Cps3CryptoIO,char_addr_dict : dict,addr_desc_list : list,length=4):
    # Selecting character
    char = prompt([List('char','角色选择',choices=char_addr_dict)])['char']
    addrs= char_addr_dict[char]

    l_max = max(len(sorted(addr_desc_list,key=lambda v:len(v))[-1]),len(str(2**(length*2))))
    
    print('当前值'.center(l_max * len(addr_desc_list),'─'))
    print(*[str(desc).center(l_max) for desc in addr_desc_list])
    print(*[str(read(rom,addr,length)).center(l_max) for addr in addrs])
    print('─' * (l_max * len(addr_desc_list) + 3),'\n')

    index = prompt([List('index','修改选择',choices=addr_desc_list)])['index']
    index = addr_desc_list.index(index)
    nVal = input_int('修改 %s(当前为：%d)为:' % (addr_desc_list[index],read(rom,addrs[index],length)))
    
    write(rom,addrs[index],nVal,length)    