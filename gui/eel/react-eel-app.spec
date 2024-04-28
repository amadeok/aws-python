# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['index.py'],
    pathex=[],
    binaries=[],
    datas=[('F:\\all\\GitHub\\aws-python\\gui\\eel\\env_eel\\lib\\site-packages\\eel\\eel.js', 'eel'), ('build', 'build')],
    hiddenimports=['bottle_websocket'],
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
    name='react-eel-app',
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
