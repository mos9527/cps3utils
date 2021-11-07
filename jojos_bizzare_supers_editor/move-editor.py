from base import input_int
from os.path import join
from cps3utils.crypt import Cps3CryptoIO
from cps3utils.games import ROMCart,jojoban
from inquirer import List, prompt

from config import rom_folder
import character

__desc__ = '''%s - 角色攻击属性编辑''' % jojoban.GAMENAME

class CharacterMove:    
    c01Damage  = '对敌伤害'
    c02StandBarDamage  = '替身条伤害'
    c03MeterBuildOnWhiff  = '攒气值'
    c04MeterBuildOnHit = '受击攒气值'
    c05Blocking1 = '可攻击格挡类型 (0x01/0x02/0x03 - 中、下、上段）'
    c06SpecialFlag = '''特殊攻击类型 0x1D - 击飞 / 0x1B - 击倒 / 0x20 - 撞墙 / 0x2A - 变小孩 / 0x31 - 抓投 / 0x27 - 击飞（出屏）/ 0x60 - softlock(real)'''
    c07LaunchSpeed = '击飞速度 (0x10 出屏）'
    c08AirLockup = '空打'
    c09Blocking2 = '格挡（2） - 0x03+ 则无法格挡'
    c10Blocking3 = '格挡（3） - 0x03+ 则无法格挡'
    c11Hitstop = '硬直？（Hitstop)'
    c12KnockBack = '击回'
    c13Hitspark = '火花特效'
    c14Unknown1 = '...'
    c15HitEffect = '击打特效'
    c16ScreenShake = '屏幕抖动'
    c17Unknown2 = '...'
    c18KnockBackOnBlock = '格挡击飞'
    c19HitStun = '击昏'
    c20HitStun = '格挡致昏'
    c21Unknown3 = '...'
    c22Hitsound = '击打音效'
    c23AirBlocking = '空中格挡'
    c24KillDenial = '防击杀 - 0x01+ 不会KO敌人'
    @staticmethod
    def get_move_names():
        k = sorted(filter(lambda v:not '__' in v and 'c' in v,dir(CharacterMove)),key=lambda v:v[:3])
        return {k:getattr(CharacterMove,k) for k in k}
    @staticmethod
    def buffer_to_moves(buffer):
        moves = CharacterMove()
        for i,nMove in enumerate(moves.get_move_names()):
            setattr(moves,nMove,buffer[i])
        return moves
    @staticmethod
    def moves_to_buffer(moves) -> bytearray:
        buffer = bytearray([getattr(moves,move) for move in moves.get_move_names()])
        return buffer
def __main__():
    print(__desc__)
    rom_10 = Cps3CryptoIO(open(join(rom_folder,'10'),'r+b'),ROMCart.locate_ROMCart('10',jojoban.ROMCARTS),jojoban)

    chara = character.CHARACTERS[prompt([List('chr','角色选择',character.CHARACTERS)])['chr']]
    move      = prompt([List('move','攻击选择',chara.MOVE_POINTERS)])['move']
    move_ptr  = chara.MOVE_POINTERS[move] - 0x6000000

    rom_10.seek(move_ptr)
    bMove = bytearray(rom_10.read(64))
    cMove = CharacterMove.buffer_to_moves(bMove)

    rom_10.seek(-64,1)

    prop = prompt([List('prop','属性选择',cMove.get_move_names().values())])['prop']
    nAttack = list(cMove.get_move_names().keys())[list(cMove.get_move_names().values()).index(prop)]

    nVal = input_int('输入新值 （当前:%d (0x%x)）：' % (getattr(cMove,nAttack),getattr(cMove,nAttack)))

    setattr(cMove,nAttack,nVal)
    bMove = cMove.moves_to_buffer(cMove)
    rom_10.write(bMove)

if __name__ == '__main__':
    __main__()