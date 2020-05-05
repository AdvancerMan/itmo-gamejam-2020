from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
Executable('__main__.py', base=base, targetName = 'game')
]

setup(name='Anime-Gang Bess',
version = '1.0',
description = 'A game for ITMO game jam 2020',
options = dict(build_exe = buildOptions),
executables = executables)