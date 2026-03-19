# -*- coding: utf-8 -*-
# Purpose:
#   Run the broad active mixed-weak boundary-matrix scan on the simple-support branch.
# Typical use:
#   Use this first when you want the main active scan, including baseline and follow-up studies.
# Edit parameters in:
#   src/shell_buckling/mixed_weak/boundary_matrix_scan.py

from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.mixed_weak.boundary_matrix_scan import main


if __name__ == "__main__":
    main()
