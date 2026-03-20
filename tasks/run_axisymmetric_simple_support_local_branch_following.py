# -*- coding: utf-8 -*-
# Purpose:
#   Run the separate local branch-following helper for the 6-state full-state
#   axisymmetric simple-support background in the difficult 4.32..4.34 MPa band.
# Typical use:
#   Use this when you want the dedicated stabilization path rather than the
#   baseline fixed-load / continuation report.
# Edit parameters in:
#   src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py

from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.mixed_weak.axisymmetric_simple_support_background import report_local_branch_following_main


if __name__ == "__main__":
    report_local_branch_following_main()
