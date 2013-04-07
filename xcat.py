#!/usr/bin/python3

import sys
import argparse
import itertools

def _parse_arguments():

    parser = argparse.ArgumentParser(
        description='xor a stream of data with a given key',
        formatter_class=argparse.RawTextHelpFormatter,
        )

    key_option = parser.add_mutually_exclusive_group(required=True)

    #
    # Every key option is expected to produce an iterable
    # These are conversion functions, used in the 'type' argument for each option
    #
    def _file_iterator(f):
        byte = f.read(1)
        while byte:
            yield byte[0]
            byte = f.read(1)

    def integer(value):
        number = int(value, 0)
        length = number.bit_length() // 8 + 1
        return number.to_bytes(length, byteorder='little')

    def hexstring(value):
        return bytes.fromhex(value)

    def file(value):
        f = open(value, 'rb')
        return _file_iterator(f)

    def ascii(value):
        return value.encode('ascii')

    def counter(value):
        if ',' not in value:
            value += ',1'
        start, step = value.split(',', 2)
        start = int(start, 0)
        step = int(step, 0)
        for i in range(0x100):
            yield (start + i * step) & 0xff

    key_option.add_argument(
        '-f',
        dest='key',
        metavar='FILE',
        type=file,
        help='create key from binary file',
        )
    key_option.add_argument(
        '-x',
        dest='key',
        metavar='HEXSTRING',
        type=hexstring,
        help='create key from hexadecimal string'
        )
    key_option.add_argument(
        '-n',
        dest='key',
        metavar='NUMBER',
        type=integer,
        help='create key from little-endian number'
        )
    key_option.add_argument(
        '-a',
        dest='key',
        metavar='STRING',
        type=ascii,
        help='create key from ASCII string'
        )
    key_option.add_argument(
        '-c',
        dest='key',
        metavar='START[,STEP]',
        type=counter,
        help='create 256-byte key by counting from START',
        )

    parser.add_argument(
            'data',
            nargs='?',
            metavar='FILE',
            type=file,
            default=_file_iterator(sys.stdin.buffer),
            help='input filename [default: use stdin]',
            )

    return parser.parse_args()

if __name__ == '__main__':

    args = _parse_arguments()
    key = args.key

    #
    # Python installs some signal handlers that raise Python exceptions
    # These lines restore normal UNIX behaviour for SIGINT/SIGPIPE
    # - Ctrl+C will now work as expected
    # - xcat ... | head will also work as expected
    #
    import signal
    try:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except AttributeError:
        pass

    for b, k in zip(args.data, itertools.cycle(key)):
        output = bytes((b ^ k,))
        sys.stdout.buffer.write(output)
