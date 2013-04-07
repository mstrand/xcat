# xcat
XOR cat - a command line tool to XOR a data stream with a given key:

    $ echo -n 'Hello world' | xcat -n 0x03
    Kfool#tlqog

---

## Example usage

The key may be a number...

    $ echo -n AAAAAAAAAAAA | xcat -n 42
    kkkkkkkkkkkk

...or a hexadecimal string...

    $ echo -n AAAAAAAAAAAA | xcat -x 2a2b2c2d2f
    kjmlnkjmlnkj

...or a file...

    $ xcat -f key.bin encrypted.bin > decrypted.bin

...or a counter...

    $ xcat -c 0xef /dev/zero | xxd -p | head -n 2
    eff0f1f2f3f4f5f6f7f8f9fafbfcfdfeff000102030405060708090a0b0c
    0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a

...or a counter with a specific step:

    $ xcat -c 0x1f,-3 /dev/zero | xxd -p | head -n 2
    1f1c191613100d0a070401fefbf8f5f2efece9e6e3e0dddad7d4d1cecbc8
    c5c2bfbcb9b6b3b0adaaa7a4a19e9b9895928f8c898683807d7a7774716e


## Options

    $ xcat -h
    usage: xcat [-h] (-f FILE | -x HEXSTRING | -n NUMBER | -a STRING | -c START)
                [FILE]

    xor a stream of data with a given key

    positional arguments:
      FILE          input filename [default: use stdin]

    optional arguments:
      -h, --help       show this help message and exit
      -f FILE          create key from binary file
      -x HEXSTRING     create key from hexadecimal string
      -n NUMBER        create key from little-endian number
      -a STRING        create key from ASCII string
      -c START[,STEP]  create 256-byte key by counting from START
