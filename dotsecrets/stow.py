import logging

from dploy import stowcmd
from pathlib import Path

from dotsecrets.utils import get_dotfiles_path


logger = logging.getLogger(__name__)


def check_args_source(args, dotfiles_path):
    sources = []
    if args.source_all:
        cwd_path = Path.cwd()
        if ((dotfiles_path == cwd_path) or
                (dotfiles_path in cwd_path.parents)):
            args_sources = []
        else:
            logger.error("Current working directory '%s' not inside "
                         "dotfiles directory '%s'", str(cwd_path),
                         str(dotfiles_path))
            return []
        for child in dotfiles_path.iterdir():
            if child.is_dir() and child.name[0] != '.':
                args_sources.append(child)
    else:
        args_sources = args.source
    for src in args_sources:
        src_path = Path(src).resolve(strict=True)
        if src_path.parent == dotfiles_path:
            sources.append(src_path)
        else:
            logger.warning("Source directory '%s' is not a parent of '%s'",
                           src, str(dotfiles_path))
    return sources


def stow(args):
    dotfiles_path = get_dotfiles_path().resolve(strict=True)
    dest_path = Path.home()
    sources = check_args_source(args, dotfiles_path)
    if not sources:
        return
    if args.is_dry_run or logger.isEnabledFor(logging.INFO):
        silent = False
    else:
        silent = True
    stowcmd.Stow(source=sources, dest=dest_path,
                 is_silent=silent,
                 is_dry_run=args.is_dry_run)


def unstow(args):
    dotfiles_path = get_dotfiles_path().resolve(strict=True)
    dest_path = Path.home()
    sources = check_args_source(args, dotfiles_path)
    if not sources:
        return
    if args.is_dry_run or logger.isEnabledFor(logging.INFO):
        silent = False
    else:
        silent = True
    stowcmd.UnStow(source=sources, dest=dest_path,
                   is_silent=silent,
                   is_dry_run=args.is_dry_run)
