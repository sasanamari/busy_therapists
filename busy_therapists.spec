# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for busy_therapists
#
# Build with:
#   conda activate busy_therapists
#   pyinstaller busy_therapists.spec

from pathlib import Path

ROOT = Path(SPECPATH)

a = Analysis(
    [str(ROOT / "main.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        # Email templates
        (str(ROOT / "templates"), "templates"),
        # src modules + bundled fonts
        (str(ROOT / "src"), "src"),
    ],
    hiddenimports=[
        "requests",
        "bs4",
        "lxml",
        "lxml.etree",
        "lxml._elementpath",
        "fpdf",
        "fpdf.fpdf",
        "scraper",
        "email_generator",
    ],
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
    [],
    exclude_binaries=True,
    name="busy_therapists",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,       # terminal window — required for interactive menu
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="busy_therapists",
)

import sys as _sys
if _sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="busy_therapists.app",
        icon=None,
        bundle_identifier=None,
    )
