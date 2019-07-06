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
