from datetime import datetime as dt

__version_info__ = (0, 3, 2)
__version__ = '.'.join(map(str, __version_info__))


NAME = 'DotSecrets'
PACKAGE_NAME = 'dotsecrets'
VERSION = __version__
LICENSE = 'BSD'
AUTHOR = 'Olaf Conradi'
AUTHOR_EMAIL = 'olaf@conradi.org'
COPYRIGHT = 'Copyright 2013-{}, {}'.format(dt.now().year, AUTHOR)
GITHUB_URL = 'https://github.com/oohlaf/{}'.format(PACKAGE_NAME)
PROJECT_URLS = {
    'Bug Reports': '{}/issues'.format(GITHUB_URL)
}
