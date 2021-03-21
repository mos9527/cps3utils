import argparse
from cps3utils import convert, create_parser, crypt,enter
__desc__ = 'cps3utils - Capcom® CP System III ROM hacking utilites'
def __main__():
    parser = create_parser(__desc__)
    subparser = parser.add_subparsers(help='What to do')
    # adding parser for our modules
    def add_subparser(module,mname):
        parser_m = subparser.add_parser(mname,formatter_class=argparse.RawTextHelpFormatter)
        parser_m.add_argument('--Module-Help',action='store_true',help=module.__desc__)
        module.setup(parser_m)
        parser_m.set_defaults(func=module.__main__)
    add_subparser(convert,'convert')
    add_subparser(crypt,'crypt')
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    enter(__main__,'cps3utils')