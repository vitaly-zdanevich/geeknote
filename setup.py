#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import shutil
import codecs
from setuptools import setup
from setuptools.command.install import install
import traceback


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


class full_install(install):

    user_options = install.user_options + [
        (
            "bash-completion-dir=",
            None,
            "(Linux only) Set bash completion directory (default: /etc/bash_completion.d)",
        ),
        (
            "zsh-completion-dir=",
            None,
            "(Linux only) Set zsh completion directory (default: /usr/local/share/zsh/site-functions)",
        ),
    ]

    def initialize_options(self):
        install.initialize_options(self)
        self.bash_completion_dir = "/etc/bash_completion.d"
        self.zsh_completion_dir = "/usr/local/share/zsh/site-functions"

    def run(self):
        if sys.platform.startswith("linux"):
            self.install_autocomplete()
        install.run(self)

    def install_autocomplete(self):
        def copy_autocomplete(src, dst):
            try:
                if os.path.exists(dst):
                    shutil.copy(src, dst)
                    print("copying %s -> %s" % (src, dst))
            except IOError:
                print(
                    "cannot copy autocomplete script %s to %s, got root ?" % (src, dst)
                )
                print(traceback.format_exc())

        print("installing autocomplete")
        # TODO fix autocomplete
        # copy_autocomplete(
        #     "completion/bash_completion/_geeknote", self.bash_completion_dir
        # )
        # copy_autocomplete(
        #     "completion/zsh_completion/_geeknote", self.zsh_completion_dir
        # )


with open("geeknote/__init__.py") as f:
    exec (f.read())  # read __version__

setup(
    name="geeknote",
    version=__version__,
    license="GPL",
    author="Vitaly Zdanevich",
    # author_email='',
    description="Geeknote - is a command line client for Evernote, "
    "that can be used on Linux, FreeBSD and OS X.",
    long_description=read("README.md"),
    url="http://github.com/vitaly-zdanevich/geeknote",
    packages=["geeknote"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
    install_requires=[
        "evernote2",
        "html2text",
        "sqlalchemy",
        "markdown2",
        "beautifulsoup4",
        "thrift",
        "proxyenv",
        "lxml",
    ],
    setup_requires=["pytest-runner"],
    entry_points={
        "console_scripts": [
            "geeknote = geeknote.geeknote:main",
            "gnsync = geeknote.gnsync:main",
        ]
    },
    cmdclass={"install": full_install},
    platforms="Any",
    zip_safe=True,
    keywords="Evernote, console",
)
