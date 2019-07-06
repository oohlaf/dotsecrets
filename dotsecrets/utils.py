import errno
import logging
import os
import stat

from pathlib import Path

# from dotsecrets.exceptions import DotFilesPathNotFound
from dotsecrets.params import (DOTFILES_PATH,
                               DOTFILTERS_FILE,
                               DOTSECRETS_XDG_NAME,
                               DOTSECRETS_FILE)


logger = logging.getLogger(__name__)


class CopyFilter(object):
    def sub(self, line):
        return line


def get_dotfiles_path():
    env_dotfiles = os.getenv('DOTFILES_PATH', DOTFILES_PATH)
    files_path = Path(env_dotfiles)
    if not files_path.is_absolute():
        files_path = Path.home().joinpath(files_path)
    logger.debug("Dotfiles path is '%s'", files_path)
    return files_path


def get_dotfilters_file():
    filter_path = get_dotfiles_path()
    filter_file = filter_path.joinpath(DOTFILTERS_FILE)
    logger.info("Dotfilters file is '%s'", filter_file)
    return filter_file


def get_dotsecrets_path():
    env_dotsecrets = os.getenv('DOTSECRETS_PATH')
    if env_dotsecrets is not None:
        secrets_path = Path(env_dotsecrets)
        if not secrets_path.is_absolute():
            secrets_path = Path.home().joinpath(secrets_path)
    else:
        env_config_home = os.getenv('XDG_CONFIG_HOME')
        if env_config_home is not None:
            config_path = Path(env_config_home)
        else:
            config_path = Path.home().joinpath('.config')
        secrets_path = config_path.joinpath(DOTSECRETS_XDG_NAME)
    logger.debug("Dotsecrets path is '%s'", secrets_path)
    return secrets_path


def get_dotsecrets_file():
    secrets_path = get_dotsecrets_path()
    secrets_file = secrets_path.joinpath(DOTSECRETS_FILE)
    logger.info("Dotsecrets file is '%s'", secrets_file)
    mode = stat.S_IMODE(secrets_file.stat().st_mode)
    if mode == 0o600:
        return secrets_file
    else:
        msg = "Bad file ownership, " \
              "please make file readable for user only (0600)"
        raise PermissionError(errno.EACCES, msg, str(secrets_file))
