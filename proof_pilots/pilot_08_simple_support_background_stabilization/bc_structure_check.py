from __future__ import annotations

import inspect
import sys
from pathlib import Path

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

import shell_buckling.mixed_weak.axisymmetric_simple_support_background as ss


EXPECTED_STATE_LABELS = ("T_s", "T_sn", "M_s", "u_r", "u_z", "varphi")
EXPECTED_BC_LABELS = (
    "T_s(1)=0",
    "M_s(1)=0",
    "u_z(1)=0",
    "T_sn(x0)=0",
    "u_r(x0)=0",
    "varphi(x0)=0",
)


def pass_fail(flag: bool) -> str:
    return "PASS" if flag else "FAIL"


def main() -> None:
    ya = np.array([11.0, 22.0, 33.0, 44.0, 55.0, 66.0], dtype=float)
    yb = np.array([101.0, 102.0, 103.0, 104.0, 105.0, 106.0], dtype=float)
    got = ss.axisymmetric_simple_support_bc(ya, yb)
    expected = np.array([yb[0], yb[2], yb[4], ya[1], ya[3], ya[5]], dtype=float)

    state_ok = tuple(ss.STATE_LABELS) == EXPECTED_STATE_LABELS
    labels_ok = tuple(ss.BC_LABELS) == EXPECTED_BC_LABELS
    count_ok = len(ss.STATE_LABELS) == len(got) == 6
    mapping_ok = np.allclose(got, expected)
    center_ok = np.allclose(got[3:], np.array([ya[1], ya[3], ya[5]], dtype=float))
    edge_ok = np.allclose(got[:3], np.array([yb[0], yb[2], yb[4]], dtype=float))

    x_probe = np.linspace(ss.AxisymmetricSimpleSupportConfig().x0, 1.0, 8)
    y_probe = np.zeros((6, x_probe.size), dtype=float)
    ode_probe = ss.axisymmetric_simple_support_ode(x_probe, y_probe, q_pa=0.0)
    ode_size_ok = ode_probe.shape == (6, x_probe.size)

    source = inspect.getsource(ss.axisymmetric_simple_support_bc)
    explicit_indices = all(token in source for token in ["yb[0]", "yb[2]", "yb[4]", "ya[1]", "ya[3]", "ya[5]"])

    overall_ok = all([state_ok, labels_ok, count_ok, mapping_ok, center_ok, edge_ok, ode_size_ok, explicit_indices])

    print("=== Pilot 08: BC structure check for the 6-state simple-support background ===")
    print()
    print("Expected simple-support BC statement:")
    print("  center: T_sn(x0)=0, u_r(x0)=0, varphi(x0)=0")
    print("  edge:   T_s(1)=0, M_s(1)=0, u_z(1)=0")
    print()
    print(f"A. State labels: {pass_fail(state_ok)} -> {list(ss.STATE_LABELS)}")
    print(f"B. BC labels: {pass_fail(labels_ok)} -> {list(ss.BC_LABELS)}")
    print(f"C. BC residual count matches 6-state system: {pass_fail(count_ok)} -> {len(got)} residuals for {len(ss.STATE_LABELS)} states")
    print(f"D. Exact BC mapping check: {pass_fail(mapping_ok)} -> got {got.tolist()}")
    print(f"E. Edge residuals hit T_s, M_s, u_z: {pass_fail(edge_ok)}")
    print(f"F. Center residuals hit T_sn, u_r, varphi: {pass_fail(center_ok)}")
    print(f"G. ODE output dimension is 6 x N: {pass_fail(ode_size_ok)} -> {ode_probe.shape}")
    print(f"H. Source shows the intended variable slots explicitly: {pass_fail(explicit_indices)}")
    print()
    print(f"Overall verdict: {pass_fail(overall_ok)}")
    if overall_ok:
        print("No silent BC replacement or BC-count mismatch was detected in the active 6-state module.")
    else:
        print("The active 6-state BC implementation needs review before further stabilization work.")


if __name__ == "__main__":
    main()
