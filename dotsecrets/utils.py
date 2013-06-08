import os
import stat


class CopyFilter(object):
    def sub(self, line):
        return line


def is_only_user_readable(filename):
    """Return true if and only if filename is readable by user and
    unreadable by group and others."""
    mode = stat.S_IMODE(os.stat(filename).st_mode)
    return mode == 0600
