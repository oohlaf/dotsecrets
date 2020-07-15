Changes
=======

0.5 (devel)
-----------
- TODO

0.4 (2020-07-15)
----------------
- Forgot to mark the changes list as final with a date
- Decided version 0.4 would be better
- Fixed git tag and minor tweaks to release document

0.3.3 (2020-07-15)
------------------
- Remove PosixPath arguments from shutil methods for compatibility
  with Python 3.5
- Reconfigure text encodings is only available on stdin and stdout
  on Python 3.7+, changing to use io.TextIOWrapper
- More small tweaks for Python 3.5

0.3.2 (2020-07-14)
------------------
- Make code compatible with Python 3.5

0.3.1 (2019-07-25)
------------------
- Testing on PyPI resulted in stricter dependencies

0.3 (2019-07-25)
----------------
- Code changed to Python 3 only
- Based filters on file names which simplifies config a lot
- Breaking change in YAML file config format
- Breaking change in git filter config (one config to rule all secrets)
- Changed YAML parser to ruamel.yaml
- Added stow and unstow command to manage linking of dotfiles
- Added test command to simplify adding new dotfiles

0.2 (2017-08-30)
----------------
- Make code compatible with Python 3

0.1 (2016-07-03)
----------------
- Add console script
- Code clean up, fix pylint warnings

0.0 (2013-05-11)
----------------
- Initial version
