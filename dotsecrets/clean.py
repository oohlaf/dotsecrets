import io
import logging
import re
import sys

from ruamel.yaml import YAML

from dotsecrets.params import (TAG_SECRET_START,
                               TAG_SECRET_END,
                               TAG_SECRET_KEY,
                               DOTFILTERS_KEYWORD_DICT)
from dotsecrets.textsub import Textsub, CopyFilter
from dotsecrets.utils import get_dotfilters_file


yaml = YAML(typ='safe')
logger = logging.getLogger(__name__)


keyword_sub = Textsub(DOTFILTERS_KEYWORD_DICT)
keyword_sub.compile()


class CleanFilter(object):
    def __init__(self, name, definition=None):
        if definition is None:
            definition = {'rules': {}}
        self.name = name
        self.rules = {}
        self.read_mode = 'r'
        self.write_mode = 'w'
        self.encoding = 'utf-8'
        self.parse_definition(definition)

    def parse_definition(self, definition):
        self.rules = {}
        if 'encoding' in definition:
            self.encoding = definition['encoding']
        if 'rules' in definition:
            rules = definition['rules']
        else:
            rules = {}
        for key, rule_def in rules.items():
            self.rules[key] = CleanSecret(key=key, **rule_def)

    def sub(self, line):
        for rule in self.rules.values():
            line = rule.sub(line)
        return line


class CleanSecret(object):
    # kwargs allows for additional keyword arguments passed
    # through YAML dictionaries
    def __init__(self, key, regex, substitute, description='', numbered=False,
                 **kwargs):
        # Define property internals
        self._substitute = None
        self._regex = None
        self._orig_regex = None
        # Initialize object with arguments
        self.key = key
        self.description = description
        self.numbered = numbered
        self.regex = regex
        self.substitute = substitute
        self.n = 0

    def get_regex(self):
        return self._regex

    def set_regex(self, regex):
        self._orig_regex = regex
        regex = keyword_sub.sub(regex)
        self._regex = re.compile(regex)

    regex = property(get_regex, set_regex)

    def sub(self, line):
        out = ''
        prev_start = -1
        prev_end = -1
        for m in self.regex.finditer(line):
            if prev_start == -1:
                out += line[:m.start()]
            else:
                if m.start() > prev_end:
                    out += line[prev_end:m.start()]
            self.n += 1
            subs = m.expand(self.substitute)
            logger.debug("Replacing '%s' with '%s'.", m.group(0), subs)
            out += subs
            prev_start = m.start()
            prev_end = m.end()
        if prev_end != -1:
            out += line[prev_end:]
            return out
        else:
            return line

    def get_substitute(self):
        key = ''
        if self.numbered:
            key += self.key + '_' + str(self.n)
        else:
            key += self.key
        return self._substitute.replace(TAG_SECRET_KEY,
                                        TAG_SECRET_START +
                                        key +
                                        TAG_SECRET_END)

    def set_substitute(self, substitute):
        self._substitute = substitute

    substitute = property(get_substitute, set_substitute)


def load_all_filters(filters_file=None):
    if filters_file is None:
        filters_file = get_dotfilters_file()
    logger.debug("Opening filters file '%s'.", filters_file)
    with open(filters_file, 'r', encoding='utf-8') as f:
        filters_dict = yaml.load(f)
    logger.debug("Closed filters file '%s'.", filters_file)
    return filters_dict, filters_file


def get_clean_filter(name, filters_file=None, filters_dict=None):
    if filters_dict is None:
        filters_dict, filters_file = load_all_filters(filters_file)
    try:
        filters_def = filters_dict['filters'][name]
    except KeyError:
        logger.info("No filter named '%s' found in file '%s', "
                    "using copy filter.", name, filters_file)
        return CopyFilter()
    return CleanFilter(name=name, definition=filters_def)


def clean_stream(input_file, output_file, clean_filter):
    if 'b' in clean_filter.read_mode:
        # Binary mode
        with (open(output_file,
                   mode=clean_filter.write_mode,
                   encoding=clean_filter.encoding) if output_file != '-'
              else sys.stdout.buffer) as output_stream:
            with (open(input_file,
                       mode=clean_filter.read_mode,
                       encoding=clean_filter.encoding) if input_file != '-'
                  else sys.stdin.buffer) as input_stream:
                while True:
                    try:
                        data = input_stream.read(io.DEFAULT_BUFFER_SIZE)
                    except KeyboardInterrupt:
                        break
                    if not data:
                        break
                    output_stream.write(clean_filter.sub(data))
    else:
        # Text mode
        if output_file == '-':
            sys.stdout.reconfigure(encoding=clean_filter.encoding)
        if input_file == '-':
            sys.stdin.reconfigure(encoding=clean_filter.encoding)
        with (open(output_file,
                   mode=clean_filter.write_mode,
                   encoding=clean_filter.encoding) if output_file != '-'
              else sys.stdout) as output_stream:
            with (open(input_file,
                       mode=clean_filter.read_mode,
                       encoding=clean_filter.encoding) if input_file != '-'
                  else sys.stdin) as input_stream:
                while True:
                    try:
                        line = input_stream.readline()
                    except KeyboardInterrupt:
                        break
                    if not line:
                        break
                    output_stream.write(clean_filter.sub(line))


def clean(args):
    clean_filter = get_clean_filter(args.name, args.filters)
    clean_stream(args.input, args.output, clean_filter)
