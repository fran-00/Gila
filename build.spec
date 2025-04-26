# -*- mode: python ; coding: utf-8 -*-

import os

def collect_assets(directory):
    datas = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, '.')
            datas.append((full_path, os.path.dirname(relative_path)))
    return datas

a = Analysis(
    ['cli.py'],
    pathex=[],
    binaries=[],
    datas=collect_assets('storage/assets'),
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='gila',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='storage/assets/icons/gila.ico'
)
