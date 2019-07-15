#!/usr/bin/env python

import argparse
import logging
import sys

from dotsecrets.clean import clean
from dotsecrets.init import init
from dotsecrets.smudge import smudge
from dotsecrets.stow import stow, unstow


logger = logging.getLogger()

logging_configured = False

log_levels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


def configure_logging(args):
    global logging_configured
    if not logging_configured:
        logger.setLevel(log_levels[args.log_level])
        console_log = logging.StreamHandler(stream=sys.stderr)
        logger.addHandler(console_log)
        logging_configured = True


def main():
    parser = argparse.ArgumentParser(description='Manage dotfiles '
                                                 'with secrets')
    parser.add_argument('--log-level', metavar='LEVEL',
                        choices=log_levels.keys(), default='warning',
                        help="set logging to LEVEL, where LEVEL is "
                             "one of %(choices)s; default is %(default)s")
    subparsers = parser.add_subparsers()

    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument('--input', metavar='FILE', default='-',
                             help="read input from FILE, "
                                  "default is '-' stdin")
    file_parser.add_argument('--output', metavar='FILE', default='-',
                             help="write output to FILE, "
                                  "default is '-' stdout")

    parser_clean = subparsers.add_parser('clean', parents=[file_parser])
    parser_clean.add_argument('--filters', metavar='FILE',
                              help='load filters from FILE')
    parser_clean.add_argument('name')
    parser_clean.set_defaults(func=clean)

    parser_smudge = subparsers.add_parser('smudge', parents=[file_parser])
    parser_smudge.add_argument('--filters', metavar='FILE',
                               help='load filters from FILE')
    parser_smudge.add_argument('--store', metavar='FILE',
                               help='load secrets from FILE')
    parser_smudge.add_argument('name')
    parser_smudge.set_defaults(func=smudge)

    dploy_parser = argparse.ArgumentParser(add_help=False)
    dploy_parser.add_argument('--all', dest='source_all',
                              action='store_true',
                              help='act on all top level directories')
    dploy_parser.add_argument('--dry-run', dest='is_dry_run',
                              action='store_true',
                              help='simulate actions')
    dploy_parser.add_argument('source', nargs='*',
                              help="source directory to act upon")

    parser_stow = subparsers.add_parser('stow', parents=[dploy_parser])
    parser_stow.set_defaults(func=stow)

    parser_unstow = subparsers.add_parser('unstow', parents=[dploy_parser])
    parser_unstow.set_defaults(func=unstow)

    parser_init = subparsers.add_parser('init')
    parser_init.add_argument('--filters', metavar='FILE',
                             help='load filters from FILE')
    parser_init.add_argument('--store', metavar='FILE',
                             help='load secrets from FILE')
    parser_init.set_defaults(func=init)

    args = parser.parse_args()
    configure_logging(args)
    try:
        args.func(args)
    except AttributeError as exc:
        try:
            if exc.args[0] == "'Namespace' object has no attribute 'func'":
                parser.error("too few arguments")
        except (KeyError, AttributeError):
            pass
        else:
            logger.exception(exc, exc_info=logger.isEnabledFor(logging.DEBUG))
    except Exception as exc:
        logger.exception(exc, exc_info=logger.isEnabledFor(logging.DEBUG))


if __name__ == '__main__':
    main()
