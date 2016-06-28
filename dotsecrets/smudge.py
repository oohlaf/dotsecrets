import re
import logging
import os
import yaml

from collections import OrderedDict

from clean import TAG_SECRET_START, TAG_SECRET_END
from utils import CopyFilter, is_only_user_readable


logger = logging.getLogger(__name__)


# Location of default secrets store
SECRETS_FILE = 'dotsecrets.yaml'
SECRETS_PATH = os.path.join('.config', 'dotsecrets')


class SmudgeFilter(object):
    def __init__(self, name, secrets={}):
        self.name = name
        self.secrets = secrets
        regex = re.escape(TAG_SECRET_START) + r'(\S+)' + \
                re.escape(TAG_SECRET_END)
        self.regex = re.compile(regex)

    def __getstate__(self):
        state = OrderedDict()
        state['name'] = self.name
        state['secrets'] = self.secrets
        return state

    def __setstate__(self, state):
        self.name = state['name']
        self.secrets = state['secrets']

    def sub(self, line):
        out = u''
        prev_start = -1
        prev_end = -1
        for m in self.regex.finditer(line):
            if prev_start == -1:
                out += line[:m.start()]
            else:
                if m.start() > prev_end:
                    out += line[prev_end:m.start()]
            key = m.group(1)
            if key in self.secrets:
                logger.debug("Replacing key '%s' with secret '%s'.",
                             key, self.secrets[key])
                out += self.secrets[key]
            else:
                out += m.group(0)
                logger.warning("No secret found for key '%s' in filter '%s'.",
                               key, self.name)
            prev_start = m.start()
            prev_end = m.end()
        if prev_end != -1:
            out += line[prev_end:]
            return out
        else:
            return line


def smudge_filter_representer(dumper, data):
    return dumper.represent_mapping(u'!Filter', data.__getstate__().items(),
                                    False)


def smudge_filter_constructor(loader, node):
    mapping = loader.construct_mapping(node)
    return SmudgeFilter(**mapping)


def load_secrets(name, filename):
    if filename is None:
        home_path = os.getenv('HOME', '')
        sec_path = os.getenv('DOTSECRETS_PATH',
                             os.path.join(home_path, SECRETS_PATH))
        filename = os.path.join(sec_path, SECRETS_FILE)
    if not is_only_user_readable(filename):
        logger.error("Insecure file permissions on secrets store '%s'.\n"
                     "Ensure store is only read/writable by user.", filename)
        return None
    logger.debug("Opening secrets store '%s'." % filename)
    with open(filename, 'r') as secrets_file:
        for f in yaml.load_all(secrets_file):
            if f.name == name:
                return f
    logger.warning("No filter named '%s' found in secrets, using copy filter.",
                   name)
    return CopyFilter()


def smudge(args):
    yaml.add_representer(SmudgeFilter, smudge_filter_representer)
    yaml.add_constructor(u'!Filter', smudge_filter_constructor)

    f = load_secrets(args.name, args.store)
    if f is None:
        logger.debug("Could not load any filter or secrets for '%s'.",
                     args.name)
        return
    while 1:
        try:
            line = args.input.readline()
        except KeyboardInterrupt:
            break
        if not line:
            break
        args.output.write(f.sub(line))
