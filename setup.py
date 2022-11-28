#!/usr/bin/env python3
"""DotSecrets setup script."""
import os

from setuptools import setup, find_packages


HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(HERE, 'CHANGES.rst'), encoding='utf-8') as f:
    CHANGES = f.read()

PACKAGES = find_packages(exclude=['tests'])

REQUIRES = [
    'ruamel.yaml>=0.15.100',
    'dploy>=0.1.2',
]

META = {}
with open(os.path.join(HERE, 'dotsecrets', 'metadata.py')) as f:
    exec(f.read(), META)


setup(name=META['PACKAGE_NAME'],
      version=META['VERSION'],
      description='DotSecrets is a tool to facilitate storing your dotfiles '
                  'in Git, including those with private information. The '
                  'private information is filtered before committing to the '
                  'repository. DotSecrets is able to symlink your dotfiles '
                  'into your home directory similar to Stow.',
      long_description='\n' + README + '\n\n' + CHANGES,
      license=META['LICENSE'],
      license_files='LICENSE',
      classifiers=[
          "License :: OSI Approved :: BSD License",
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Intended Audience :: End Users/Desktop",
          "Topic :: System :: Shells",
          "Operating System :: POSIX",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Topic :: Software Development :: Version Control",
          "Topic :: System :: Systems Administration",
          "Topic :: Utilities"
      ],
      author=META['AUTHOR'],
      author_email=META['AUTHOR_EMAIL'],
      url=META['GITHUB_URL'],
      project_urls=META['PROJECT_URLS'],
      keywords='manage dotfiles git stow secret private password',
      packages=PACKAGES,
      entry_points={
          'console_scripts': ['dotsecrets=dotsecrets.main:main'],
      },
      python_requires=">=3.5",
      install_requires=REQUIRES,
      tests_require=REQUIRES,
      test_suite="tests",
      )
