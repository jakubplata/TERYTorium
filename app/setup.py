#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable
"""
Plik tworzacy aplikacje dostepna w systemie Windows
"""
includes = ['./ter.ico', './dane']
excludes = ['_gtkagg', '_tkagg']
packages = ['gui', 'teryt', 'tkinter', 'lxml']
path = []

base = None
if sys.platform == "win32":
    base = "Win32GUI"


setup(
    version='0.1',
    description=u'Program wyświetla dane z bazy teryt',
    name=u'TERYTorium',
    options = {"build_exe": {"include_files":includes,
                            "excludes":excludes,
                            "packages":packages,
                            "path":path
                            }
    },
    executables=[Executable('gui.py', base=base,
                            targetName=u'ter.exe', icon='./ter.ico')])


