import sys

from pathlib import Path


if sys.version_info.major == 3 and sys.version_info.minor < 6:
    # Before Python 3.6 resolving was always strict
    def resolve(src: Path, strict=False):
        return src.resolve()
else:
    # Python 3.6+ changes strict resolving to false
    def resolve(src: Path, strict=False):
        return src.resolve(strict)
