DotSecrets
==========

DotSecrets [1]_ is a tool to facilitate keeping your dotfiles in Git, including
those with private information.

By keeping your configuration files in a public Git repository, you can share
your settings with others. Any private information is kept in a single file
store outside the repository. It's up to the user to transport this file.

This tool is similar in functionality to Briefcase [2]_ but differs
significantly. DotSecrets uses Git filtering to manage private information and
uses a different file hierarchy and naming convention.

For more information on the filtering capabilities of Git, see the
git attributes manual [3]_ in section Effects under filter attribute.


Dependencies
------------

DotSecrets depends on PyYAML [4]_ for reading configuration files.


Installation
------------

Run::

    $ pip3 install .

You should then have a ``dotsecrets`` script available in a new shell.

You might need to symlink it into your ``~/bin`` folder::

    $ ln -s ~/.local/bin/dotsecrets ~/bin



Usage
-----

DotSecrets is to be used together with Git to manage your dotfiles.

Git filters are used to clean and smudge secrets. Each filter is configured
using regular expressions grouped per filter name.


Filters
-------

Filter rules are defined in a file called ``.dotfilters.yaml`` inside the
dotfiles repository.

Its syntax is as follows:

.. code-block:: yaml

    version: 2
    filters:
      "mutt/.mutt/muttrc":
        rules:
          passwd:
            description: Mutt passwords
            numbered: true
            regex: password(\s*)=(\s*)(?#WSUpToHash)
            substitute: password\1=\2(?#Key)
      "irssi/.irssi/config":
        rules:
          nickname:
            description: IRC nickname
            regex: nick(\s*)=(\s*)(?#QuotedString);
            substitute: nick\1=\2"(?#Key)";
          realname:
            regex: real_name(\s*)=(\s*)(?#QuotedString);
            substitute: real_name\1=\2"(?#Key)";

This file contains filter rules for each file that contains secrets. The
first example defines a filter for replacing passwords in mutt configuration
files. A secret is detected by a regular expression matching on each line
containing the word ``password`` followed by an equal sign and each character
(except whitespace) up to an optional hash ``#`` comment.

A match is replaced by the following: ``password = $DotSecrets: password_1$``.
The key is appended with the number of matches because ``numbered`` is defined
as ``true``. This allows for multiple matches and substitutions as long as the
ordering in the file is retained.

The second example shows a filter for hiding your nickname in an Irssi
configuration file. The regular expression matches any line containing the
word nick followed by whitespace and one or more alphanumeric characters. A
match is replaced by ``nick = "$DotSecrets: nickname$";``.

Similar for the filter to hide your real name in the same file. The regular
expression matches any line containing ``real_name`` followed by an equal
sign, quoted text and a final semi-colon. A match is replaced by
``real_name = "$DotSecrets: realname$";``.

Please note that the description and number fields are optional.

The regular expressions and substitutions follow the Python regular expression
syntax [5]_. Substitutions can reference regex groups ``(...)`` using
``\number`` syntax. To make it easier to define complex regular expressions,
the following hortcuts are available. They are defined as regex comments
``(?#...)``:

======================  ====================================================
Shortcut                Description
======================  ====================================================
(?#QuotedString)        Matches balanced single or double quoted strings and
                        is able to cope with escaped quote symbols within
                        the string
(?#QuotedOrSingleWord)  Same as QuotedString or an unquoted single word of
                        non-whitespace characters
(?#WSUpToHash)          Matches whitespace up to the hash symbol ``#``
(?#WSUpToSemicolon)     Matches whitespace up to the semi colon symbol ``;``
(?#Key)                 Used to substitute the secret
======================  ====================================================


Secrets
-------

Secret information, like passwords, answers to security questions, and other
sensitive information is stored in a file called ``dotsecrets.yaml`` inside
the XDG configuration directory (typically
``~/.config/dotsecrets/dotsecrets.yaml``).

Its syntax is as follows:

.. code-block:: yaml

    version: 2
    filters:
      "mutt/.mutt/muttrc":
        secrets:
          password_1:
            description: Password for GMail
            secret: s3cr3t
          password_2:
            description: Password for Hotmail
            secret: f00bar
      "irssi/.irssi/config":
        secrets:
          nick:
            secret: mynick
          realname:
            secret: My Real Name

This configuration file contains two filters for mutt and irssi. Each
filter contains one or more secrets. These secrets are used to filter the
files in the Git repository for sensitive data.


Linking filters and secrets
---------------------------

Git attributes are used to link file patterns to Git filters. The filters are
defined in git config files.

Contents of ``.gitattributes``::

    * filter=dotsecrets

When checking in files with Git, the clean command is run for those files that
match the pattern given in ``.gitattributes``. When checking out files that
have a filter defined, the smudge command substitutes the secrets again.

To add these filters run the following commands::

    git config filter.dotsecrets.clean "dotsecrets clean %f"
    git config filter.dotsecrets.smudge "dotsecrets smudge %f"
    git config filter.dotsecrets.required true

They result in the following addition to your ``.git/config`` file:

.. code-block:: ini

    [filter "dotsecrets"]
        clean = dotsecrets clean %f
        smudge = dotsecrets smudge %f
        required = true


References
==========

.. [1] https://github.com/oohlaf/dotsecrets
.. [2] https://github.com/jim/briefcase
.. [3] https://git-scm.com/docs/gitattributes
.. [4] https://pypi.python.org/pypi/PyYAML
.. [5] https://docs.python.org/3/library/re.html#regular-expression-syntax
