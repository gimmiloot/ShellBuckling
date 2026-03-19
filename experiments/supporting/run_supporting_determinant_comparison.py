# -*- coding: utf-8 -*-
# Purpose:
#   Run the supporting determinant-based comparison between shallow and non-shallow models.
# Typical use:
#   Use this when you want a legacy/supporting comparison against the determinant route.
# Edit parameters in:
#   src/shell_buckling/supporting/determinant_criterion_comparison.py

from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.supporting.determinant_criterion_comparison import main


if __name__ == "__main__":
    main()
