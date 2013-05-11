import re
import sys
import yaml

from collections import OrderedDict
from util import warning


class SmudgeTemplate(object):
    def __init__(self, template_type, secrets={}):
        self.template_type = template_type
        self.secrets = secrets
        self.regex = re.compile(r'\$DotBrief: (\S+)\$')

    def __getstate__(self):
        state = OrderedDict()
        state['type'] = self.template_type
        state['secrets'] = self.secrets
        return state

    def __setstate__(self, state):
        self.template_type = state['type']
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
                out += self.secrets[key]
            else:
                out += m.group(0)
                warning("No secret found for key '%s' in template '%s'" % (
                        key,
                        self.template_type))
            prev_start = m.start()
            prev_end = m.end()
        if prev_end != -1:
            out += line[prev_end:]
            return out
        else:
            return line


def smudge_template_representer(dumper, data):
    return dumper.represent_mapping(u'!Template', data.__getstate__().items(), False)


def smudge_template_constructor(loader, node):
    mapping = loader.construct_mapping(node)
    if 'type' in mapping:
        mapping['template_type'] = mapping['type']
        del mapping['type']
    return SmudgeTemplate(**mapping)


def create_secrets():
    s = {}
    s['passwd_1'] = 'H0p1a'
    s['passwd_2'] = 'sdfweg'
    t = []
    t.append(SmudgeTemplate('mutt', s))
    secrets_file = open('.dotsecrets.yaml', 'w')
    yaml.dump_all(t, secrets_file, default_flow_style=False)
    secrets_file.close()


def load_secrets(template_type, filename):
    if filename is None:
        filename = '.dotsecrets.yaml'
    with open(filename, 'r') as secrets_file:
        for template in yaml.load_all(secrets_file):
            if template.template_type == template_type:
                return template
    return None


def smudge(args):
    yaml.add_representer(SmudgeTemplate, smudge_template_representer)
    yaml.add_constructor(u'!Template', smudge_template_constructor)

    template = load_secrets(args.type, args.store)
    if template is None:
        template = CopyTemplate()
    while 1:
        try:
            line = args.input.readline()
        except KeyboardInterrupt:
            break
        if not line:
            break
        args.output.write(template.sub(line))
