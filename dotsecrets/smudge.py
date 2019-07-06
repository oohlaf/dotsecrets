import re
import logging

from ruamel.yaml import YAML

from dotsecrets.params import TAG_SECRET_START, TAG_SECRET_END
from dotsecrets.utils import CopyFilter, get_dotsecrets_file


yaml = YAML(typ='safe')
logger = logging.getLogger(__name__)


class SmudgeFilter(object):
    def __init__(self, name, secrets=None):
        if secrets is None:
            secrets = {}
        self.name = name
        self.secrets = secrets
        self.parse_secrets()
        regex = re.escape(TAG_SECRET_START) + r'(\S+)' + \
            re.escape(TAG_SECRET_END)
        self.regex = re.compile(regex)

    def parse_secrets(self):
        for key, secret_def in self.secrets.items():
            self.secrets[key] = SmudgeSecret(key=key, **secret_def)

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
                out += self.secrets[key].secret
            else:
                out += m.group(0)
                logger.info("No secret found for key '%s' in filter '%s'.",
                            key, self.name)
            prev_start = m.start()
            prev_end = m.end()
        if prev_end != -1:
            out += line[prev_end:]
            return out
        else:
            return line


class SmudgeSecret(object):
    # kwargs allows for additional keyword arguments passed
    # through YAML dictionaries
    def __init__(self, key, secret=None, description='', **kwargs):
        self.key = key
        self.secret = secret
        self.description = description


def load_secrets(name, secret_file):
    if secret_file is None:
        secret_file = get_dotsecrets_file()
    logger.debug("Opening secrets store '%s'.", secret_file)
    with open(secret_file, 'r', encoding='utf-8') as f:
        secret_dict = yaml.load(f)
        try:
            secret_def = secret_dict['filters'][name]
        except KeyError:
            logger.warning("No filter named '%s' found "
                           "in secrets store '%s', "
                           "using copy filter.", name, secret_file)
            return CopyFilter()
        # On success return the actual filter
        return SmudgeFilter(name=name, secrets=secret_def['secrets'])
    # Fail safe return default copy filter
    return CopyFilter()


def smudge(args):
    smudge_filter = load_secrets(args.name, args.store)
    while True:
        try:
            line = args.input.readline()
        except KeyboardInterrupt:
            break
        if not line:
            break
        args.output.write(smudge_filter.sub(line))
