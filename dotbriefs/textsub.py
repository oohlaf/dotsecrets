# Original algorithm by Xavier Defrang.
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/81330
# This implementation by alane@sourceforge.net.

import re
import UserDict


class Textsub(UserDict.UserDict):
    def __init__(self, dict = None):
        self.re = None
        self.regex = None
        UserDict.UserDict.__init__(self, dict)

    def compile(self):
        if len(self.data) > 0:
            tmp = "(%s)" % "|".join(map(re.escape,
                                        self.data.keys()))
            if self.re != tmp:
                self.re = tmp
                self.regex = re.compile(self.re)

    def __call__(self, match):
        return self.data[match.string[match.start():match.end()]]

    def sub(self, s):
        if len(self.data) == 0:
            return s
        return self.regex.sub(self, s)
