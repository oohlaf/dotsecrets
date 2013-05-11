import re
import sys
import yaml

from collections import OrderedDict
from textsub import Textsub
from util import warning


keyword_dict = {
        '(?#QuotedString)'       : r'("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')',
        '(?#QuotedOrSingleWord)' : r'("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\'|\S+)',
        '(?#UpToHash)'           : r'([^\s#]+(?:[ \t\v\f]*[^\s#]+)+)',
        '(?#UpToSemicolon)'      : r'([^\s;]+(?:[ \t\v\f]*[^\s;]+)+)',
}
keyword_sub = Textsub(keyword_dict)
keyword_sub.compile()


class CleanTemplate(object):
    def __init__(self, template_type, rules=[]):
        self.template_type = template_type
        self.rules = rules
        self.set_parent_rules()

    def __getstate__(self):
        state = OrderedDict()
        state['type'] = self.template_type
        state['rules'] = self.rules
        return state

    def __setstate__(self, state):
        self.template_type = state['type']
        self.rules = state['rules']

    def set_parent_rules(self):
        for rule in self.rules:
            rule.template = self

    def sub(self, line):
        for rule in self.rules:
            line = rule.sub(line)
        return line


def clean_template_representer(dumper, data):
    return dumper.represent_mapping(u'!Template', data.__getstate__().items(), False)


def clean_template_constructor(loader, node):
    mapping = loader.construct_mapping(node)
    if 'type' in mapping:
        mapping['template_type'] = mapping['type']
        del mapping['type']
    return CleanTemplate(**mapping)


class CleanSecret(object):
    def __init__(self, key, regex, substitute, description='', numbered=False):
        self.key = key
        self.description = description
        self.numbered = numbered
        self.regex = regex
        self.substitute = substitute
        self.n = 0
        self.template = None

    def __getstate__(self):
        state = OrderedDict()
        state['key'] = self.key
        state['description'] = self.description
        state['numbered'] = self.numbered
        state['regex'] = self._orig_regex
        state['substitute'] = self._substitute
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.n = 0
        self.template = None

    def get_regex(self):
        return self._regex

    def set_regex(self, regex):
        self._orig_regex = regex
        regex = keyword_sub.sub(regex)
        self._regex = re.compile(regex)

    regex = property(get_regex, set_regex)

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
            self.n += 1
            out += m.expand(self.substitute)
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
            key += self.key + '_' + unicode(self.n)
        else:
            key += self.key
        return self._substitute.replace('(?#Key)', '$DotBrief: ' + key + '$')

    def set_substitute(self, substitute):
        self._substitute = substitute

    substitute = property(get_substitute, set_substitute)


def clean_secret_representer(dumper, data):
    return dumper.represent_mapping(u'!Secret', data.__getstate__().items(), False)


def clean_secret_constructor(loader, node):
    mapping = loader.construct_mapping(node)
    return CleanSecret(**mapping)


class CopyTemplate(object):
    def sub(self, line):
        return line


def create_config():
    s = []
    s.append(CleanSecret("passwd",
            r'password(\s*)=(\s*)(?#QuotedOrSingleWord)',
            r'password\1=\2(?#Key)', 'Mutt passwords', True))
    t = []
    t.append(CleanTemplate('mutt', s))
    config_file = open('.dotbrief.yaml', 'w')
    yaml.dump_all(t, config_file)
    config_file.close()


def load_config(template_type, filename):
    if filename is None:
        filename = '.dotbrief.yaml'
    with open(filename, 'r') as config_file:
        for template in yaml.load_all(config_file):
            if template.template_type == template_type:
                template.set_parent_rules()
                return template
    return None


def clean(args):
    yaml.add_representer(CleanTemplate, clean_template_representer)
    yaml.add_constructor(u'!Template', clean_template_constructor)
    yaml.add_representer(CleanSecret, clean_secret_representer)
    yaml.add_constructor(u'!Secret', clean_secret_constructor)

    template = load_config(args.type, args.config)
    if template is None:
        warning("No template found")
        template = CopyTemplate()
    while 1:
        try:
            line = args.input.readline()
        except KeyboardInterrupt:
            break
        if not line:
            break
        args.output.write(template.sub(line))
