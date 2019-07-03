import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()


requires = [
    'pyyaml',
    ]


setup(name='dotsecrets',
      version='0.1',
      description='Manage dot files with secrets in Git',
      long_description=README + '\n\n' + CHANGES,
      license='BSD',
      classifiers=[
        "License :: OSI Approved :: BSD License",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Shells",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Version Control",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities"
        ],
      author='Olaf Conradi',
      author_email='olaf@conradi.org',
      url='https://github.com/oohlaf/dotsecrets',
      keywords='dotfiles git secret manage private',
      packages=find_packages(),
      entry_points = {
          'console_scripts': ['dotsecrets=dotsecrets.main:main'],
      },
      install_requires=requires,
      tests_require=requires,
      test_suite="dotsecrets.tests",
      )
