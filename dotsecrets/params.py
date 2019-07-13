# Configuration file for filters
DOTFILTERS_FILE = '.dotfilters.yaml'
DOTFILES_PATH = 'dotfiles'

# Location of default secrets store
DOTSECRETS_FILE = 'dotsecrets.yaml'
# Subdirectory name under XDG config home
DOTSECRETS_XDG_NAME = 'dotsecrets'

# Used to tag secrets in dot files
TAG_SECRET_START = '$DotSecrets: '
TAG_SECRET_END = '$'

# Tag used in regex substitution for secret keys
TAG_SECRET_KEY = '(?#Key)'

# Regex shortcuts in dotfilters
DOTFILTERS_KEYWORD_DICT = {
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

# Pattern used to detect presence of the dotsecrets filter in git attributes
GIT_ATTR_DOTSECRETS = r'^[^#].*filter=dotsecrets'
