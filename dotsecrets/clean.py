import re
import logging

from ruamel.yaml import YAML

from dotsecrets.params import TAG_SECRET_START, TAG_SECRET_END, TAG_SECRET_KEY
from dotsecrets.textsub import Textsub, CopyFilter
from dotsecrets.utils import get_dotfilters_file


yaml = YAML(typ='safe')
logger = logging.getLogger(__name__)


# Regex shortcuts
keyword_dict = {
    # Match a quoted string
    '(?#QuotedString)':
        r'("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')',
    # Match an unquoted single word or a quoted string
    '(?#QuotedOrSingleWord)':
        r'("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\'|\S+)',
    # Match whitespace up to hash symbol
    '(?#WSUpToHash)':
        r'([^\s#]+(?:[ \t\v\f]*[^\s#]+)+)',
    # Match whitespace up to semicolon
    '(?#WSUpToSemicolon)':
        r'([^\s;]+(?:[ \t\v\f]*[^\s;]+)+)',
}
keyword_sub = Textsub(keyword_dict)
keyword_sub.compile()


class CleanFilter(object):
    def __init__(self, name, rules=None):
        if rules is None:
            rules = {}
        self.name = name
        self.rules = rules
        self.parse_rules()

    def parse_rules(self):
        for key, rule_def in self.rules.items():
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


def load_filter(name, filter_file):
    if filter_file is None:
        filter_file = get_dotfilters_file()
    logger.debug("Opening file '%s'.", filter_file)
    with open(filter_file, 'r', encoding='utf-8') as f:
        filter_dict = yaml.load(f)
        try:
            filter_def = filter_dict['filters'][name]
        except KeyError:
            logger.info("No filter named '%s' found in file '%s', "
                        "using copy filter.", name, filter_file)
            return CopyFilter()
        # On success return the actual filter
        return CleanFilter(name=name, rules=filter_def['rules'])
    # Fail safe return default copy filter
    return CopyFilter()


def clean(args):
    clean_filter = load_filter(args.name, args.filters)
    while True:
        try:
            line = args.input.readline()
        except KeyboardInterrupt:
            break
        if not line:
            break
        args.output.write(clean_filter.sub(line))
