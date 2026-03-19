# -*- coding: utf-8 -*-
# Purpose:
#   Run the supporting comparison of dimensionless background fields and branch-A diagnostics.
# Typical use:
#   Use this when you want a quick supporting check of shallow vs non-shallow background behavior.
# Edit parameters in:
#   experiments/supporting/run_supporting_dimensionless_comparison.py
#   src/shell_buckling/supporting/dimensionless_background_comparison.py

from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.supporting.dimensionless_background_comparison import compare_dimensionless


def main() -> None:
    q_target = 6.0e6
    compare_dimensionless(q_target)


if __name__ == "__main__":
    main()
