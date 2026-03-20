# -*- coding: utf-8 -*-
# Purpose:
#   Run a compact diagnostic report for the separate full-state axisymmetric
#   simple-support background solver path.
# Typical use:
#   Use this when you want a short success/failure summary across the default
#   fixed-load and continuation schedules.
# Edit parameters in:
#   src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py

from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.mixed_weak.axisymmetric_simple_support_background import report_main


if __name__ == "__main__":
    report_main()