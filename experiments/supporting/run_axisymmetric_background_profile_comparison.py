# -*- coding: utf-8 -*-
# Purpose:
#   Plot axisymmetric non-shallow honest simple-support background profiles for
#   a small selected load set on one tracked continuation branch.

from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.supporting.axisymmetric_background_profile_comparison import main


if __name__ == "__main__":
    main()
