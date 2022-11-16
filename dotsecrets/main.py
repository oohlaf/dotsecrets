#!/usr/bin/env python3
import argparse
import logging
import sys

from pathlib import Path

from dotsecrets.clean import clean
from dotsecrets.init import init
from dotsecrets.metadata import VERSION
from dotsecrets.smudge import smudge
from dotsecrets.stow import stow, unstow
from dotsecrets.test import test


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
    parser = argparse.ArgumentParser(description='manage dotfiles '
                                                 'with secrets')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {}'.format(VERSION))
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

    filter_parser = argparse.ArgumentParser(add_help=False)
    filter_parser.add_argument('--filters', metavar='FILE',
                               help='load filters from FILE', type=Path)

    store_parser = argparse.ArgumentParser(add_help=False)
    store_parser.add_argument('--store', metavar='FILE',
                              help='load secrets from FILE', type=Path)

    init_cmd_parser = subparsers.add_parser('init',
                                            help='initialize fresh Git '
                                                 'checkout',
                                            parents=[filter_parser,
                                                     store_parser])
    init_cmd_parser.set_defaults(func=init)

    clean_cmd_parser = subparsers.add_parser('clean',
                                             help='clean filter used '
                                                  'by Git',
                                             parents=[file_parser,
                                                      filter_parser])
    clean_cmd_parser.add_argument('name',
                                  help='file within repository to filter')
    clean_cmd_parser.set_defaults(func=clean)

    smudge_cmd_parser = subparsers.add_parser('smudge',
                                              help='smudge filter used '
                                                   'by Git',
                                              parents=[file_parser,
                                                       filter_parser,
                                                       store_parser])
    smudge_cmd_parser.add_argument('name',
                                   help='file within repository to filter')
    smudge_cmd_parser.set_defaults(func=smudge)

    dploy_parser = argparse.ArgumentParser(add_help=False)
    dploy_parser.add_argument('--all', dest='source_all',
                              action='store_true',
                              help='act on all topic directories')
    dploy_parser.add_argument('--dry-run', dest='is_dry_run',
                              action='store_true',
                              help='simulate actions')
    dploy_parser.add_argument('source', nargs='*',
                              help='topic directory to act upon')

    stow_cmd_parser = subparsers.add_parser('stow',
                                            help='symlink topic to '
                                                 'home directory',
                                            parents=[dploy_parser])
    stow_cmd_parser.set_defaults(func=stow)

    unstow_cmd_parser = subparsers.add_parser('unstow',
                                              help='remove topic symlink '
                                                   'from home directory',
                                              parents=[dploy_parser])
    unstow_cmd_parser.set_defaults(func=unstow)

    test_cmd_parser = subparsers.add_parser('test',
                                            help='test filter definition',
                                            parents=[filter_parser,
                                                     store_parser])
    test_cmd_parser.add_argument('--keep', action='store_true',
                                 help='keep intermediate files')
    test_cmd_parser.add_argument('name',
                                 help='file within repository to filter')
    test_cmd_parser.set_defaults(func=test)

    args = parser.parse_args()
    configure_logging(args)
    try:
        return args.func(args)
    except AttributeError as exc:
        if exc.args[0] == "'Namespace' object has no attribute 'func'":
            parser.error("too few arguments")
        else:
            logger.exception(exc, exc_info=logger.isEnabledFor(logging.DEBUG))
    except Exception as exc:
        logger.exception(exc, exc_info=logger.isEnabledFor(logging.DEBUG))


if __name__ == '__main__':
    exit(main())
