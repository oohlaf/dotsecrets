Making a DotSecrets release
===========================

This document describes the actions to take when releasing a new version.


Preflight check
---------------

1.  Check if the ``CHANGES.rst`` is up to date with the changes part of this
    release.

2.  Check if ``AUTHORS`` needs to be updated for contributors.

3.  Ensure the working tree is clean and up to date::

        ~/src/dotsecrets$ source venv/bin/activate
        (venv) ~/src/dotsecrets$ git pull
        Already up to date.
        (venv) ~/src/dotsecrets$ git status
        On branch master
        Your branch is up to date with 'origin/master'.
        
        nothing to commit, working tree clean


4.  Ensure all the tests pass::

        (venv) ~/src/dotsecrets$ python setup.py test
        running test
        running egg_info
        writing top-level names to dotsecrets.egg-info/top_level.txt
        writing requirements to dotsecrets.egg-info/requires.txt
        writing entry points to dotsecrets.egg-info/entry_points.txt
        writing dotsecrets.egg-info/PKG-INFO
        writing dependency_links to dotsecrets.egg-info/dependency_links.txt
        reading manifest file 'dotsecrets.egg-info/SOURCES.txt'
        writing manifest file 'dotsecrets.egg-info/SOURCES.txt'
        running build_ext
        test_regex_sub (tests.test_clean.TestCleanSecret)
        Test regex substitution with predefined short cuts ... ok
        test_sub_qs_single_match (tests.test_clean.TestCleanSecret)
        Test quotedstring single match two times ... ok
        test_sub_qs_single_match_inner_dquotes (tests.test_clean.TestCleanSecret)
        Test quotedstring single match with inner double quotes ... ok
        test_sub_qs_single_match_inner_squotes (tests.test_clean.TestCleanSecret)
        Test quotedstring single match with inner single quotes ... ok
        test_sub_uth_double_match_in_comment (tests.test_clean.TestCleanSecret)
        Test uptohash one match before comment, ... ok
        test_sub_uth_no_match (tests.test_clean.TestCleanSecret)
        Test uptohash copy line on no match ... ok
        test_sub_uth_single_match (tests.test_clean.TestCleanSecret)
        Test uptohash single match ... ok
        test_sub_uth_single_match_comment (tests.test_clean.TestCleanSecret)
        Test uptohash single match with comment ... ok
        test_sub_uth_single_match_inside_comment (tests.test_clean.TestCleanSecret)
        Test uptohash single match inside comment ... ok
        test_double_sub (tests.test_smudge.TestSmudgeFilter) ... ok
        test_nokey_sub (tests.test_smudge.TestSmudgeFilter) ... ok
        test_nomatch_sub (tests.test_smudge.TestSmudgeFilter) ... ok
        test_nosecret_sub (tests.test_smudge.TestSmudgeFilter) ... ok
        test_single_sub (tests.test_smudge.TestSmudgeFilter) ... ok
        test_copyfilter (tests.test_utils.TestUtils)
        Test copy filter ... ok
    
        ----------------------------------------------------------------------
        Ran 15 tests in 0.013s
    
        OK


Making a release
----------------

1.  Remove prior build artifacts and ensure the working tree is clean::

        (venv) ~/src/dotsecrets$ rm -rf build/ dist/ *.egg-info
        (venv) ~/src/dotsecrets$ git status
        On branch master
        Your branch is up to date with 'origin/master'.
        
        nothing to commit, working tree clean


2.  Ensure that recent wheel and setuptools are installed::

        (venv) ~/src/dotsecrets$ pip install --upgrade wheel setuptools
        Requirement already satisfied: wheel in ./venv/lib/python3.5/site-packages (0.34.2)
        Requirement already up-to-date: setuptools in ./venv/lib/python3.5/site-packages (49.2.0)


3.  Ensure that twine is installed::

        (venv) ~/src/dotsecrets$ pip install twine
        Requirement already satisfied: twine in ./venv/lib/python3.5/site-packages (1.15.0)
        Requirement already satisfied: requests!=2.15,!=2.16,>=2.5.0 in ./venv/lib/python3.5/site-packages (from twine) (2.24.0)
        Requirement already satisfied: pkginfo>=1.4.2 in ./venv/lib/python3.5/site-packages (from twine) (1.5.0.1)
        Requirement already satisfied: tqdm>=4.14 in ./venv/lib/python3.5/site-packages (from twine) (4.47.0)
        Requirement already satisfied: setuptools>=0.7.0 in ./venv/lib/python3.5/site-packages (from twine) (28.8.0)
        Requirement already satisfied: requests-toolbelt!=0.9.0,>=0.8.0 in ./venv/lib/python3.5/site-packages (from twine) (0.9.1)
        Requirement already satisfied: readme-renderer>=21.0 in ./venv/lib/python3.5/site-packages (from twine) (26.0)
        Requirement already satisfied: chardet<4,>=3.0.2 in ./venv/lib/python3.5/site-packages (from requests!=2.15,!=2.16,>=2.5.0->twine) (3.0.4)
        Requirement already satisfied: idna<3,>=2.5 in ./venv/lib/python3.5/site-packages (from requests!=2.15,!=2.16,>=2.5.0->twine) (2.10)
        Requirement already satisfied: certifi>=2017.4.17 in ./venv/lib/python3.5/site-packages (from requests!=2.15,!=2.16,>=2.5.0->twine) (2020.6.20)
        Requirement already satisfied: urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 in ./venv/lib/python3.5/site-packages (from requests!=2.15,!=2.16,>=2.5.0->twine) (1.25.9)
        Requirement already satisfied: Pygments>=2.5.1 in ./venv/lib/python3.5/site-packages (from readme-renderer>=21.0->twine) (2.6.1)
        Requirement already satisfied: six in ./venv/lib/python3.5/site-packages (from readme-renderer>=21.0->twine) (1.15.0)
        Requirement already satisfied: bleach>=2.1.0 in ./venv/lib/python3.5/site-packages (from readme-renderer>=21.0->twine) (3.1.5)
        Requirement already satisfied: docutils>=0.13.1 in ./venv/lib/python3.5/site-packages (from readme-renderer>=21.0->twine) (0.16)
        Requirement already satisfied: packaging in ./venv/lib/python3.5/site-packages (from bleach>=2.1.0->readme-renderer>=21.0->twine) (20.4)
        Requirement already satisfied: webencodings in ./venv/lib/python3.5/site-packages (from bleach>=2.1.0->readme-renderer>=21.0->twine) (0.5.1)
        Requirement already satisfied: pyparsing>=2.0.2 in ./venv/lib/python3.5/site-packages (from packaging->bleach>=2.1.0->readme-renderer>=21.0->twine) (2.4.7)


4.  Change the version number in ``dotsecrets/metadata.py`` usually by
    removing the fourth element. Make sure to follow PEP-440 [1]_ and the
    semantic versioning guidelines [2]_.

    Typically the diff would look like this::

        (venv) ~/src/dotsecrets$ git diff dotsecrets/metadata.py
        diff --git a/dotsecrets/metadata.py b/dotsecrets/metadata.py
        index e51f521..5fd31e8 100644
        --- a/dotsecrets/metadata.py
        +++ b/dotsecrets/metadata.py
        @@ -1,6 +1,6 @@
         from datetime import datetime as dt
        
         -__version_info__ = (0, 3, 3, "dev0")
         +__version_info__ = (0, 3, 3)
          __version__ = '.'.join(map(str, __version_info__))


5.  Commit the version change::

        (venv) ~/src/dotsecrets$ git add dotsecrets/metadata.py
        (venv) ~/src/dotsecrets$ git commit -m "Ready for release v0.3.3"


6.  Do a source build::

        (venv) ~/src/dotsecrets$ python setup.py sdist
        running sdist
        running egg_info
        creating dotsecrets.egg-info
        writing dotsecrets.egg-info/PKG-INFO
        writing top-level names to dotsecrets.egg-info/top_level.txt
        writing dependency_links to dotsecrets.egg-info/dependency_links.txt
        writing requirements to dotsecrets.egg-info/requires.txt
        writing entry points to dotsecrets.egg-info/entry_points.txt
        writing manifest file 'dotsecrets.egg-info/SOURCES.txt'
        warning: Failed to find the configured license file 'L'
        warning: Failed to find the configured license file 'C'
        warning: Failed to find the configured license file 'N'
        reading manifest file 'dotsecrets.egg-info/SOURCES.txt'
        reading manifest template 'MANIFEST.in'
        writing manifest file 'dotsecrets.egg-info/SOURCES.txt'
        running check
        creating dotsecrets-0.3.3
        creating dotsecrets-0.3.3/dotsecrets
        creating dotsecrets-0.3.3/dotsecrets.egg-info
        copying files to dotsecrets-0.3.3...
        copying AUTHORS -> dotsecrets-0.3.3
        copying CHANGES.rst -> dotsecrets-0.3.3
        copying LICENSE -> dotsecrets-0.3.3
        copying MANIFEST.in -> dotsecrets-0.3.3
        copying README.rst -> dotsecrets-0.3.3
        copying RELEASE.rst -> dotsecrets-0.3.3
        copying setup.cfg -> dotsecrets-0.3.3
        copying setup.py -> dotsecrets-0.3.3
        copying dotsecrets/__init__.py -> dotsecrets-0.3.3/dotsecrets
        copying dotsecrets/clean.py -> dotsecrets-0.3.3/dotsecrets
        copying dotsecrets/compat.py -> dotsecrets-0.3.3/dotsecrets
        copying dotsecrets/init.py -> dotsecrets-0.3.3/dotsecrets
        copying dotsecrets/main.py -> dotsecrets-0.3.3/dotsecrets
        copying dotsecrets/metadata.py -> dotsecrets-0.3.3/dotsecrets
        copying dotsecrets/params.py -> dotsecrets-0.3.3/dotsecrets
        copying dotsecrets/smudge.py -> dotsecrets-0.3.3/dotsecrets
        copying dotsecrets/stow.py -> dotsecrets-0.3.3/dotsecrets
        copying dotsecrets/test.py -> dotsecrets-0.3.3/dotsecrets
        copying dotsecrets/textsub.py -> dotsecrets-0.3.3/dotsecrets
        copying dotsecrets/utils.py -> dotsecrets-0.3.3/dotsecrets
        copying dotsecrets.egg-info/PKG-INFO -> dotsecrets-0.3.3/dotsecrets.egg-info
        copying dotsecrets.egg-info/SOURCES.txt -> dotsecrets-0.3.3/dotsecrets.egg-info
        copying dotsecrets.egg-info/dependency_links.txt -> dotsecrets-0.3.3/dotsecrets.egg-info
        copying dotsecrets.egg-info/entry_points.txt -> dotsecrets-0.3.3/dotsecrets.egg-info
        copying dotsecrets.egg-info/requires.txt -> dotsecrets-0.3.3/dotsecrets.egg-info
        copying dotsecrets.egg-info/top_level.txt -> dotsecrets-0.3.3/dotsecrets.egg-info
        Writing dotsecrets-0.3.3/setup.cfg
        creating dist
        Creating tar archive
        removing 'dotsecrets-0.3.3' (and everything under it)


7.  Do a binary wheel build::

        (venv) ~/src/dotsecrets$ python setup.py bdist_wheel
        running bdist_wheel
        running build
        running build_py
        creating build
        creating build/lib
        creating build/lib/dotsecrets
        copying dotsecrets/__init__.py -> build/lib/dotsecrets
        copying dotsecrets/main.py -> build/lib/dotsecrets
        copying dotsecrets/params.py -> build/lib/dotsecrets
        copying dotsecrets/textsub.py -> build/lib/dotsecrets
        copying dotsecrets/utils.py -> build/lib/dotsecrets
        copying dotsecrets/init.py -> build/lib/dotsecrets
        copying dotsecrets/clean.py -> build/lib/dotsecrets
        copying dotsecrets/smudge.py -> build/lib/dotsecrets
        copying dotsecrets/metadata.py -> build/lib/dotsecrets
        copying dotsecrets/test.py -> build/lib/dotsecrets
        copying dotsecrets/compat.py -> build/lib/dotsecrets
        copying dotsecrets/stow.py -> build/lib/dotsecrets
        installing to build/bdist.linux-x86_64/wheel
        running install
        running install_lib
        creating build/bdist.linux-x86_64
        creating build/bdist.linux-x86_64/wheel
        creating build/bdist.linux-x86_64/wheel/dotsecrets
        copying build/lib/dotsecrets/__init__.py -> build/bdist.linux-x86_64/wheel/dotsecrets
        copying build/lib/dotsecrets/main.py -> build/bdist.linux-x86_64/wheel/dotsecrets
        copying build/lib/dotsecrets/params.py -> build/bdist.linux-x86_64/wheel/dotsecrets
        copying build/lib/dotsecrets/textsub.py -> build/bdist.linux-x86_64/wheel/dotsecrets
        copying build/lib/dotsecrets/utils.py -> build/bdist.linux-x86_64/wheel/dotsecrets
        copying build/lib/dotsecrets/init.py -> build/bdist.linux-x86_64/wheel/dotsecrets
        copying build/lib/dotsecrets/clean.py -> build/bdist.linux-x86_64/wheel/dotsecrets
        copying build/lib/dotsecrets/smudge.py -> build/bdist.linux-x86_64/wheel/dotsecrets
        copying build/lib/dotsecrets/metadata.py -> build/bdist.linux-x86_64/wheel/dotsecrets
        copying build/lib/dotsecrets/test.py -> build/bdist.linux-x86_64/wheel/dotsecrets
        copying build/lib/dotsecrets/compat.py -> build/bdist.linux-x86_64/wheel/dotsecrets
        copying build/lib/dotsecrets/stow.py -> build/bdist.linux-x86_64/wheel/dotsecrets
        running install_egg_info
        running egg_info
        writing entry points to dotsecrets.egg-info/entry_points.txt
        writing dependency_links to dotsecrets.egg-info/dependency_links.txt
        writing top-level names to dotsecrets.egg-info/top_level.txt
        writing dotsecrets.egg-info/PKG-INFO
        writing requirements to dotsecrets.egg-info/requires.txt
        warning: Failed to find the configured license file 'L'
        warning: Failed to find the configured license file 'C'
        warning: Failed to find the configured license file 'N'
        reading manifest file 'dotsecrets.egg-info/SOURCES.txt'
        reading manifest template 'MANIFEST.in'
        writing manifest file 'dotsecrets.egg-info/SOURCES.txt'
        Copying dotsecrets.egg-info to build/bdist.linux-x86_64/wheel/dotsecrets-0.3.3-py3.5.egg-info
        running install_scripts
        adding license file "CHANGES.rst" (matched pattern "*.rst")
        adding license file "README.rst" (matched pattern "*.rst")
        adding license file "RELEASE.rst" (matched pattern "*.rst")
        adding license file "LICENSE" (matched pattern "LICENSE")
        creating build/bdist.linux-x86_64/wheel/dotsecrets-0.3.3.dist-info/WHEEL
        creating 'dist/dotsecrets-0.3.3-py3-none-any.whl' and adding 'build/bdist.linux-x86_64/wheel' to it
        adding 'dotsecrets/__init__.py'
        adding 'dotsecrets/clean.py'
        adding 'dotsecrets/compat.py'
        adding 'dotsecrets/init.py'
        adding 'dotsecrets/main.py'
        adding 'dotsecrets/metadata.py'
        adding 'dotsecrets/params.py'
        adding 'dotsecrets/smudge.py'
        adding 'dotsecrets/stow.py'
        adding 'dotsecrets/test.py'
        adding 'dotsecrets/textsub.py'
        adding 'dotsecrets/utils.py'
        adding 'dotsecrets-0.3.3.dist-info/CHANGES.rst'
        adding 'dotsecrets-0.3.3.dist-info/LICENSE'
        adding 'dotsecrets-0.3.3.dist-info/METADATA'
        adding 'dotsecrets-0.3.3.dist-info/README.rst'
        adding 'dotsecrets-0.3.3.dist-info/RELEASE.rst'
        adding 'dotsecrets-0.3.3.dist-info/WHEEL'
        adding 'dotsecrets-0.3.3.dist-info/entry_points.txt'
        adding 'dotsecrets-0.3.3.dist-info/top_level.txt'
        adding 'dotsecrets-0.3.3.dist-info/RECORD'
        removing build/bdist.linux-x86_64/wheel


8.  Upload test packages to test instance of PyPI::

        (venv) ~/src/dotsecrets$ python -m twine upload --repository testpypi dist/*
        Enter your username:
        Enter your password:
        Uploading distributions to https://test.pypi.org/legacy/
        Uploading dotsecrets-0.3.3-py3-none-any.whl
        100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 43.4k/43.4k [00:02<00:00, 16.0kB/s]
        Uploading dotsecrets-0.3.3.tar.gz
        100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 39.6k/39.6k [00:01<00:00, 35.7kB/s]
        
        View at:
        https://test.pypi.org/project/dotsecrets/0.3.3/


9.  Review the package discription on `Test PyPI <https://test.pypi.org/project/dotsecrets/>`_.

10. Create a new virtual environment and install the test package::

        (venv) ~/src/dotsecrets$ deactivate
        ~/src/dotsecrets$ cd ~/tmp
        ~/tmp$ python3 -m venv test_venv_ds
        ~/tmp$ source test_venv_ds/bin/activate
        (test_venv_ds) ~/tmp$ $ pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple dotsecrets
        Collecting dotsecrets
          Downloading https://test-files.pythonhosted.org/packages/ef/67/fe725a9cec7e5391660ec36631e61900eb2d8e67be69f8b5dad3c28b0213/dotsecrets-0.3.3-py3-none-any.whl
        Collecting dploy>=0.1.2 (from dotsecrets)
        Collecting ruamel.yaml>=0.15.100 (from dotsecrets)
          Using cached https://files.pythonhosted.org/packages/a6/92/59af3e38227b9cc14520bf1e59516d99ceca53e3b8448094248171e9432b/ruamel.yaml-0.16.10-py2.py3-none-any.whl
        Collecting ruamel.yaml.clib>=0.1.2; platform_python_implementation == "CPython" and python_version < "3.9" (from ruamel.yaml>=0.15.100->dotsecrets)
          Using cached https://files.pythonhosted.org/packages/e8/da/d7f3368dcb3ed175b5b5778362c2e7092988ff3878d23f9b717708d9a01f/ruamel.yaml.clib-0.2.0-cp35-cp35m-manylinux1_x86_64.whl
        Installing collected packages: dploy, ruamel.yaml.clib, ruamel.yaml, dotsecrets
        Successfully installed dotsecrets-0.3.3 dploy-0.1.2 ruamel.yaml-0.16.10 ruamel.yaml.clib-0.2.0
        You are using pip version 9.0.1, however version 20.1.1 is available.
        You should consider upgrading via the 'pip install --upgrade pip' command.


11. Test some of the commands on your dotfiles repository::

        (test_venv_ds) ~/dotfiles$ dotsecrets --version
        dotsecrets 0.3.3
        (test_venv_ds) ~/dotfiles$ dotsecrets init
        (test_venv_ds) ~/dotfiles$ dotsecrets test <relative name of a dotfile>
        (test_venv_ds) ~/dotfiles$ dotsecrets stow <name of toplevel folder>
        (test_venv_ds) ~/dotfiles$ dotsecrets unstow <name of toplevel folder>
        (test_venv_ds) ~/dotfiles$ deactivate


12. If something is not as expected, do not upload a new version to PyPI,
    Troubleshoot and fix issues (or ultimately revert the version back
    to development).

13. When all is as expected tag the release::

        ~/src/dotsecrets$ source venv/bin/activate
        (venv) ~/src/dotsecrets$ git tag -a "v0.3.3" -m "Tag release v0.3.2"
        (venv) ~/src/dotsecrets$ git push --tags


14. Upload the final release version to PyPI::

        (venv) ~/src/dotsecrets$ python -m twine upload dist/*
        Enter your username:
        Enter your password:
        Uploading distributions to https://pypi.org/legacy/
        Uploading dotsecrets-0.3.3-py3-none-any.whl
        100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 43.4k/43.4k [00:02<00:00, 16.0kB/s]
        Uploading dotsecrets-0.3.3.tar.gz
        100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 39.6k/39.6k [00:01<00:00, 35.7kB/s]
        
        View at:
        https://pypi.org/project/dotsecrets/0.3.3/


Starting next development cycle
-------------------------------

1.  Change the version number to start next development cycle by
    adjusting ``dotsecrets/metadata.py``. Add a fourth element to the
    version tuple. The version should follow PEP-440 [1]_ and the
    semantic versioning guidelines [2]_.

    Typically the diff would look like this::

        (venv) ~/src/dotsecrets$ git diff dotsecrets/metadata.py
        diff --git a/dotsecrets/metadata.py b/dotsecrets/metadata.py
        index e51f521..5fd31e8 100644
        --- a/dotsecrets/metadata.py
        +++ b/dotsecrets/metadata.py
        @@ -1,6 +1,6 @@
         from datetime import datetime as dt
        
         -__version_info__ = (0, 3, 3)
         +__version_info__ = (0, 3, 4, "dev0")
          __version__ = '.'.join(map(str, __version_info__))


2.  Commit the version change::

        (venv) ~/src/dotsecrets$ git commit -m "Start development v0.3.4.dev0"


References
==========

.. [1] https://www.python.org/dev/peps/pep-0440/
.. [2] https://semver.org/
