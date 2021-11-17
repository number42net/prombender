import sys
import argparse
from prombender import combine, split, concatenate, pad

# This class is required to print the full help when an error is encountered
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f'error: {message}\n')
        self.print_help()
        sys.exit(2)

def main():
    # Create argument parsers
    parser = MyParser()
    sp = parser.add_subparsers()
    sp.required = True
    sp.dest = 'command'

    # Combine
    arg = sp.add_parser('combine', add_help=False,
        help="Combine ROMS")
    arg.set_defaults(func=combine)    
    req = arg.add_argument_group('required arguments')

    req.add_argument('--out', dest='out_file', metavar="FILE", required=True, type=argparse.FileType('bw'),
        help="Output file")

    opt = arg.add_argument_group('required arguments for regular combine')
    opt.add_argument('--in', dest='in_files', metavar="FILE", type=argparse.FileType('br'), nargs='+',
        help="List of files to combine")

    opt = arg.add_argument_group('required arguments for odd / even combine')    
    opt.add_argument('--even', dest='even_file', metavar="FILE", type=argparse.FileType('br'),
        help="Source file with even bytes")
    opt.add_argument('--odd', dest='odd_file', metavar="FILE", type=argparse.FileType('br'),
        help="Source file with odd bytes")

    # Split
    arg = sp.add_parser('split', add_help=False,
        help="Split ROMS")
    arg.set_defaults(func=split)    
    req = arg.add_argument_group('required arguments')

    req.add_argument('--in', dest='in_file', metavar="FILE", required=True, type=argparse.FileType('br'),
        help="Input file")

    opt = arg.add_argument_group('required arguments for regular split')
    req.add_argument('--out', dest='out_file', metavar="PATTERN", type=str,
        help="Output file pattern. Example: output.bin will result in output-1.bin, output-2.bin, etc.")

    opt = arg.add_argument_group('optional arguments for regular split')
    opt.add_argument('--count', dest='count', metavar="NUMBER", type=int,
        help="Number of files to split the ROM into")

    opt = arg.add_argument_group('required arguments for odd / even split')    
    opt.add_argument('--even', dest='even_file', metavar="FILE", type=argparse.FileType('bw'),
        help="Source file with even bytes")
    opt.add_argument('--odd', dest='odd_file', metavar="FILE", type=argparse.FileType('bw'),
        help="Source file with odd bytes")    

    # Concatenate
    arg = sp.add_parser('concatenate', add_help=False,
        help="Concatenate a file to fill a ROM of a specific size")
    arg.set_defaults(func=concatenate)
    req = arg.add_argument_group('required arguments')

    req.add_argument('--in', dest='in_file', metavar="FILE", required=True, type=argparse.FileType('br'),
        help="Input file")
    req.add_argument('--out', dest='out_file', metavar="FILE", required=True, type=argparse.FileType('bw'),
        help="Output file")

    opt = arg.add_argument_group('optional arguments')
    opt = opt.add_mutually_exclusive_group()
    opt.add_argument('--kbits', dest='kbits', metavar="KILO_BITS", type=int,
        help="Final size in kilobits. Example: for a 27C256 EPROM, set this to 256")

    opt.add_argument('--copies', dest='copies', metavar="NUMBER", type=int,
        help="Number of copies to make. Example: to fill a 256k EPROM with a 64k file set this to 4")

    # Pad
    arg = sp.add_parser('pad', add_help=False,
        help="Concatenate a file to fill a ROM of a specific size")
    arg.set_defaults(func=pad)
    req = arg.add_argument_group('required arguments')

    req.add_argument('--in', dest='in_file', metavar="FILE", required=True, type=argparse.FileType('br'),
        help="Input file")
    req.add_argument('--out', dest='out_file', metavar="FILE", required=True, type=argparse.FileType('bw'),
        help="Output file")
    req.add_argument('--kbits', dest='kbits', metavar="INTEGER", required=True, type=int,
        help="Final size in kbits")
    
    opt = arg.add_argument_group('optional arguments')

    opt_ex = opt.add_mutually_exclusive_group()
    opt_ex.add_argument('--hex', dest='hex_val', metavar="HEX", type=str,
        help="Use the hex value for padding")
    opt_ex.add_argument('--dec', dest='dec_val', metavar="INTEGER", type=int,
        help="Use the decimal value for padding")

    opt_ex = opt.add_mutually_exclusive_group()
    opt_ex.add_argument('--bottom', dest='bottom', action='store_true',
        help="Pad the bottom, data stays at the beginning of the file")
    opt_ex.add_argument('--top', dest='top', action='store_true',
        help="Pad the top, data moves to the end of the file")


    # Prepare function arguments
    args = parser.parse_args()

    arguments = dict(vars(args))
    del arguments['command']
    del arguments['func']

    try:
        args.func(**arguments)
    except Exception as e:
        print (f"Failed: {e}")

if __name__ == "__main__":
    main()