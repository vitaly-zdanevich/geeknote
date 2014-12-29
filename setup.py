#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys
import os
import shutil
import getpass
import codecs
import geeknote
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.bdist_egg import bdist_egg


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


class full_install(install):

    extra_options = [
        ('bash-completion-dir', None,
         "(Linux only) Set bash completion directory (default: /etc/bash_completion.d)"
        ),
        ('zsh-completion-dir', None,
         "(Linux only) Set zsh completion directory (default: /usr/local/share/zsh/site-functions)"
        )
    ]

    user_options = install.user_options + extra_options


    def initialize_extra_options(self):
        self.bash_completion_dir = '/etc/bash_completion.d'
        self.zsh_completion_dir = '/usr/local/share/zsh/site-functions'

    def initialize_options(self):
        install.initialize_options(self)
        self.initialize_extra_options()
        

    def run(self):
        if sys.platform.startswith('linux'):
            self.install_autocomplete()
        install.run(self)

    def install_autocomplete(self):
        def copy_autocomplete(src,dst):
            if os.path.exists(dst):
                shutil.copy(src,dst)
                print('copying %s -> %s' % (src,dst))


        print "installing autocomplete"
        copy_autocomplete('completion/bash_completion/_geeknote',self.bash_completion_dir)
        copy_autocomplete('completion/zsh_completion/_geeknote',self.zsh_completion_dir)


setup(
    name='geeknote',
    version=geeknote.__version__,
    license='GPL',
    author='Vitaliy Rodnenko',
    author_email='vitaliy@rodnenko.ru',
    description='Geeknote - is a command line client for Evernote, '
                'that can be use on Linux, FreeBSD and OS X.',
    long_description=read("README.md"),
    url='http://www.geeknote.me',
    packages=['geeknote'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],

    install_requires=[
        'evernote>=1.17',
        'html2text',
        'sqlalchemy',
        'markdown2',
        'beautifulsoup4',
        'thrift'
    ],

    entry_points={
        'console_scripts': [
            'geeknote = geeknote.geeknote:main',
            'gnsync = geeknote.gnsync:main'
        ]
    },
    cmdclass={
        'install': full_install,
    },
    platforms='Any',
    test_suite='tests',
    zip_safe=False,
    keywords='Evernote, console'
)

"""
import time
import os
from setuptools import setup, find_packages

# local
import config

os.system('rm -rf geeknote')

packages = ['geeknote.' + x for x in find_packages()] + ['geeknote']

# This is to properly encapsulate the library during egg generation
os.system('mkdir .geeknote && cp -pr * .geeknote/ && mv .geeknote geeknote')

setup(
    name = "geeknote",
    version = time.strftime(str(config.VERSION) + '.%Y%m%d.%H%M'),
    packages = packages,
    author = 'Vitaliy Rodnenko',
    author_email = 'vitaly@webpp.ru',
    description = 'terminal-mode geeknote client and synchronizer',
    entry_points = {
        'console_scripts': [
            'geeknote = geeknote.geeknote:main',
            'gnsync = geeknote.gnsync:main',
        ]
    }
)
"""
