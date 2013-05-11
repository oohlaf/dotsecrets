from __future__ import print_function

import sys


def warning(*objs):
    print('WARNING:', *objs, end='\n', file=sys.stderr)


def error(*objs):
    print('ERROR:', *objs, end='\n', file=sys.stderr)
