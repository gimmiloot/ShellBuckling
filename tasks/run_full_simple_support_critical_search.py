# -*- coding: utf-8 -*-
# Purpose:
#   Run the standalone clean mixed-weak critical-load search for the full
#   simple-support task using the honest 6-state axisymmetric background.
# Typical use:
#   Use this when you want the first-pass n=2..6 simple-support critical
#   search without reusing the older hybrid F_min-backed scan path.
# Edit parameters in:
#   src/shell_buckling/mixed_weak/full_simple_support_critical_search.py

from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.mixed_weak.full_simple_support_critical_search import main


if __name__ == "__main__":
    main()
