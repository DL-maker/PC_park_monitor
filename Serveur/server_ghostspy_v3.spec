# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['server.py'],
    pathex=[],
    binaries=[],
    datas=[('frontend', 'frontend'), ('schema.sql', '.'), ('requirements.txt', '.')],
    hiddenimports=['flask', 'customtkinter', 'sqlite3', 'PIL', 'cryptography', 'ssl', 'cryptography.hazmat.primitives.asymmetric.rsa', 'cryptography.hazmat.primitives.serialization', 'cryptography.x509', 'cryptography.hazmat.primitives.hashes'],
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
    name='server_ghostspy_v3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['SpyGhost_icon.ico'],
)
