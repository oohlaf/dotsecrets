#!/usr/bin/env python

import argparse
import logging
import sys

from clean import clean
from smudge import smudge


logger = logging.getLogger()

logging_configured = False

log_levels = {
        'debug'    : logging.DEBUG,
        'info'     : logging.INFO,
        'warning'  : logging.WARNING,
        'error'    : logging.ERROR,
        'critical' : logging.CRITICAL
        }


def configure_logging(args):
    global logging_configured
    if not logging_configured:
        logger.setLevel(log_levels[args.log_level])
        console_log = logging.StreamHandler(stream=sys.stderr)
        logger.addHandler(console_log)
        logging_configured = True


def main():
    parser = argparse.ArgumentParser(
            description='Manage dotfiles with secrets')
    parser.add_argument('--log-level', metavar='LEVEL',
            choices=log_levels.keys(), default='warning',
            help="set logging to LEVEL, where LEVEL is "
                 "one of %(choices)s; default is %(default)s")
    subparsers = parser.add_subparsers()

    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument('--input', metavar='FILE',
            type=argparse.FileType('r'), default=sys.stdin,
            help="read input from FILE, default is '-' stdin")
    file_parser.add_argument('--output', metavar='FILE',
            type=argparse.FileType('w'), default=sys.stdout,
            help="write output from FILE, default is '-' stdout")

    parser_clean = subparsers.add_parser('clean', parents=[file_parser])
    parser_clean.add_argument('--filters', metavar='FILE',
            help='load filters from FILE')
    parser_clean.add_argument('name')
    parser_clean.set_defaults(func=clean)

    parser_smudge = subparsers.add_parser('smudge', parents=[file_parser])
    parser_smudge.add_argument('--store', metavar='FILE',
            help='load secrets from FILE')
    parser_smudge.add_argument('name')
    parser_smudge.set_defaults(func=smudge)
    
    args=parser.parse_args()
    configure_logging(args)
    args.func(args)


if __name__ == '__main__':
    main()
