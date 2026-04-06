# -*- coding: utf-8 -*-
# Purpose:
#   Localize branch switching of the honest axisymmetric simple-support
#   background by comparing up-scan and down-scan branch indicators.

from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.supporting.axisymmetric_simple_support_branch_localization import main


if __name__ == "__main__":
    main()
