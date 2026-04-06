# -*- coding: utf-8 -*-
# Purpose:
#   Run the supporting determinant-based comparison between shallow and
#   non-shallow models for the simple-support line.
# Typical use:
#   Use this when you want the legacy/supporting determinant route, but with
#   the non-shallow prebuckling state taken from the dedicated full-state
#   simple-support background path.

from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.supporting.determinant_criterion_comparison_simple_support import main


if __name__ == "__main__":
    main()
