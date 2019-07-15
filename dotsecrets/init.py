import logging
import random
import re
import shutil
import string
import subprocess

from pathlib import Path

from dotsecrets.clean import load_all_filters, get_clean_filter
from dotsecrets.smudge import (load_all_secrets,
                               get_smudge_filter,
                               smudge_stream)
from dotsecrets.params import GIT_ATTR_DOTSECRETS
from dotsecrets.utils import get_dotfiles_path, is_sub_path


logger = logging.getLogger(__name__)


def check_git_config():
    cwd_path = Path.cwd()
    dotfiles_path = get_dotfiles_path()
    if not is_sub_path(cwd_path, dotfiles_path):
        return False
    try:
        subprocess.run(['git', 'config',
                        '--get', 'filter.dotsecrets.clean'],
                       stdout=subprocess.DEVNULL,
                       check=True)
    except subprocess.CalledProcessError:
        subprocess.run(['git', 'config', '--local',
                        'filter.dotsecrets.clean',
                        'dotsecrets clean %f'],
                       stdout=subprocess.DEVNULL,
                       check=True)
    try:
        subprocess.run(['git', 'config',
                        '--get', 'filter.dotsecrets.smudge'],
                       stdout=subprocess.DEVNULL,
                       check=True)
    except subprocess.CalledProcessError:
        subprocess.run(['git', 'config', '--local',
                        'filter.dotsecrets.smudge',
                        'dotsecrets smudge %f'],
                       stdout=subprocess.DEVNULL,
                       check=True)
    try:
        subprocess.run(['git', 'config',
                        '--get', 'filter.dotsecrets.required'],
                       stdout=subprocess.DEVNULL,
                       check=True)
    except subprocess.CalledProcessError:
        subprocess.run(['git', 'config', '--local',
                        'filter.dotsecrets.required',
                        'true'],
                       stdout=subprocess.DEVNULL,
                       check=True)
    return True


def contains_filter_definition(git_attr_file):
    pattern = re.compile(GIT_ATTR_DOTSECRETS)
    with open(git_attr_file, 'r', encoding='utf-8') as f:
        for line in f:
            if pattern.match(line):
                return True
    return False


def append_filter_definition(git_attr_file):
    with open(git_attr_file, 'a', encoding='utf-8') as f:
        f.write('* filter=dotsecrets\n')


def check_git_attributes():
    dotfiles_path = get_dotfiles_path()
    git_info_attr_file = dotfiles_path.joinpath('.git/info/attributes')
    if git_info_attr_file.exists():
        if contains_filter_definition(git_info_attr_file):
            return True
    git_attr_file = dotfiles_path.joinpath('.gitattributes')
    if git_attr_file.exists():
        if contains_filter_definition(git_attr_file):
            return True
    append_filter_definition(git_attr_file)
    return True


def initial_smudge(filters_file, secrets_file):
    filters_dict, filters_file = load_all_filters(filters_file)
    secrets_dict, secrets_file = load_all_secrets(secrets_file)
    dotfiles_path = get_dotfiles_path()
    for name in filters_dict['filters']:
        clean_filter = get_clean_filter(name, filters_file, filters_dict)
        smudge_filter = get_smudge_filter(name, secrets_file, secrets_dict)
        smudge_filter.read_mode = clean_filter.read_mode
        smudge_filter.write_mode = clean_filter.write_mode
        smudge_filter.encoding = clean_filter.encoding
        source_file = dotfiles_path.joinpath(name)
        source_stat = source_file.stat()
        random_string = ''.join([random.choice(string.ascii_lowercase)
                                 for i in range(16)])
        dest_file = source_file.with_name(source_file.name + '.' +
                                          random_string)
        smudge_stream(source_file, dest_file, smudge_filter)
        shutil.copystat(source_file, dest_file)
        shutil.chown(dest_file, source_stat.st_uid, source_stat.st_gid)
        dest_file.rename(source_file)


def init(args):
    if check_git_config() and check_git_attributes():
        initial_smudge(args.filters, args.store)
