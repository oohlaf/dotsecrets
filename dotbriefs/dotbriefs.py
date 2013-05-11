#!/usr/bin/env python

import argparse
import logging
import sys

from clean import clean
from smudge import smudge


logger = logging.getLogger()
logging_configured = False


def configure_logging(args):
    global logging_configured
    if not logging_configured:
        logger.setLevel(logging.DEBUG)
        console_log = logging.StreamHandler(stream=sys.stderr)
        logger.addHandler(console_log)
        logging_configured = True


def main():
    parser = argparse.ArgumentParser(
            description='Manage dot files with secrets')
    subparsers = parser.add_subparsers()

    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument('--input', metavar='FILE',
            type=argparse.FileType('r'), default=sys.stdin,
            help="Read input from FILE, default is '-' stdin")
    file_parser.add_argument('--output', metavar='FILE',
            type=argparse.FileType('w'), default=sys.stdout,
            help="Write output from FILE, default is '-' stdout")

    parser_clean = subparsers.add_parser('clean', parents=[file_parser])
    parser_clean.add_argument('--config', metavar='FILE',
            help='Load config from FILE')
    parser_clean.add_argument('type')
    parser_clean.set_defaults(func=clean)

    parser_smudge = subparsers.add_parser('smudge', parents=[file_parser])
    parser_smudge.add_argument('--store', metavar='FILE',
            help='Load secrets from FILE')
    parser_smudge.add_argument('type')
    parser_smudge.set_defaults(func=smudge)
    
    args=parser.parse_args()
    configure_logging(args)
    args.func(args)


if __name__ == '__main__':
    main()
