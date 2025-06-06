# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('pdf_data.py', '.'), ('Networkdata.py', '.'), ('wifi_info.py', '.'), ('csv_data.py', '.'), ('Json_data.py', '.'), ('SpyGhost_icon.ico', '.'), ('requirements.txt', '.')]
binaries = []
hiddenimports = ['reportlab', 'reportlab.lib', 'reportlab.lib.pagesizes', 'reportlab.platypus', 'reportlab.graphics', 'reportlab.graphics.charts', 'psutil', 'requests', 'wmi', 'pandas', 'PIL', 'watchdog', 'customtkinter', 'getmac']
tmp_ret = collect_all('reportlab')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['client.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='client_ghostspy_v3',
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
    icon=['SpyGhost_icon.ico'],
)
