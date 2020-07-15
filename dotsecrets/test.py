import logging
import subprocess

from dotsecrets.clean import get_clean_filter, clean_stream
from dotsecrets.params import TEST_CLEAN_SUFFIX, TEST_SMUDGE_SUFFIX
from dotsecrets.smudge import get_smudge_filter, smudge_stream
from dotsecrets.utils import get_dotfiles_path


logger = logging.getLogger(__name__)


def check_test_results(source_file, clean_file, smudge_file):
    logger.info("Comparing '%s' before and after cleaning",
                source_file)
    try:
        subprocess.run(['diff', '-u',
                        str(source_file), str(clean_file)],
                       # stdout=subprocess.DEVNULL,
                       check=True)
    except subprocess.CalledProcessError:
        logger.info("Source '%s' and cleaned source differ", source_file)
    else:
        logger.warning("Source and cleaned source are identical\n"
                       "Does '%s' contain secrets?", source_file)
        return False
    logger.info("Comparing '%s' before and after smudge",
                source_file)
    try:
        subprocess.run(['diff', '-u',
                        str(source_file), str(smudge_file)],
                       # stdout=subprocess.DEVNULL,
                       check=True)
    except subprocess.CalledProcessError:
        logger.warning("Source '%s' and smudged source differ\n"
                       "Please adjust filter definition or "
                       "validate your stored secrets", source_file)
        return False
    else:
        logger.info("Source '%s' and smudged source are identical",
                    source_file)
        return True


def delete_test_results(clean_file, smudge_file):
    logger.info("Delete intermediate files '%s' and '%s'",
                clean_file, smudge_file)
    try:
        clean_file.unlink()
    except FileNotFoundError:
        pass
    try:
        smudge_file.unlink()
    except FileNotFoundError:
        pass


def test(args):
    repo_path = get_dotfiles_path()
    source_file = repo_path.joinpath(args.name)
    clean_file = source_file.with_suffix(source_file.suffix +
                                         TEST_CLEAN_SUFFIX)
    smudge_file = source_file.with_suffix(source_file.suffix +
                                          TEST_SMUDGE_SUFFIX)
    try:
        clean_filter = get_clean_filter(args.name, args.filters)
        clean_stream(source_file, clean_file, clean_filter)
        smudge_filter = get_smudge_filter(args.name, args.store)
        smudge_filter.read_mode = clean_filter.read_mode
        smudge_filter.write_mode = clean_filter.write_mode
        smudge_filter.encoding = clean_filter.encoding
        smudge_stream(clean_file, smudge_file, smudge_filter)
        if check_test_results(source_file, clean_file, smudge_file):
            return 0
        else:
            return 1
    except TypeError as exc:
        if (exc.args[0] == "cannot use a string pattern on "
                           "a bytes-like object"):
            logger.exception("Binary mismatch between "
                             "clean and smudge filter",
                             exc_info=logger.isEnabledFor(logging.DEBUG))
        else:
            raise
    finally:
        if not args.keep:
            delete_test_results(clean_file, smudge_file)
