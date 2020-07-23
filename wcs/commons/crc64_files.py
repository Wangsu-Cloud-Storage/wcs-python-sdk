import argparse
from wcs.commons.util import file_crc64



def main():
    parser = argparse.ArgumentParser(prog='WCS Python SDK')
    sub_parsers = parser.add_subparsers()
    parser_etag = sub_parsers.add_parser(
        'crc64', description='calculating 64-bit CRC value', help='crc64 [file...]')
    parser_etag.add_argument(
        'crc64_files', metavar='N', nargs='+', help='tthe file list for calculate crc64')

    args = parser.parse_args()
    try:
        crc64_files = args.crc64_files
    except AttributeError:
        crc64_files = None

    if crc64_files:
        print(crc64_files)
        r = [file_crc64(file) for file in crc64_files]
        if len(r) == 1:
            print(r[0])
        else:
            print(' '.join([str(i) for i in r]))

if __name__ == '__main__':
    main()

