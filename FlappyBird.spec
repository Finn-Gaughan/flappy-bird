# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for Flappy Bird.
#
# The game itself (flappy_bird.py) is intentionally bundled as a *data file*,
# NOT imported or added to hiddenimports: Pygame Zero only works when it loads
# the game module itself (injecting Actor/screen/sounds/... globals), so any
# other import path would crash with "Actor is not defined". The launcher hands
# the bundled file back to pgzero's runner at runtime.
import sys

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

hiddenimports = collect_submodules("pgzero")
datas = [
    ("flappy_bird.py", "."),
    ("images", "images"),
    ("sounds", "sounds"),
    ("fonts", "fonts"),
]
datas += collect_data_files("pgzero")

a = Analysis(
    ["launcher.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="FlappyBird",
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

# macOS needs an .app bundle around the windowed executable.
if sys.platform == "darwin":
    app = BUNDLE(
        exe,
        name="FlappyBird.app",
        icon=None,
        bundle_identifier="com.finngaughan.flappybird",
    )
