#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright 2010-2015 Christoph Reiter
#           2015 Nick Boultbee
#           2010 Steven Robertson
#           2007-2008 Joe Wreschnig
#
# This software and accompanying documentation, if any, may be freely
# used, distributed, and/or modified, in any form and for any purpose,
# as long as this notice is preserved. There is no warranty, either
# express or implied, for this software.

import os
import sys
import types

from gdist import GDistribution, setup


def exec_module(path):
    """Executes the Python file at `path` and returns it as the module"""

    globals_ = {}
    if sys.version_info[0] == 2:
        execfile(path, globals_)
    else:
        with open(path) as h:
            exec(h.read(), globals_)
    module = types.ModuleType("")
    module.__dict__.update(globals_)
    return module


def main():
    # distutils depends on setup.py beeing executed from the same dir.
    # Most of our custom commands work either way, but this makes
    # it work in all cases.
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    const = exec_module(os.path.join("quodlibet", "const.py"))

    # convert to a setuptools compatible version string
    version = const.VERSION_TUPLE
    if version[-1] == -1:
        version_string = ".".join(map(str, version[:-1])) + ".dev0"
    else:
        version_string = ".".join(map(str, version))

    package_path = "quodlibet"
    packages = []
    for root, dirnames, filenames in os.walk(package_path):
        if "__init__.py" in filenames:
            relpath = os.path.relpath(root, os.path.dirname(package_path))
            package_name = relpath.replace(os.sep, ".")
            packages.append(package_name)
    assert packages

    setup_kwargs = {
        'distclass': GDistribution,
        'name': "quodlibet",
        'version': version_string,
        'url': "https://quodlibet.readthedocs.org",
        'description': "a music library, tagger, and player",
        'author': "Joe Wreschnig, Michael Urman, & others",
        'author_email': "quod-libet-development@googlegroups.com",
        'maintainer': "Steven Robertson and Christoph Reiter",
        'license': "GNU GPL v2",
        'launchers': {
            "console_scripts": [
                "operon=quodlibet.operon:main",
            ],
            "gui_scripts": [
                "quodlibet=quodlibet.main:main",
                "exfalso=quodlibet.exfalso:main",
            ]
        },
        'packages': packages,
        'package_data': {
            "quodlibet": [
                "images/hicolor/*/*/*.png",
                "images/hicolor/*/*/*.svg",
            ],
        },
        'po_directory': "po",
        'po_package': "quodlibet",
        'shortcuts': ["data/quodlibet.desktop", "data/exfalso.desktop"],
        'dbus_services': [
            "data/net.sacredchao.QuodLibet.service",
            # https://github.com/quodlibet/quodlibet/issues/1268
            # "data/org.mpris.MediaPlayer2.quodlibet.service",
            # "data/org.mpris.quodlibet.service",
        ],
        'appdata': [
            "data/quodlibet.appdata.xml",
            "data/exfalso.appdata.xml",
        ],
        'man_pages': [
            "data/quodlibet.1",
            "data/exfalso.1",
            "data/operon.1",
        ],
        "search_provider": "data/quodlibet-search-provider.ini",
        "zsh_completions": [
            ("data/quodlibet.zsh", "_quodlibet"),
        ],
        "coverage_options": {
            "directory": "coverage",
        },
    }

    if os.name == "nt":
        # cli variants for gui scripts
        cs = setup_kwargs["launchers"]["console_scripts"]
        for line in setup_kwargs["launchers"]["gui_scripts"]:
            cs.append(line.replace("=", "-cmd=", 1))

    setup(**setup_kwargs)


if __name__ == "__main__":
    main()
