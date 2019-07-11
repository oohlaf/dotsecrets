import logging
import shutil

from pathlib import Path
from tempfile import NamedTemporaryFile

from dotsecrets.clean import load_all_filters
from dotsecrets.smudge import (load_all_secrets,
                               get_smudge_filter,
                               smudge_stream)
from dotsecrets.utils import get_dotfiles_path


logger = logging.getLogger(__name__)


def init(args):
    filters_dict, filters_file = load_all_filters(args.filters)
    secrets_dict, secrets_file = load_all_secrets(args.store)
    dotfiles_path = get_dotfiles_path()
    for name in filters_dict['filters']:
        smudge_filter = get_smudge_filter(name, secrets_file, secrets_dict)
        source_file = dotfiles_path.joinpath(name)
        source_stat = source_file.stat()
        tmp_file = NamedTemporaryFile(mode='w', encoding='utf-8',
                                      prefix=source_file.name,
                                      dir=source_file.parent,
                                      delete=False)
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                smudge_stream(f, tmp_file, smudge_filter)
        finally:
            tmp_file.close()
        dest_file = Path(tmp_file.name)
        shutil.copystat(source_file, dest_file)
        shutil.chown(dest_file, source_stat.st_uid, source_stat.st_gid)
        dest_file.rename(source_file)
