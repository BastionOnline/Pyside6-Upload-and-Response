# MyApp.spec
# -*- mode: python ; coding: utf-8 -*-

import PySide6
import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files, collect_dynamic_libs

# Collect everything PySide6 needs
hiddenimports = collect_submodules("PySide6")
datas = collect_data_files("PySide6")
binaries = collect_dynamic_libs("PySide6")

# Add your app files
datas += [
    ("index.html", "."),           # put index.html in dist folder root
    ("assets/*", "assets"),        # copy assets folder
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MyApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,   # change to True if you want console logs
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MyApp'
)
