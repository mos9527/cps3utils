import time
import sys
import argparse
from enum import IntEnum


class GameInfo():
    '''Stub class for game archives'''
    FILENAME = '<undefined>'
    GAMENAME = '<undefined>'
    '''SIMM rom names'''
    SIMM = []
    '''Combined rom names'''
    COMBINED = []
    '''Index of PRG rom in COMBINED,usually 2'''
    PRG_INDEX = 0
    '''CPS3 PRG ROM Key'''
    KEY1 = 0xffffffff
    KEY2 = 0xffffffff


'''BEGIN GAME INFO'''
from jojoban import jojoban
GAMES = [jojoban]

def locate_game_by_name(sname: str):
    '''Locates a game by its shortname,e.g. jojoban'''
    for game in GAMES:
        if game.__name__ == sname:
            return game
    raise Exception("Game not supported : %s" % sname)


def create_default_parser(description='<default tool name>'):
    '''Creates an `argparser` with `game` as its first positional argument'''
    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('game', metavar='GAME',
                        help='Game name (i.e. shortnames,for Jojo HFTF it\'s jojoban)')
    return parser


'''boring CLI stuff'''


def delayed_prompt(line: str, delay=.5, out=sys.stdout):
    out.write('%s\n' % line)
    time.sleep(delay)
    return True


def indexed_selector(l: list, title='', out=sys.stdout):
    if title:
        out.write('%s\n' % title)
    for index, value in enumerate(l, 1):
        out.write('    %s: %s\n' % (str(index).ljust(3), value))
    try:
        index = input('Make your selection [1-%d]:' % len(l))
    except:
        print('Goodbye.')
        sys.exit(0)
    if not index.isnumeric() or int(index) - 1 not in range(0, len(l)):
        out.write(
            'Invalid selection. Input should be within range [1-%d] \n' % len(l))
        time.sleep(1)
        return indexed_selector(l, title, out)
    return int(index) - 1
