from dump import *
from __init__ import jojoban
file10 = 'jojoban/10'
cps3 = CPS3IO(open(file10,'rb').read(),ROMType.PRG_10,jojoban)
# begin
cps3.seek(0x1DB0C4)
print(cps3.read(4))
cps3.seek(-4,1)
cps3.write(b'\x12\x13\x14\x15')
# end
cps3.seek(0)
open(file10,'wb').write(cps3.read_unmasked())