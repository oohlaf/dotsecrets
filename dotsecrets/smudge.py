import io
import logging
import re
import sys

from ruamel.yaml import YAML

from dotsecrets.clean import get_clean_filter
from dotsecrets.params import TAG_SECRET_START, TAG_SECRET_END
from dotsecrets.utils import get_dotsecrets_file
from dotsecrets.textsub import CopyFilter


yaml = YAML(typ='safe')
logger = logging.getLogger(__name__)


class SmudgeFilter(object):
    def __init__(self, name, secrets=None):
        if secrets is None:
            secrets = {}
        self.name = name
        self.secrets = secrets
        self.read_mode = 'r'
        self.write_mode = 'w'
        self.encoding = 'utf-8'
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


def load_all_secrets(secrets_file=None):
    if secrets_file is None:
        secrets_file = get_dotsecrets_file()
    logger.debug("Opening secrets store '%s'.", secrets_file)
    with open(secrets_file, 'r', encoding='utf-8') as f:
        secrets_dict = yaml.load(f)
    logger.debug("Closed secrets store '%s'.", secrets_file)
    return secrets_dict, secrets_file


def get_smudge_filter(name, secrets_file=None, secrets_dict=None):
    if secrets_dict is None:
        secrets_dict, secrets_file = load_all_secrets(secrets_file)
    try:
        secrets_def = secrets_dict['filters'][name]
    except KeyError:
        logger.warning("No filter named '%s' found in secrets store '%s', "
                       "using copy filter.", name, secrets_file)
        return CopyFilter()
    return SmudgeFilter(name=name, secrets=secrets_def['secrets'])


def smudge_stream(input_file, output_file, smudge_filter):
    if 'b' in smudge_filter.read_mode:
        # Binary mode
        with (open(output_file,
                   mode=smudge_filter.write_mode,
                   encoding=smudge_filter.encoding) if output_file != '-'
              else sys.stdout.buffer) as output_stream:
            with (open(input_file,
                       mode=smudge_filter.read_mode,
                       encoding=smudge_filter.encoding) if input_file != '-'
                  else sys.stdin.buffer) as input_stream:
                while True:
                    try:
                        data = input_stream.read(io.DEFAULT_BUFFER_SIZE)
                    except KeyboardInterrupt:
                        break
                    if not data:
                        break
                    output_stream.write(smudge_filter.sub(data))
    else:
        # Text mode
        if output_file == '-':
            sys.stdout.reconfigure(encoding=smudge_filter.encoding)
        if input_file == '-':
            sys.stdin.reconfigure(encoding=smudge_filter.encoding)
        with (open(output_file,
                   mode=smudge_filter.write_mode,
                   encoding=smudge_filter.encoding) if output_file != '-'
              else sys.stdout) as output_stream:
            with (open(input_file,
                       mode=smudge_filter.read_mode,
                       encoding=smudge_filter.encoding) if input_file != '-'
                  else sys.stdin) as input_stream:
                while True:
                    try:
                        line = input_stream.readline()
                    except KeyboardInterrupt:
                        break
                    if not line:
                        break
                    output_stream.write(smudge_filter.sub(line))


def smudge(args):
    # The mode and encoding for the file is defined in the dotfilter file
    # and put them in the smudge filter
    clean_filter = get_clean_filter(args.name, args.filters)
    smudge_filter = get_smudge_filter(args.name, args.store)
    smudge_filter.read_mode = clean_filter.read_mode
    smudge_filter.write_mode = clean_filter.write_mode
    smudge_filter.encoding = clean_filter.encoding
    smudge_stream(args.input, args.output, smudge_filter)
    return 0
