# -*- coding: utf-8 -*-
# Purpose:
#   Run the dense/high-load supporting determinant-based comparison between
#   shallow and non-shallow simple-support models for n = 3,4,5, with the
#   non-shallow comparison including the tracked Branch B curve and the
#   historical Branch A -> B determinant curve.

from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.supporting.determinant_criterion_comparison_simple_support_n345_high_load import main


if __name__ == "__main__":
    main()
