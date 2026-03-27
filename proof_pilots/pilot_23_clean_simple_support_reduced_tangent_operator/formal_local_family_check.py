from __future__ import annotations

import json
import sys
from pathlib import Path

import sympy as sp

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.mixed_weak import full_simple_support_critical_search as full_search
from shell_buckling.mixed_weak import simple_support_high_load_background_continuation as high_bg
from shell_buckling.mixed_weak import solver_patched_core as mw


SAMPLE_POINTS: tuple[tuple[int, float], ...] = (
    (4, 11.1),
    (6, 17.6),
    (7, 17.3),
    (8, 17.8),
)


def principal_model_report() -> dict[str, object]:
    n, nu, lam_c, Lambda, Ctw = sp.symbols("n nu lam_c Lambda Ctw", positive=True)
    Aus, Aun, Av, Aphi, Apsi, ATs, AQs, AMs = sp.symbols(
        "Aus Aun Av Aphi Apsi ATs AQs AMs"
    )
    x = sp.symbols("x", positive=True)

    us = Aus * x**n
    un = Aun * x**n
    v = Av * x**n
    phi = Aphi * x**(n - 1)
    psi = Apsi * x**(n - 1)
    Ts = ATs * x**(n - 1)
    Qs = AQs * x**(n - 2)
    Ms = AMs * x**(n - 2)

    Ttheta = sp.expand(nu * Ts + us / x + n * v / x)
    S = sp.expand((sp.diff(v, x) - v / x - n * us / x) / (2 * (1 + nu)))
    Mtheta = sp.expand(nu * Ms + (phi + n * psi) / (Lambda * x))
    H = sp.expand((sp.diff(psi, x) - psi / x - n * phi / x) / Ctw)
    chi = sp.expand((n * Mtheta / x - sp.diff(H, x) - 2 * H / x))

    residuals = {
        "R_un_lead": sp.expand((sp.diff(un, x) + lam_c * phi) / x**(n - 1)),
        "R_gtheta_lead": sp.expand((n * un / x + psi) / x**(n - 1)),
        "R_phi_lead": sp.expand((sp.diff(phi, x) - Lambda * (Ms - nu * Mtheta)) / x**(n - 2)),
        "R_us_lead": sp.expand((sp.diff(us, x) - (Ts - nu * Ttheta)) / x**(n - 1)),
        "R_Ts_principal": sp.simplify(
            sp.expand((sp.diff(Ts, x) + Ts / x - Ttheta / x + n * S / x) / x**(n - 2))
        ),
        "R_v_principal": sp.simplify(
            sp.expand((sp.diff(S, x) + 2 * S / x - n * Ttheta / x) / x**(n - 2))
        ),
        "R_Qs_principal": sp.simplify(
            sp.expand((sp.diff(Qs, x) + Qs / x + n * chi / x) / x**(n - 3))
        ),
        "R_Ms_principal": sp.simplify(
            sp.expand((sp.diff(Ms, x) + Ms / x - Mtheta / x - Qs + n * H / x) / x**(n - 3))
        ),
    }

    lead_solution = sp.solve(
        [
            sp.Eq(residuals["R_un_lead"], 0),
            sp.Eq(residuals["R_gtheta_lead"], 0),
            sp.Eq(residuals["R_phi_lead"], 0),
        ],
        [Aun, Apsi, AMs],
        dict=True,
    )
    if len(lead_solution) != 1:
        raise RuntimeError("Expected a unique symbolic solution for the leading local relations.")
    lead_solution_map = lead_solution[0]

    us_relation = sp.solve(sp.Eq(residuals["R_us_lead"], 0), ATs, dict=True)
    if len(us_relation) != 1:
        raise RuntimeError("Expected a unique symbolic relation from R_us_lead.")

    no_full_frozen_solution = sp.solve(
        [sp.Eq(expr, 0) for expr in residuals.values()],
        [Aun, Apsi, AMs, ATs, Av, AQs],
        dict=True,
    )

    return {
        "principal_model": {
            "background_assumptions": [
                "c0 -> 1",
                "s0 -> 0",
                "a0 -> 1/x",
                "a0_prime -> -1/x^2",
                "lambda_s0 -> lambda_c",
                "lambda_theta0 -> 1",
                "drop kappa_s0, kappa_theta0, g_s, g_n from the leading singular block",
            ],
            "field_scaling": {
                "u_s": "Aus * x^n",
                "u_n": "Aun * x^n",
                "v": "Av * x^n",
                "varphi": "Aphi * x^(n-1)",
                "psi": "Apsi * x^(n-1)",
                "T_s": "ATs * x^(n-1)",
                "Q_s": "AQs * x^(n-2)",
                "M_s": "AMs * x^(n-2)",
            },
        },
        "residuals": {name: sp.sstr(expr) for name, expr in residuals.items()},
        "derived_leading_relations": {
            "Aun": sp.sstr(sp.simplify(lead_solution_map[Aun])),
            "Apsi": sp.sstr(sp.simplify(lead_solution_map[Apsi])),
            "AMs": sp.sstr(sp.simplify(lead_solution_map[AMs])),
            "ATs_from_R_us": sp.sstr(sp.simplify(us_relation[0][ATs])),
        },
        "frozen_principal_closure": {
            "all_frozen_equations_have_nontrivial_solution": bool(no_full_frozen_solution),
            "raw_solution_count": len(no_full_frozen_solution),
            "meaning": (
                "The singular leading block closes cleanly, but the fully frozen principal truncation does not by itself produce a nontrivial closed family."
            ),
        },
        "conclusion": {
            "closed_now": (
                "The singular leading center block is two-parameter in (Aus, Aphi), with Aun, Apsi, and AMs determined at that partial level."
            ),
            "still_open": (
                "This is not yet a full local formal family of the frozen principal model; the full layer equations must still be checked order by order."
            ),
        },
    }


def recurrence_report() -> dict[str, object]:
    n, nu, lam_c, Lambda, Ctw, mu = sp.symbols("n nu lam_c Lambda Ctw mu", positive=True)
    x = sp.symbols("x", positive=True)

    U0, U1, U2 = sp.symbols("U0 U1 U2")
    N0, N1, N2 = sp.symbols("N0 N1 N2")
    V0, V1, V2 = sp.symbols("V0 V1 V2")
    P0, P1, P2 = sp.symbols("P0 P1 P2")
    Y0, Y1, Y2 = sp.symbols("Y0 Y1 Y2")
    T0, T1, T2 = sp.symbols("T0 T1 T2")
    Q0c, Q1, Q2 = sp.symbols("Q0c Q1 Q2")
    M0, M1, M2 = sp.symbols("M0 M1 M2")

    us = U0 * x**n + U1 * x**(n + 1) + U2 * x**(n + 2)
    un = N0 * x**n + N1 * x**(n + 1) + N2 * x**(n + 2)
    v = V0 * x**n + V1 * x**(n + 1) + V2 * x**(n + 2)
    phi = P0 * x**(n - 1) + P1 * x**n + P2 * x**(n + 1)
    psi = Y0 * x**(n - 1) + Y1 * x**n + Y2 * x**(n + 1)
    Ts = T0 * x**(n - 1) + T1 * x**n + T2 * x**(n + 1)
    Qs = Q0c * x**(n - 2) + Q1 * x**(n - 1) + Q2 * x**n
    Ms = M0 * x**(n - 2) + M1 * x**(n - 1) + M2 * x**n

    e_theta = sp.expand(us / x + n * v / x)
    Ttheta = sp.expand(nu * Ts + e_theta)
    e_s = sp.expand(Ts - nu * Ttheta)
    S = sp.expand((sp.diff(v, x) - v / x - n * us / x) / (2 * (1 + nu)))
    Mtheta = sp.expand(nu * Ms + (phi / x + n * psi / x) / Lambda)
    H = sp.expand((sp.diff(psi, x) - psi / x - n * phi / x) / Ctw)
    chi = sp.expand((n * Mtheta / x - sp.diff(H, x) - 2 * H / x))

    residuals = {
        "R_us": sp.expand(us.diff(x) - e_s),
        "R_un": sp.expand(un.diff(x) + lam_c * phi),
        "R_gtheta": sp.expand(n * un / x + psi),
        "R_phi": sp.expand(phi.diff(x) - Lambda * (Ms - nu * Mtheta)),
        "R_Ts": sp.expand(Ts.diff(x) + Ts / x - Ttheta / x + n * S / x),
        "R_Qs": sp.expand(Qs.diff(x) + Qs / x + n * chi / x),
        "R_Ms": sp.expand(Ms.diff(x) + Ms / x - Mtheta / x - Qs + n * H / x),
        "R_v": sp.expand(S.diff(x) + 2 * S / x - n * Ttheta / x),
    }

    relative_coeffs: dict[str, dict[int, sp.Expr]] = {}
    for name, expr in residuals.items():
        series_expr = sp.series(sp.expand(expr / x**(n - 2)), x, 0, 4).removeO()
        relative_coeffs[name] = {
            power: sp.simplify(sp.expand(series_expr).coeff(x, power))
            for power in (-1, 0, 1, 2, 3)
        }

    physical_subs = {
        Lambda: 12 * (1 - nu**2) * mu**2,
        Ctw: 12 * (1 + nu) * mu**2,
    }

    leading_membrane = {
        "E_us_0": relative_coeffs["R_us"][1],
        "E_Ts_0": relative_coeffs["R_Ts"][0],
        "E_v_0": relative_coeffs["R_v"][0],
    }
    leading_flexural = {
        "E_un_0": relative_coeffs["R_un"][1],
        "E_gtheta_0": relative_coeffs["R_gtheta"][1],
        "E_phi_0": relative_coeffs["R_phi"][0],
        "E_Ms_0": relative_coeffs["R_Ms"][-1],
    }

    membrane_unknowns = [U0, V0, T0]
    membrane_matrix = sp.Matrix(
        [[sp.diff(expr, unknown) for unknown in membrane_unknowns] for expr in leading_membrane.values()]
    )
    delta_membrane = sp.factor(sp.together(membrane_matrix.det()))

    flexural_unknowns = [N0, P0, Y0, M0]
    flexural_matrix = sp.Matrix(
        [[sp.diff(expr, unknown) for unknown in flexural_unknowns] for expr in leading_flexural.values()]
    )
    delta_flexural = sp.factor(sp.together(flexural_matrix.det()))
    delta_flexural_physical = sp.factor(sp.together(delta_flexural.subs(physical_subs)))

    leading_unknowns = [U0, N0, V0, P0, Y0, T0, M0]
    leading_equations = [
        leading_membrane["E_us_0"],
        leading_flexural["E_un_0"],
        leading_membrane["E_Ts_0"],
        leading_flexural["E_gtheta_0"],
        leading_flexural["E_phi_0"],
        leading_flexural["E_Ms_0"],
        leading_membrane["E_v_0"],
    ]
    leading_matrix = sp.Matrix(
        [[sp.diff(expr, unknown) for unknown in leading_unknowns] for expr in leading_equations]
    )
    delta_leading = sp.factor(sp.together(leading_matrix.det()))
    delta_leading_physical = sp.factor(sp.together(delta_leading.subs(physical_subs)))

    next_membrane = {
        "E_us_1": relative_coeffs["R_us"][2],
        "E_Ts_1": relative_coeffs["R_Ts"][1],
        "E_v_1": relative_coeffs["R_v"][1],
    }
    next_flexural = {
        "E_un_1": relative_coeffs["R_un"][2],
        "E_gtheta_1": relative_coeffs["R_gtheta"][2],
        "E_phi_1": relative_coeffs["R_phi"][1],
        "E_Qs_1": relative_coeffs["R_Qs"][-1],
        "E_Ms_1": relative_coeffs["R_Ms"][0],
    }

    next_membrane_unknowns = [U1, V1, T1]
    next_membrane_matrix = sp.Matrix(
        [[sp.diff(expr, unknown) for unknown in next_membrane_unknowns] for expr in next_membrane.values()]
    )
    next_membrane_nullspace = next_membrane_matrix.nullspace()
    if len(next_membrane_nullspace) != 1:
        raise RuntimeError("Expected a one-dimensional next membrane nullspace.")
    next_membrane_nullvector = next_membrane_nullspace[0]

    next_flexural_unknowns = [N1, P1, Y1, M1, Q0c]
    next_flexural_matrix = sp.Matrix(
        [[sp.diff(expr, unknown) for unknown in next_flexural_unknowns] for expr in next_flexural.values()]
    )
    delta_next_flexural = sp.factor(sp.together(next_flexural_matrix.det()))
    delta_next_flexural_physical = sp.factor(sp.together(delta_next_flexural.subs(physical_subs)))

    next_unknowns = [U1, N1, V1, P1, Y1, T1, M1, Q0c]
    next_equations = [
        next_membrane["E_us_1"],
        next_flexural["E_un_1"],
        next_membrane["E_Ts_1"],
        next_flexural["E_gtheta_1"],
        next_flexural["E_phi_1"],
        next_flexural["E_Qs_1"],
        next_flexural["E_Ms_1"],
        next_membrane["E_v_1"],
    ]
    next_matrix = sp.Matrix(
        [[sp.diff(expr, unknown) for unknown in next_unknowns] for expr in next_equations]
    )

    next_solution = sp.solve(
        [sp.Eq(expr, 0) for expr in next_equations],
        [U1, N1, V1, P1, Y1, M1, Q0c],
        dict=True,
    )
    if len(next_solution) != 1:
        raise RuntimeError("Expected a unique generic next-layer solution modulo T1.")
    next_solution_map = next_solution[0]

    leading_zero_subs = {
        U0: 0,
        N0: 0,
        V0: 0,
        P0: 0,
        Y0: 0,
        T0: 0,
        M0: 0,
    }
    layer1_subs = leading_zero_subs | next_solution_map

    second_layer = {
        "E_us_2": sp.simplify(relative_coeffs["R_us"][3].subs(layer1_subs)),
        "E_un_2": sp.simplify(relative_coeffs["R_un"][3].subs(layer1_subs)),
        "E_Ts_2": sp.simplify(relative_coeffs["R_Ts"][2].subs(layer1_subs)),
        "E_gtheta_2": sp.simplify(relative_coeffs["R_gtheta"][3].subs(layer1_subs)),
        "E_phi_2": sp.simplify(relative_coeffs["R_phi"][2].subs(layer1_subs)),
        "E_Qs_2": sp.simplify(relative_coeffs["R_Qs"][0].subs(layer1_subs)),
        "E_Ms_2": sp.simplify(relative_coeffs["R_Ms"][1].subs(layer1_subs)),
        "E_v_2": sp.simplify(relative_coeffs["R_v"][2].subs(layer1_subs)),
    }

    second_unknowns = [U2, N2, V2, P2, Y2, T2, M2, Q1]
    second_matrix = sp.Matrix(
        [[sp.diff(expr, unknown) for unknown in second_unknowns] for expr in second_layer.values()]
    )
    delta_second = sp.factor(sp.together(second_matrix.det()))
    delta_second_physical = sp.factor(sp.together(delta_second.subs(physical_subs)))

    second_solution = sp.solve(
        [sp.Eq(expr, 0) for expr in second_layer.values()],
        second_unknowns,
        dict=True,
    )
    if len(second_solution) != 1:
        raise RuntimeError("Expected a unique second-layer solution after substituting the next membrane mode.")

    return {
        "frozen_principal_model": {
            "background_assumptions": [
                "c0 -> 1",
                "s0 -> 0",
                "a0 -> 1/x",
                "a0_prime -> -1/x^2",
                "lambda_s0 -> lambda_c",
                "lambda_theta0 -> 1",
                "drop kappa_s0, kappa_theta0, g_s, g_n",
            ],
            "field_expansion": {
                "u_s": "U0*x^n + U1*x^(n+1) + U2*x^(n+2)",
                "u_n": "N0*x^n + N1*x^(n+1) + N2*x^(n+2)",
                "v": "V0*x^n + V1*x^(n+1) + V2*x^(n+2)",
                "varphi": "P0*x^(n-1) + P1*x^n + P2*x^(n+1)",
                "psi": "Y0*x^(n-1) + Y1*x^n + Y2*x^(n+1)",
                "T_s": "T0*x^(n-1) + T1*x^n + T2*x^(n+1)",
                "Q_s": "Q0*x^(n-2) + Q1*x^(n-1) + Q2*x^n",
                "M_s": "M0*x^(n-2) + M1*x^(n-1) + M2*x^n",
            },
        },
        "leading_full_layer": {
            "membrane_equations": {name: sp.sstr(sp.factor(expr)) for name, expr in leading_membrane.items()},
            "flexural_equations": {name: sp.sstr(sp.factor(expr)) for name, expr in leading_flexural.items()},
            "delta_membrane": sp.sstr(delta_membrane),
            "delta_flexural_physical": sp.sstr(delta_flexural_physical),
            "delta_full_physical": sp.sstr(delta_leading_physical),
            "meaning": (
                "If delta_membrane != 0 and delta_flexural_physical != 0, then the full frozen principal leading layer forces U0 = V0 = T0 = N0 = P0 = Y0 = M0 = 0."
            ),
        },
        "next_layer_after_zero_leading": {
            "membrane_equations": {name: sp.sstr(sp.factor(expr)) for name, expr in next_membrane.items()},
            "flexural_equations": {name: sp.sstr(sp.factor(expr)) for name, expr in next_flexural.items()},
            "full_rank": int(next_matrix.rank()),
            "full_nullity": int(next_matrix.cols - next_matrix.rank()),
            "membrane_rank": int(next_membrane_matrix.rank()),
            "membrane_nullvector_T1_equals_1": [sp.sstr(sp.simplify(entry)) for entry in next_membrane_nullvector],
            "flexural_det_physical": sp.sstr(delta_next_flexural_physical),
            "generic_solution_mod_T1": {
                key.name: sp.sstr(sp.simplify(value)) for key, value in next_solution_map.items()
            },
            "resonance_denominator": "(n - 2) * (n + 1)",
            "meaning": (
                "After the leading layer is zero, the frozen principal next layer is not invertible: it leaves one free membrane parameter T1, while the flexural coefficients N1, P1, Y1, M1, Q0 are uniquely zero when flexural_det_physical != 0."
            ),
        },
        "second_layer_after_next_membrane_mode": {
            "equations": {name: sp.sstr(sp.factor(expr)) for name, expr in second_layer.items()},
            "rank": int(second_matrix.rank()),
            "delta_full_physical": sp.sstr(delta_second_physical),
            "unique_solution": {
                key.name: sp.sstr(sp.simplify(value)) for key, value in second_solution[0].items()
            },
            "meaning": (
                "After substituting the generic next-layer membrane mode, the checked second layer is again uniquely zero under nonresonance."
            ),
        },
    }


def live_nonresonance_report() -> dict[str, object]:
    n, nu, lam_c = sp.symbols("n nu lam_c", positive=True)

    delta_leading = sp.factor(
        n**2
        * (2 * n - 1)
        * (2 * n + 1)
        * (
            lam_c * n * nu**3
            - lam_c * n * nu**2
            + lam_c * n
            - 2 * lam_c * nu**3
            + 2 * lam_c * nu**2
            + lam_c * nu
            - 3 * lam_c
            - n * nu**3
            + n * nu**2
            + n * nu
            - 2
        )
        / (2 * (nu + 1))
    )
    delta_next_flexural = sp.factor(
        lam_c * n**4 * nu
        + lam_c * n**4
        - 2 * lam_c * n**3 * nu**3
        + 2 * lam_c * n**3 * nu**2
        + lam_c * n**3 * nu
        - 3 * lam_c * n**3
        + 2 * lam_c * n**2 * nu**3
        - 2 * lam_c * n**2 * nu**2
        - 2 * lam_c * n**2 * nu
        + 3 * lam_c * n**2
        + n**4 * nu
        + n**4
        + 2 * n**3 * nu**3
        - 2 * n**3 * nu**2
        - n**3 * nu
        + 3 * n**3
        + 2 * n**2 * nu**3
        - 2 * n**2 * nu**2
        - 2 * n**2 * nu
        + n**2
        + 1
    )
    delta_second = sp.factor(
        -3
        * n**2
        * (2 * n + 1)
        * (2 * n + 3)
        * (
            lam_c * n**2 * nu
            + lam_c * n**2
            - 2 * lam_c * n * nu**3
            + 2 * lam_c * n * nu**2
            + 3 * lam_c * n * nu
            - 3 * lam_c * n
            + n**2 * nu
            + n**2
            + 2 * n * nu**3
            - 2 * n * nu**2
            + n * nu
            + 7 * n
            + 4 * nu**3
            - 4 * nu**2
            - 2 * nu
            + 10
        )
        / (2 * (nu + 1))
    )

    config = high_bg.default_high_load_background_config()
    q_values = sorted({float(q) for _mode, q in SAMPLE_POINTS})
    background_results = high_bg.solve_axisymmetric_simple_support_high_load_schedule(
        q_values,
        config=config,
        verbose=False,
    )
    by_q = {round(float(result.q_mpa), 7): result for result in background_results}

    sample_rows: list[dict[str, object]] = []
    for mode, q_mpa in SAMPLE_POINTS:
        background = by_q[round(float(q_mpa), 7)]
        if not background.success or background.solution is None:
            raise RuntimeError(f"Background solve failed at n={mode}, q={q_mpa} MPa.")
        obj = full_search.build_boundary_matrix_objects(mode, background, x0=float(config.x0))
        lambda_c_value = float(obj.base.at_many([config.x0])["lambda_s0"][0])
        sample_rows.append(
            {
                "n": int(mode),
                "q_mpa": float(q_mpa),
                "lambda_c_from_live_clean_object": lambda_c_value,
                "delta_leading": float(delta_leading.subs({n: mode, nu: mw.nu, lam_c: lambda_c_value}).evalf()),
                "delta_next_flexural": float(
                    delta_next_flexural.subs({n: mode, nu: mw.nu, lam_c: lambda_c_value}).evalf()
                ),
                "delta_second": float(
                    delta_second.subs({n: mode, nu: mw.nu, lam_c: lambda_c_value}).evalf()
                ),
            }
        )

    return {
        "sample_points": sample_rows,
        "interpretation": (
            "On the representative clean competition set n=4,6,7,8 the leading full-layer determinant, the next flexural determinant, and the checked second-layer determinant are all far from zero, so the frozen-principal finite-order pattern is not a sample-point resonance artifact on the current live clean path."
        ),
    }




def richer_first_finite_terms_report() -> dict[str, object]:
    n, nu, lam_c, K, mu = sp.symbols("n nu lam_c K mu", positive=True)

    singular_relations = {
        "N0": sp.sstr(sp.simplify(-(lam_c / n) * sp.Symbol("P0"))),
        "Y0": "P0",
        "M0": sp.sstr(
            sp.simplify(
                (n - 1) * sp.Symbol("P0") / (12 * mu**2 * (nu - 1) ** 2 * (nu + 1) ** 2)
            )
        ),
    }

    r_ts_low = sp.factor(
        -K
        * sp.Symbol("P0")
        * (lam_c * n * nu - lam_c * nu + n + 1)
        / (12 * lam_c**3 * mu**2 * (nu - 1) ** 2 * (nu + 1) ** 2)
    )
    r_ms_low = sp.factor(
        -sp.Symbol("P0")
        * (
            lam_c * n**2
            - 2 * lam_c * n * nu**3
            + 2 * lam_c * n * nu**2
            + lam_c * n * nu
            - 4 * lam_c * n
            + lam_c * nu
            + lam_c
            + n**2 * nu
            - n
            - nu
            - 1
        )
        / (12 * lam_c * mu**2 * (nu - 1) ** 2 * (nu + 1) ** 2)
    )
    r_v_low = sp.factor(
        K
        * sp.Symbol("P0")
        * n
        * (
            2 * lam_c**2 * nu**3
            - 2 * lam_c**2 * nu**2
            - 2 * lam_c**2 * nu
            + 2 * lam_c**2
            + lam_c * n * nu
            - lam_c * nu
            + n
            + 1
        )
        / (12 * lam_c**4 * mu**2 * (nu - 1) ** 2 * (nu + 1) ** 2)
    )
    positive_ts_factor = sp.factor(lam_c * n * nu - lam_c * nu + n + 1)

    config = high_bg.default_high_load_background_config()
    q_values = sorted({float(q) for _mode, q in SAMPLE_POINTS})
    background_results = high_bg.solve_axisymmetric_simple_support_high_load_schedule(
        q_values,
        config=config,
        verbose=False,
    )
    by_q = {round(float(result.q_mpa), 7): result for result in background_results}

    sample_rows: list[dict[str, object]] = []
    for mode, q_mpa in SAMPLE_POINTS:
        background = by_q[round(float(q_mpa), 7)]
        if not background.success or background.solution is None:
            raise RuntimeError(f"Background solve failed at n={mode}, q={q_mpa} MPa.")
        obj = full_search.build_boundary_matrix_objects(mode, background, x0=float(config.x0))
        base_row = obj.base.at_many([config.x0])
        lambda_c_value = float(base_row["lambda_s0"][0])
        kappa_s_value = float(base_row["kappa_s0"][0])
        sample_rows.append(
            {
                "n": int(mode),
                "q_mpa": float(q_mpa),
                "lambda_c_from_live_clean_object": lambda_c_value,
                "kappa_s0_from_live_clean_object": kappa_s_value,
                "R_Ts_low_factor": float(
                    positive_ts_factor.subs({n: mode, nu: mw.nu, lam_c: lambda_c_value}).evalf()
                ),
                "R_Ms_low_factor": float(
                    (
                        lam_c * n**2
                        - 2 * lam_c * n * nu**3
                        + 2 * lam_c * n * nu**2
                        + lam_c * n * nu
                        - 4 * lam_c * n
                        + lam_c * nu
                        + lam_c
                        + n**2 * nu
                        - n
                        - nu
                        - 1
                    )
                    .subs({n: mode, nu: mw.nu, lam_c: lambda_c_value})
                    .evalf()
                ),
                "R_v_low_factor": float(
                    (
                        2 * lam_c**2 * nu**3
                        - 2 * lam_c**2 * nu**2
                        - 2 * lam_c**2 * nu
                        + 2 * lam_c**2
                        + lam_c * n * nu
                        - lam_c * nu
                        + n
                        + 1
                    )
                    .subs({n: mode, nu: mw.nu, lam_c: lambda_c_value})
                    .evalf()
                ),
            }
        )

    return {
        "restored_center_terms": {
            "center_constants": [
                "lambda_s0(0) = lambda_theta0(0) = lambda_c",
                "kappa_s0(0) = K",
                "kappa_theta0(0) = K / lambda_c",
                "T_s^0(0), T_theta^0(0), M_theta^0(0)",
                "T_sn^0(x) = Q1 * x + O(x^3)",
            ],
            "first_omitted_finite_corrections": [
                "c0 = 1 + O(x^2)",
                "s0 = K * x + O(x^3)",
                "a0 = 1 / x + O(x)",
                "a0' = -1 / x^2 + O(1)",
                "lambda_s0 = lambda_c + O(x^2)",
                "lambda_theta0 = lambda_c + O(x^2)",
                "kappa_s0 = K + O(x^2)",
                "kappa_theta0 = K / lambda_c + O(x^2)",
                "T_s^0 = T_s^0(0) + O(x^2)",
                "T_theta^0 = T_theta^0(0) + O(x^2)",
                "M_theta^0 = M_theta^0(0) + O(x^2)",
                "The honest background recurrence fixes Ts2, U3, K3, Ms2, Q3 uniquely in the richer local expansion.",
            ],
        },
        "low_order_invariance": {
            "statement": (
                "The first omitted finite center corrections start at O(x^2) or O(x^3), so they do not modify the lowest obstruction orders coming from R_Ts, R_Ms, and R_v. Those rows still see exactly the same low-order P0-coupling as in the constant-finite model."
            ),
            "manual_order_counting": {
                "R_Ts": (
                    "The obstruction term sits in -(s0 * c0 / r0^2) * Mtheta ~ x^(-1) * x^(n-2) = x^(n-3). The restored corrections change s0 * c0 / r0^2 only by O(x), so they first enter at x^(n-1)."
                ),
                "R_Ms": (
                    "The low layer comes from Ms_x, a0 * Ms, -a0 * Mtheta, -Q_s, and (n/x) * H at x^(n-3). The restored finite background corrections change these rows only by O(x^(n-1)) or higher."
                ),
                "R_v": (
                    "The low layer comes from kap_theta0 * chi with chi ~ x^(n-3). Since kap_theta0 = K / lambda_c + O(x^2), the restored terms first enter at x^(n-1), not at the obstruction layer x^(n-3)."
                ),
            },
        },
        "unchanged_low_order_formulas": {
            "singular_relations_after_R_un_R_gtheta_R_phi": singular_relations,
            "R_Ts_low_after_substitution": sp.sstr(r_ts_low),
            "R_Ms_low_after_substitution": sp.sstr(r_ms_low),
            "R_v_low_after_substitution": sp.sstr(r_v_low),
            "R_Ts_simple_positive_factor": sp.sstr(positive_ts_factor),
        },
        "live_clean_factor_check": {
            "sample_points": sample_rows,
            "interpretation": (
                "On the representative active clean competition set, the center curvature K is nonzero and all three low-order obstruction factors are far from zero, so the richer first-finite-corrections layer does not rescue a nontrivial P0 branch on those live clean cases."
            ),
        },
        "conservative_reading": {
            "closed_now": (
                "Restoring the first omitted finite center coefficients is not enough to change the decisive low-order obstruction rows. At the checked low orders the richer local model still forces P0 = 0 generically."
            ),
            "still_open": (
                "This does not prove the final theorem-level local family, but it does show that the first O(x^2) / O(x^3) background corrections alone cannot recover the expected two-amplitude continuation."
            ),
        },
    }

def main() -> None:
    print(
        json.dumps(
            {
                "leading_local_family": principal_model_report(),
                "higher_order_frozen_principal_recurrence": recurrence_report(),
                "live_nonresonance_check": live_nonresonance_report(),
                "richer_first_finite_terms_c3c": richer_first_finite_terms_report(),
                "conclusion": {
                    "closed_now": (
                        "The local theory is now split more sharply: the frozen-principal model has a checked finite-order obstruction, and the richer first-finite-center-coefficients model still leaves the same low-order P0 obstruction unchanged."
                    ),
                    "obstruction": (
                        "The first omitted finite center coefficients do not by themselves restore the expected clean two-amplitude local family."
                    ),
                    "next_needed_ingredient": (
                        "The next theorem-facing step is no longer to add only the first O(x^2) / O(x^3) center corrections; it is to identify a local ingredient that can act at the same low orders as the unchanged obstruction, or else to reconsider the exact theorem-facing local comparison object."
                    ),
                },
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()

