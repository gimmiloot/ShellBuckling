# -*- coding: utf-8 -*-
# Purpose:
#   Run the targeted mixed-weak follow-up scan around the current candidate windows.
# Typical use:
#   Use this after the broad scan when you want a narrower search near the best candidates.
# Edit parameters in:
#   src/shell_buckling/mixed_weak/boundary_matrix_targeted_scan.py

from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.mixed_weak.boundary_matrix_targeted_scan import main


if __name__ == "__main__":
    main()
