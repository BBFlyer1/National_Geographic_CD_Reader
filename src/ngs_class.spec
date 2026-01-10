# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ngs_class.py', 'util_files.py', 'util_monitors.py', 'util_mov.py', 'util_ngs.py', 'NGS_CD_Reader.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['app_class.py'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ngs_class',
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
)
