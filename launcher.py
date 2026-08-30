"""Entry point for running Flappy Bird, both from source and frozen with PyInstaller.

Pygame Zero loads the game module by name and injects its globals (Actor, screen,
sounds, keys, Rect, ...) into it, resolving images/ sounds/ fonts/ relative to the
game script. When frozen with PyInstaller, everything is unpacked to sys._MEIPASS;
when running from source, assets sit next to this file. Change into that directory
so both the pgzero loaders and the game's own relative paths (e.g. images/white.png)
resolve correctly.
"""

import os
import sys

base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
os.chdir(base)
if base not in sys.path:
    sys.path.insert(0, base)

import pgzero.runner

# argv[0] is ignored by the runner; argv[1] names the game script to load.
sys.argv = ["pgzrun", "flappy_bird.py"]
pgzero.runner.main()
