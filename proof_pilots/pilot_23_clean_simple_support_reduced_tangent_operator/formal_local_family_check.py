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


def live_center_trace_boundary_report() -> dict[str, object]:
    config = high_bg.default_high_load_background_config()
    q_values = sorted({float(q) for _n, q in SAMPLE_POINTS})
    background_results = high_bg.solve_axisymmetric_simple_support_high_load_schedule(
        q_values,
        config=config,
        verbose=False,
    )

    sample_rows: list[dict[str, object]] = []
    for result in background_results:
        if not result.success or result.solution is None:
            raise RuntimeError(f"Background solve failed at q={result.q_mpa} MPa.")
        x0 = float(config.x0)
        y0 = result.solution.sol([x0])
        u_r_x0 = float(y0[3, 0])
        base = full_search.build_full_simple_support_base_interp(result.solution, q_mpa=float(result.q_mpa))
        base_row = base.at_many([x0])
        sample_rows.append(
            {
                "q_mpa": float(result.q_mpa),
                "u_r_x0": u_r_x0,
                "T_sn_x0": float(y0[1, 0]),
                "varphi_x0": float(y0[5, 0]),
                "lambda_s0_x0": float(base_row["lambda_s0"][0]),
                "lambda_theta0_x0": float(base_row["lambda_theta0"][0]),
                "r0_over_x0": float(base_row["r"][0] / x0),
            }
        )

    return {
        "structural_reading": {
            "current_clean_background_identity": (
                "On the current truncated clean boundary, lambda_theta0(x0) = r0(x0) / x0 = 1 exactly because the honest background BC fixes u_r(x0) = 0, so r0(x0) = x0."
            ),
            "theorem_facing_use": (
                "The selected trace comparison with J_0 = C_center must therefore use the same x0-trace convention as the live clean architecture, not a different fourth-coordinate normalization."
            ),
        },
        "sample_points": sample_rows,
        "conclusion": {
            "closed_now": (
                "The live clean background path is compatible with the principal local trace convention lambda_theta0 -> 1 at the selected x0-trace layer."
            ),
            "warning": (
                "This does not yet identify a full x -> 0 intrinsic higher-order selector; it only fixes the current theorem-facing trace convention that must be compared to J_0(A_ls)."
            ),
        },
    }


def selected_trace_recovery_report() -> dict[str, object]:
    n, lam_c = sp.symbols('n lam_c', positive=True)
    U0, N0, P0, Y0 = sp.symbols('U0 N0 P0 Y0')

    e_un = n * N0 + lam_c * P0
    e_gtheta = n * N0 + Y0
    solved = sp.solve([sp.Eq(e_un, 0), sp.Eq(e_gtheta, 0)], [N0, Y0], dict=True)
    if len(solved) != 1:
        raise RuntimeError('Expected a unique symbolic trace solution for the leading local selected relations.')
    solved_map = solved[0]

    trace_vector = sp.Matrix([
        U0,
        P0,
        N0 + (lam_c / n) * P0,
        Y0 - lam_c * P0,
    ])
    trace_vector_recovered = sp.simplify(trace_vector.subs(solved_map))

    alternative_trace_vector = sp.Matrix([
        U0,
        P0,
        N0 + (lam_c / n) * P0,
        Y0 - P0,
    ])
    alternative_trace_recovered = sp.simplify(alternative_trace_vector.subs(solved_map))

    d_amp = sp.Matrix(
        [
            [1, 0],
            [0, 1],
            [0, 0],
            [0, 0],
        ]
    )
    amp_vector = sp.Matrix([U0, P0])

    return {
        "current_trace_coordinates": {
            "J_0_lead": "tau(U0, N0, P0, Y0) = [U0, P0, N0 + (lambda_c / n) P0, Y0 - lambda_c P0]",
            "D_amp": [[int(value) for value in row] for row in d_amp.tolist()],
        },
        "leading_selected_equations": {
            "E_un": sp.sstr(e_un),
            "E_gtheta": sp.sstr(e_gtheta),
        },
        "solved_relations": {
            "N0": sp.sstr(sp.simplify(solved_map[N0])),
            "Y0": sp.sstr(sp.simplify(solved_map[Y0])),
        },
        "trace_recovery": {
            "tau_after_substitution": [sp.sstr(sp.simplify(value)) for value in trace_vector_recovered],
            "d_amp_times_amplitudes": [sp.sstr(sp.simplify(value)) for value in (d_amp * amp_vector)],
            "exact_match_to_im_D_amp": bool(trace_vector_recovered == d_amp * amp_vector),
        },
        "mismatch_if_fourth_coordinate_is_changed": {
            "alternative_trace": "tau_alt(U0, N0, P0, Y0) = [U0, P0, N0 + (lambda_c / n) P0, Y0 - P0]",
            "tau_alt_after_substitution": [sp.sstr(sp.simplify(value)) for value in alternative_trace_recovered],
            "meaning": (
                "If the fourth coordinate is normalized differently, the same singular local block no longer lands exactly in im(D_amp) unless lambda_c = 1. This is why the theorem-facing comparison must keep the current J_0 coordinates fixed."
            ),
        },
        "conclusion": {
            "closed_now": (
                "At the singular leading-center-jet level and in the same trace coordinates as J_0 = C_center, the continuum/local selected trace is exactly the 2D plane im(D_amp)."
            ),
            "still_open": (
                "This does not produce a full intrinsic higher-order local selector. It closes only the leading selected trace plane and isolates the remaining gap as a higher-order / trace-reconciliation theorem."
            ),
        },
    }



def trace_normalization_reconciliation_report() -> dict[str, object]:
    n, lam_c, eta = sp.symbols('n lam_c eta', positive=True)
    U0, N0, P0, Y0 = sp.symbols('U0 N0 P0 Y0')
    U1, N1, P1, Y1 = sp.symbols('U1 N1 P1 Y1')

    delta_un = sp.simplify(N0 + (lam_c / n) * P0)
    delta_psi_eta = sp.simplify(Y0 - eta * P0)

    richer_trace_jet = sp.Matrix([
        U0,
        P0,
        delta_un,
        delta_psi_eta,
        U1,
        N1,
        P1,
        Y1,
    ])
    projection_eta_to_j0 = sp.Matrix(
        [
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, eta - lam_c, 0, 1, 0, 0, 0, 0],
        ]
    )
    j0_trace_from_richer = sp.simplify(projection_eta_to_j0 * richer_trace_jet)
    direct_j0_trace = sp.Matrix([
        U0,
        P0,
        delta_un,
        sp.simplify(Y0 - lam_c * P0),
    ])

    selected_relations = {
        N0: sp.simplify(-(lam_c / n) * P0),
        Y0: sp.simplify(lam_c * P0),
    }
    richer_selected_trace = sp.simplify(richer_trace_jet.subs(selected_relations))

    d_rich_eta = sp.Matrix(
        [
            [1, 0],
            [0, 1],
            [0, 0],
            [0, lam_c - eta],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
        ]
    )
    d_amp = sp.Matrix(
        [
            [1, 0],
            [0, 1],
            [0, 0],
            [0, 0],
        ]
    )

    config = high_bg.default_high_load_background_config()
    q_values = sorted({float(q) for _n, q in SAMPLE_POINTS})
    background_results = high_bg.solve_axisymmetric_simple_support_high_load_schedule(
        q_values,
        config=config,
        verbose=False,
    )
    sample_rows: list[dict[str, object]] = []
    for result in background_results:
        if not result.success or result.solution is None:
            raise RuntimeError(f"Background solve failed at q={result.q_mpa} MPa.")
        base = full_search.build_full_simple_support_base_interp(result.solution, q_mpa=float(result.q_mpa))
        lam_c_value = float(base.at_many([float(config.x0)])["lambda_s0"][0])
        sample_rows.append(
            {
                "q_mpa": float(result.q_mpa),
                "lambda_c_x0": lam_c_value,
                "lift_coefficient_for_eta_equals_one": float(lam_c_value - 1.0),
            }
        )

    return {
        "candidate_richer_trace_objects": {
            "smallest_leading_family": (
                "Xi_rich^(0,eta) = [U0, P0, Delta_un^(0), Delta_psi,eta^(0)] with Delta_un^(0) = N0 + (lambda_c / n) P0 and Delta_psi,eta^(0) = Y0 - eta P0."
            ),
            "best_current_candidate": (
                "Xi_rich^(1,eta) = [U0, P0, Delta_un^(0), Delta_psi,eta^(0), U1, N1, P1, Y1]. It is the smallest regular-singular jet currently supported by the checked local recurrence that already extends J_0 by one post-leading layer."
            ),
            "coordinate_dependence": (
                "The richer trace is not yet canonical: it depends on the choice of the fourth-coordinate normalization parameter eta and on how many higher center coefficients are retained."
            ),
        },
        "canonical_projection_to_j0": {
            "projection_matrix_Pi_eta_to_J0": [[sp.sstr(value) for value in row] for row in projection_eta_to_j0.tolist()],
            "projection_identity": [sp.sstr(sp.simplify(value)) for value in j0_trace_from_richer],
            "direct_J0_trace": [sp.sstr(sp.simplify(value)) for value in direct_j0_trace],
            "exact_identity": bool(j0_trace_from_richer == direct_j0_trace),
            "meaning": (
                "Any richer trace chart with fourth coordinate Y0 - eta P0 projects to the canonical J_0 trace by adding the correction (eta - lambda_c) P0 in the fourth slot and forgetting the higher coefficients."
            ),
        },
        "selected_lift_inside_richer_trace": {
            "selected_relations_in_current_live_coordinates": {
                "N0": sp.sstr(selected_relations[N0]),
                "Y0": sp.sstr(selected_relations[Y0]),
            },
            "selected_richer_trace": [sp.sstr(sp.simplify(value)) for value in richer_selected_trace],
            "D_rich_eta": [[sp.sstr(value) for value in row] for row in d_rich_eta.tolist()],
            "projection_of_D_rich_eta": [[sp.sstr(value) for value in row] for row in (projection_eta_to_j0 * d_rich_eta).tolist()],
            "D_amp": [[sp.sstr(value) for value in row] for row in d_amp.tolist()],
            "exact_projected_plane_identity": bool(sp.simplify(projection_eta_to_j0 * d_rich_eta - d_amp) == sp.zeros(4, 2)),
            "meaning": (
                "The selected object in a richer eta-normalized trace is not generally the zero-defect slice. It is the 2D lifted plane im(D_rich_eta), and its canonical projection to J_0 is exactly im(D_amp)."
            ),
        },
        "special_case_eta_equals_one": {
            "interpretation": (
                "The older richer local note corresponds to eta = 1, so its selected leading trace is the lifted plane with fourth component (lambda_c - 1) P0, not the zero fourth row in current J_0 coordinates."
            ),
            "sample_points": sample_rows,
        },
        "conclusion": {
            "closed_now": (
                "The richer local trace can now be reconciled with J_0 by an explicit triangular projection map Pi_eta_to_J0, and the invariant selected object is a 2D lifted plane whose J_0 projection is exactly im(D_amp)."
            ),
            "still_open": (
                "What remains open is a higher-order intrinsic theorem showing how the post-leading coefficients U1, N1, P1, Y1 and beyond are selected inside that lifted family."
            ),
        },
    }


def higher_order_selected_family_report() -> dict[str, object]:
    n, nu, lam_c, Lambda, Ctw, eta = sp.symbols("n nu lam_c Lambda Ctw eta", positive=True)
    U0, P0 = sp.symbols("U0 P0")
    U1, V1, T1 = sp.symbols("U1 V1 T1")
    N1, P1, Y1, M1, Q0c = sp.symbols("N1 P1 Y1 M1 Q0c")
    s_mem = sp.symbols("s_mem")

    next_equations = {
        "E_us_1": T1 * nu**2 - T1 + U1 * n + U1 * nu + U1 + V1 * n * nu,
        "E_Ts_1": -(
            -2 * T1 * n * nu
            - 2 * T1 * n
            + 2 * T1 * nu**2
            - 2 * T1
            + U1 * n**2
            + 2 * U1 * nu
            + 2 * U1
            - V1 * n**2
            + 2 * V1 * n * nu
            + 2 * V1 * n
        )
        / (2 * (nu + 1)),
        "E_v_1": -n
        * (
            2 * T1 * nu**2
            + 2 * T1 * nu
            + U1 * n
            + 2 * U1 * nu
            + 4 * U1
            + 2 * V1 * n * nu
            + V1 * n
            - 2 * V1
        )
        / (2 * (nu + 1)),
        "E_un_1": N1 * n + N1 + P1 * lam_c,
        "E_gtheta_1": N1 * n + Y1,
        "E_phi_1": Lambda * M1 * nu**2 - Lambda * M1 + P1 * n + P1 * nu + Y1 * n * nu,
        "E_Qs_1": (
            Ctw * Lambda * M1 * n**2 * nu
            + Ctw * Lambda * Q0c * n
            - Ctw * Lambda * Q0c
            + Ctw * P1 * n**2
            + Ctw * Y1 * n**3
            + Lambda * P1 * n**3
            + Lambda * P1 * n**2
            - Lambda * Y1 * n**3
            + Lambda * Y1 * n
        )
        / (Ctw * Lambda),
        "E_Ms_1": -(
            -Ctw * Lambda * M1 * n
            + Ctw * Lambda * M1 * nu
            + Ctw * Lambda * Q0c
            + Ctw * P1
            + Ctw * Y1 * n
            + Lambda * P1 * n**2
            - Lambda * Y1 * n**2
            + Lambda * Y1 * n
        )
        / (Ctw * Lambda),
    }

    selected_postleading_jacobian = sp.Matrix(list(next_equations.values())).jacobian([U0, P0])

    next_solution = sp.solve(
        [sp.Eq(expr, 0) for expr in next_equations.values()],
        [U1, V1, N1, P1, Y1, M1, Q0c],
        dict=True,
    )
    if len(next_solution) != 1:
        raise RuntimeError("Expected a unique first post-leading solution modulo T1.")
    next_solution_map = next_solution[0]

    alpha = sp.simplify(next_solution_map[U1] / T1)
    beta = sp.simplify(next_solution_map[V1] / T1)
    alpha_num, alpha_den = [sp.factor(part) for part in sp.fraction(sp.together(alpha))]
    beta_num, beta_den = [sp.factor(part) for part in sp.fraction(sp.together(beta))]
    alpha_zero_locus_in_nu = [sp.sstr(sp.simplify(value)) for value in sp.solve(sp.Eq(alpha_num, 0), nu)]
    beta_zero_locus_in_nu = [sp.sstr(sp.simplify(value)) for value in sp.solve(sp.Eq(beta_num, 0), nu)]

    projection_eta_to_j0 = sp.Matrix(
        [
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, eta - lam_c, 0, 1, 0, 0, 0, 0],
        ]
    )
    projection_aug_to_j0 = sp.Matrix.hstack(projection_eta_to_j0, sp.zeros(4, 2))

    d_rich_eta = sp.Matrix(
        [
            [1, 0],
            [0, 1],
            [0, 0],
            [0, lam_c - eta],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
        ]
    )
    d_rich_eta_corr = sp.Matrix(
        [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
            [0, lam_c - eta, 0],
            [0, 0, 1],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
    )
    d_rich_eta_aug = sp.Matrix(
        [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
            [0, lam_c - eta, 0],
            [0, 0, alpha],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, beta],
            [0, 0, 1],
        ]
    )
    d_amp = sp.Matrix(
        [
            [1, 0],
            [0, 1],
            [0, 0],
            [0, 0],
        ]
    )
    d_amp_with_zero = sp.Matrix.hstack(d_amp, sp.zeros(4, 1))

    exact_augmented_solution_subs = {
        U1: sp.simplify(alpha * s_mem),
        V1: sp.simplify(beta * s_mem),
        T1: s_mem,
        N1: 0,
        P1: 0,
        Y1: 0,
        M1: 0,
        Q0c: 0,
    }
    exact_augmented_solution_residuals = [
        sp.simplify(expr.subs(exact_augmented_solution_subs)) for expr in next_equations.values()
    ]

    config = high_bg.default_high_load_background_config()
    q_values = sorted({float(q) for _n, q in SAMPLE_POINTS})
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
                "alpha_U1_over_T1": float(alpha.subs({n: mode, nu: mw.nu}).evalf()),
                "beta_V1_over_T1": float(beta.subs({n: mode, nu: mw.nu}).evalf()),
                "lifted_fourth_component_for_eta_equals_one": float(lambda_c_value - 1.0),
            }
        )

    recurrence_summary = recurrence_report()

    return {
        "setup": {
            "current_richer_trace": (
                "Xi_rich^(1,eta) = [U0, P0, Delta_un^(0), Delta_psi,eta^(0), U1, N1, P1, Y1]."
            ),
            "raw_lifted_plane": [[sp.sstr(value) for value in row] for row in d_rich_eta.tolist()],
            "known_projection_identity": "Pi_eta_to_J0(im(D_rich,eta)) = im(D_amp).",
        },
        "first_post_leading_recurrence": {
            "equations": {name: sp.sstr(sp.factor(expr)) for name, expr in next_equations.items()},
            "jacobian_wrt_selected_leading_amplitudes": [
                [sp.sstr(value) for value in row] for row in selected_postleading_jacobian.tolist()
            ],
            "exact_independence_from_U0_P0": bool(selected_postleading_jacobian == sp.zeros(8, 2)),
            "generic_solution_mod_T1": {
                key.name: sp.sstr(sp.simplify(value)) for key, value in next_solution_map.items()
            },
            "meaning": (
                "At the first checked post-leading layer the recurrence is an exact direct product over the leading selected amplitudes (U0, P0): it does not depend on them, kills all flexural post-leading coefficients under nonresonance, and leaves one free membrane parameter T1."
            ),
        },
        "membrane_nullmode_visibility": {
            "alpha_U1_over_T1": sp.sstr(alpha),
            "beta_V1_over_T1": sp.sstr(beta),
            "alpha_zero_locus_in_nu": alpha_zero_locus_in_nu,
            "beta_zero_locus_in_nu": beta_zero_locus_in_nu,
            "physical_reading": (
                "For n > 2 and positive nu the zero loci for alpha and beta lie outside the physical regime, so the free membrane mode is visible already in the current richer jet through U1 (and in the augmented jet through both U1 and V1)."
            ),
            "sample_points": sample_rows,
        },
        "preservation_test": {
            "raw_im_D_rich_eta_preserved": False,
            "reason": (
                "The raw lifted plane im(D_rich,eta) fixes U1 = N1 = P1 = Y1 = 0, but the exact first post-leading recurrence allows a one-parameter membrane mode with U1 = alpha*T1 and V1 = beta*T1 while N1 = P1 = Y1 = 0."
            ),
            "exact_augmented_solution_residuals": [sp.sstr(value) for value in exact_augmented_solution_residuals],
        },
        "corrected_selected_object": {
            "minimal_visible_correction_in_Xi_rich^(1,eta)": (
                "Xi_sel,corr^(1,eta) = {[U0, P0, 0, (lambda_c - eta) P0, U1, 0, 0, 0]}."
            ),
            "D_rich_eta_corr": [[sp.sstr(value) for value in row] for row in d_rich_eta_corr.tolist()],
            "projection_of_D_rich_eta_corr": [
                [sp.sstr(value) for value in row] for row in (projection_eta_to_j0 * d_rich_eta_corr).tolist()
            ],
            "projected_image_is_still_im_D_amp": bool(
                sp.simplify(projection_eta_to_j0 * d_rich_eta_corr - d_amp_with_zero) == sp.zeros(4, 3)
            ),
            "faithful_augmented_jet": (
                "Xi_rich^(1+,eta) = [U0, P0, Delta_un^(0), Delta_psi,eta^(0), U1, N1, P1, Y1, V1, T1]."
            ),
            "D_rich_eta_aug": [[sp.sstr(value) for value in row] for row in d_rich_eta_aug.tolist()],
            "projection_of_D_rich_eta_aug": [
                [sp.sstr(value) for value in row] for row in (projection_aug_to_j0 * d_rich_eta_aug).tolist()
            ],
            "augmented_projection_is_im_D_amp": bool(
                sp.simplify(projection_aug_to_j0 * d_rich_eta_aug - d_amp_with_zero) == sp.zeros(4, 3)
            ),
            "meaning": (
                "The smallest corrected higher-order selected object is a one-parameter membrane thickening over the lifted 2D selected plane. Inside the current eight-coordinate richer jet it appears as a 3D plane with free U1; in a coefficient-faithful augmented jet it is the exact 3D plane spanned by the leading amplitudes and the membrane nullmode (U1, V1, T1) = T1*(alpha, beta, 1)."
            ),
        },
        "checked_next_support": {
            "second_layer_after_generic_membrane_mode": recurrence_summary["second_layer_after_next_membrane_mode"],
            "meaning": (
                "Within the same frozen-principal recurrence model, once the first membrane nullmode is admitted, the next checked layer closes uniquely to zero under the same nonresonance assumptions; no second independent post-leading direction appears at that checked order."
            ),
        },
        "conclusion": {
            "closed_now": (
                "At the first checked post-leading order the raw 2D lifted plane im(D_rich,eta) is not preserved exactly. What is preserved is its one-parameter membrane thickening, whose canonical J_0 projection remains exactly im(D_amp)."
            ),
            "still_open": (
                "This is not an all-orders theorem. It identifies only the first corrected higher-order selected object and leaves open the intrinsic higher-order rule that should select or normalize the free membrane direction."
            ),
        },
    }


def canonical_membrane_quotient_report() -> dict[str, object]:
    n, nu, lam_c, eta, ell1, ell2 = sp.symbols("n nu lam_c eta ell1 ell2", positive=True)

    alpha = sp.simplify((-n * nu - n - 2 * nu + 2) / (-n**2 + n + 2))
    beta = sp.simplify((n * nu + n + 4) / (-n**2 + n + 2))

    projection_eta_to_j0 = sp.Matrix(
        [
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, eta - lam_c, 0, 1, 0, 0, 0, 0],
        ]
    )
    projection_aug_to_j0 = sp.Matrix.hstack(projection_eta_to_j0, sp.zeros(4, 2))

    d_rich_eta_corr = sp.Matrix(
        [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
            [0, lam_c - eta, 0],
            [0, 0, 1],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
    )
    d_rich_eta_aug = sp.Matrix(
        [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
            [0, lam_c - eta, 0],
            [0, 0, alpha],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, beta],
            [0, 0, 1],
        ]
    )
    d_amp = sp.Matrix(
        [
            [1, 0],
            [0, 1],
            [0, 0],
            [0, 0],
        ]
    )
    d_amp_with_zero = sp.Matrix.hstack(d_amp, sp.zeros(4, 1))

    visible_projection_on_coefficients = sp.simplify(projection_eta_to_j0 * d_rich_eta_corr)
    augmented_projection_on_coefficients = sp.simplify(projection_aug_to_j0 * d_rich_eta_aug)

    visible_kernel_basis = sp.Matrix(visible_projection_on_coefficients).nullspace()
    augmented_kernel_basis = sp.Matrix(augmented_projection_on_coefficients).nullspace()
    if len(visible_kernel_basis) != 1 or len(augmented_kernel_basis) != 1:
        raise RuntimeError("Expected a one-dimensional membrane kernel in both corrected charts.")

    membrane_generator_visible = sp.simplify(d_rich_eta_corr * visible_kernel_basis[0])
    membrane_generator_augmented = sp.simplify(d_rich_eta_aug * augmented_kernel_basis[0])

    section_matrix = sp.Matrix(
        [
            [1, 0],
            [0, 1],
            [ell1, ell2],
        ]
    )
    visible_section = sp.simplify(d_rich_eta_corr * section_matrix)
    augmented_section = sp.simplify(d_rich_eta_aug * section_matrix)
    visible_section_projection = sp.simplify(projection_eta_to_j0 * visible_section)
    augmented_section_projection = sp.simplify(projection_aug_to_j0 * augmented_section)

    recurrence_summary = recurrence_report()

    return {
        "corrected_selected_family": {
            "visible_chart": "Xi_sel,corr^(1,eta) = im(D_rich,eta^corr) inside Xi_rich^(1,eta).",
            "augmented_chart": "Xi_sel,corr^(1+,eta) = im(D_rich,eta^aug) inside Xi_rich^(1+,eta).",
            "projection_to_J0_visible": [[sp.sstr(value) for value in row] for row in visible_projection_on_coefficients.tolist()],
            "projection_to_J0_augmented": [[sp.sstr(value) for value in row] for row in augmented_projection_on_coefficients.tolist()],
        },
        "membrane_direction": {
            "coefficient_space_kernel_basis_visible": [[sp.sstr(value)] for value in visible_kernel_basis[0].tolist()],
            "coefficient_space_kernel_basis_augmented": [[sp.sstr(value)] for value in augmented_kernel_basis[0].tolist()],
            "jet_generator_visible": [sp.sstr(value) for value in membrane_generator_visible],
            "jet_generator_augmented": [sp.sstr(value) for value in membrane_generator_augmented],
            "projection_kills_visible_generator": bool(
                sp.simplify(projection_eta_to_j0 * membrane_generator_visible) == sp.zeros(4, 1)
            ),
            "projection_kills_augmented_generator": bool(
                sp.simplify(projection_aug_to_j0 * membrane_generator_augmented) == sp.zeros(4, 1)
            ),
            "second_checked_layer_status": recurrence_summary["second_layer_after_next_membrane_mode"]["meaning"],
            "meaning": (
                "The extra membrane thickening direction lies exactly in the kernel of the canonical J_0 projection on the corrected family, and the next checked recurrence layer does not kill it."
            ),
        },
        "family_of_sections": {
            "general_section_matrix_on_coefficient_space": [[sp.sstr(value) for value in row] for row in section_matrix.tolist()],
            "visible_section_basis": [[sp.sstr(value) for value in row] for row in visible_section.tolist()],
            "augmented_section_basis": [[sp.sstr(value) for value in row] for row in augmented_section.tolist()],
            "visible_section_projection": [[sp.sstr(value) for value in row] for row in visible_section_projection.tolist()],
            "augmented_section_projection": [[sp.sstr(value) for value in row] for row in augmented_section_projection.tolist()],
            "visible_section_projects_to_D_amp": bool(
                sp.simplify(visible_section_projection - d_amp) == sp.zeros(4, 2)
            ),
            "augmented_section_projects_to_D_amp": bool(
                sp.simplify(augmented_section_projection - d_amp) == sp.zeros(4, 2)
            ),
            "meaning": (
                "There is a whole two-parameter family of 2D sections of the corrected 3D family, each projecting isomorphically to im(D_amp). Therefore the current checked local data do not single out a canonical normalized 2D section."
            ),
        },
        "theorem_facing_reading": {
            "canonical_normalization_found": False,
            "quotient_object_identified": True,
            "best_current_local_object": (
                "The corrected higher-order selected family should currently be treated canonically only modulo the membrane kernel direction, i.e. as the quotient im(D_rich,eta^corr) / span(g_mem), equivalently im(D_rich,eta^aug) / span(g_mem^aug)."
            ),
            "canonical_invariant": (
                "The quotient is canonically identified by the J_0 projection with the selected leading trace plane im(D_amp)."
            ),
            "status_of_membrane_direction": (
                "At the current checked order the membrane direction is best treated as quotient-like rather than as a proved gauge symmetry or a proved physical selected degree of freedom."
            ),
        },
        "conclusion": {
            "closed_now": (
                "C3j identifies the correct current theorem-facing local object as a quotient class of the corrected 3D selected family modulo the membrane thickening direction."
            ),
            "still_open": (
                "What remains open is an intrinsic higher-order rule that would either canonically normalize this quotient back to a distinguished 2D representative or show that the quotient itself is the final local selected object."
            ),
        },
    }


def canonical_representative_vs_quotient_report() -> dict[str, object]:
    n, nu, eta, lam_c = sp.symbols("n nu eta lam_c", positive=True)
    ell1, ell2 = sp.symbols("ell1 ell2")
    a, b, s = sp.symbols("a b s")
    g11, g12, g13, g22, g23, g33 = sp.symbols("g11 g12 g13 g22 g23 g33")

    alpha = sp.simplify((-n * nu - n - 2 * nu + 2) / (-n**2 + n + 2))
    beta = sp.simplify((n * nu + n + 4) / (-n**2 + n + 2))

    q_coeff = sp.Matrix([[1, 0, 0], [0, 1, 0]])
    zero_section = sp.Matrix([[1, 0], [0, 1], [0, 0]])
    section_matrix = sp.Matrix([[1, 0], [0, 1], [ell1, ell2]])
    quotient_preserving_chart = sp.Matrix([[1, 0, 0], [0, 1, 0], [ell1, ell2, 1]])
    transformed_zero_section = sp.simplify(quotient_preserving_chart * zero_section)

    metric = sp.Matrix(
        [
            [g11, g12, g13],
            [g12, g22, g23],
            [g13, g23, g33],
        ]
    )
    orthogonality_equation = sp.simplify((sp.Matrix([[0, 0, 1]]) * metric * sp.Matrix([a, b, s]))[0])
    metric_selected_s = sp.simplify(sp.solve(sp.Eq(orthogonality_equation, 0), s)[0])

    chart_metric = sp.simplify(quotient_preserving_chart.inv().T * quotient_preserving_chart.inv())
    chart_metric_selected_s = sp.simplify(
        sp.solve(
            sp.Eq((sp.Matrix([[0, 0, 1]]) * chart_metric * sp.Matrix([a, b, s]))[0], 0),
            s,
        )[0]
    )

    c3i_report = higher_order_selected_family_report()
    c3j_report = canonical_membrane_quotient_report()

    return {
        "objects_under_test": {
            "corrected_selected_family": c3j_report["theorem_facing_reading"]["best_current_local_object"],
            "membrane_kernel_generator_visible": c3j_report["membrane_direction"]["jet_generator_visible"],
            "quotient_map_on_coefficients": [[sp.sstr(value) for value in row] for row in q_coeff.tolist()],
        },
        "candidate_selection_rules": {
            "next_checked_local_compatibility": {
                "result": "does_not_select",
                "evidence": c3i_report["checked_next_support"]["meaning"],
                "meaning": (
                    "The next checked recurrence layer does not distinguish representatives inside the membrane-thickened family."
                ),
            },
            "checked_local_residual_minimization": {
                "result": "does_not_select",
                "evidence": c3i_report["preservation_test"]["exact_augmented_solution_residuals"],
                "meaning": (
                    "Inside the coefficient-faithful corrected family the checked residual is exactly zero along the membrane direction, so minimal residual does not select a unique representative."
                ),
            },
            "chart_zero_membrane_coordinate": {
                "quotient_preserving_chart_change": [[sp.sstr(value) for value in row] for row in quotient_preserving_chart.tolist()],
                "q_times_chart": [[sp.sstr(value) for value in row] for row in (q_coeff * quotient_preserving_chart).tolist()],
                "transformed_zero_section": [[sp.sstr(value) for value in row] for row in transformed_zero_section.tolist()],
                "arbitrary_section": [[sp.sstr(value) for value in row] for row in section_matrix.tolist()],
                "exact_identity": bool(sp.simplify(transformed_zero_section - section_matrix) == sp.zeros(3, 2)),
                "result": "chart_dependent",
                "meaning": (
                    "Setting the membrane coordinate to zero is not canonical: after any quotient-preserving chart change it becomes an arbitrary 2D section of the corrected 3D family."
                ),
            },
            "metric_orthogonality_or_minimal_norm": {
                "general_metric": [[sp.sstr(value) for value in row] for row in metric.tolist()],
                "orthogonality_equation": sp.sstr(orthogonality_equation),
                "selected_s_for_general_metric": sp.sstr(metric_selected_s),
                "chart_induced_metric_from_euclidean": [[sp.sstr(value) for value in row] for row in chart_metric.tolist()],
                "selected_s_for_chart_induced_metric": sp.sstr(chart_metric_selected_s),
                "result": "metric_dependent",
                "meaning": (
                    "Any chosen SPD metric gives a unique section by orthogonality to the membrane line, but the selected section depends on the metric. In particular, Euclidean minimal norm in a quotient-preserving shifted chart produces an arbitrary section s = ell1*a + ell2*b."
                ),
            },
            "import_global_kkt_metric": {
                "result": "extrinsic_not_local",
                "meaning": (
                    "A global H-based selector exists on the weighted-trial KKT side, but on the current checked local boundary no intrinsic local metric has been derived that would canonically reproduce a representative of each quotient class."
                ),
            },
        },
        "strongest_current_theorem": {
            "canonical_representative_found": False,
            "quotient_is_best_current_object": True,
            "final_current_reading": (
                "At the current checked local boundary the quotient object, not a canonically normalized representative, is the strongest justified theorem-facing local selected object."
            ),
            "equivalent_representatives_statement": (
                "All representatives of a quotient class have the same canonical selected leading trace plane because the membrane kernel direction is invisible to J_0."
            ),
        },
        "conclusion": {
            "closed_now": (
                "C3k does not find an intrinsic canonical higher-order representative on the current checked boundary. It strengthens the quotient theorem: the membrane-thickened corrected family should currently be treated only modulo its membrane kernel direction."
            ),
            "still_open": (
                "What remains open is either an intrinsic higher-order selector that canonically chooses one representative per quotient class, or a theorem that the quotient object itself is the final local selected object."
            ),
        },
    }


def final_boundary_fork_decision_report() -> dict[str, object]:
    q_coeff = sp.Matrix([[1, 0, 0], [0, 1, 0]])
    d_amp = sp.Matrix(
        [
            [1, 0],
            [0, 1],
            [0, 0],
            [0, 0],
        ]
    )
    d_amp_with_zero = sp.Matrix.hstack(d_amp, sp.zeros(4, 1))

    c3i_report = higher_order_selected_family_report()
    c3j_report = canonical_membrane_quotient_report()
    c3k_report = canonical_representative_vs_quotient_report()

    j0_factorization_matrix = sp.simplify(d_amp * q_coeff)
    zero_two = sp.zeros(2, 3)

    return {
        "fork_under_decision": {
            "corrected_local_selected_family": c3j_report["theorem_facing_reading"]["best_current_local_object"],
            "membrane_direction": c3j_report["theorem_facing_reading"]["status_of_membrane_direction"],
            "quotient_map_on_coefficients": [[sp.sstr(value) for value in row] for row in q_coeff.tolist()],
            "what_counts_as_intrinsic_selector": (
                "A local rule intrinsic to the currently checked recurrence/trace structure that chooses a unique representative in each membrane-quotient class without importing an extra chart or metric choice."
            ),
            "what_counts_as_final_quotient_theorem": (
                "A boundary-scoped statement that every currently justified local selected invariant factors through the membrane quotient and no checked local condition distinguishes representatives inside one quotient class."
            ),
        },
        "factorization_of_currently_justified_invariants": {
            "canonical_J0_trace": {
                "factor_map": [[sp.sstr(value) for value in row] for row in d_amp.tolist()],
                "quotient_then_trace": [[sp.sstr(value) for value in row] for row in j0_factorization_matrix.tolist()],
                "expected_projection_on_corrected_family": [[sp.sstr(value) for value in row] for row in d_amp_with_zero.tolist()],
                "exact_factorization": bool(sp.simplify(j0_factorization_matrix - d_amp_with_zero) == sp.zeros(4, 3)),
                "meaning": (
                    "On the corrected 3D family the canonical J_0 trace is exactly D_amp composed with the quotient map (a, b, s) -> (a, b)."
                ),
            },
            "checked_local_residual": {
                "restricted_residual": c3i_report["preservation_test"]["exact_augmented_solution_residuals"],
                "factors_through_quotient": all(value == '0' for value in c3i_report["preservation_test"]["exact_augmented_solution_residuals"]),
                "meaning": (
                    "The checked local residual vanishes identically on the coefficient-faithful corrected family, so it cannot distinguish representatives and factors trivially through the quotient by the zero map."
                ),
            },
            "next_checked_local_compatibility": {
                "evidence": c3i_report["checked_next_support"]["second_layer_after_generic_membrane_mode"],
                "factors_through_quotient": True,
                "meaning": (
                    "The next checked compatibility layer still does not distinguish representatives inside a membrane-quotient class; on the current checked boundary it contributes no invariant beyond the quotient coordinates."
                ),
            },
        },
        "selector_decision": {
            "strongest_plausible_candidates": c3k_report["candidate_selection_rules"],
            "intrinsic_selector_found": False,
            "meaning": (
                "None of the strongest plausible selectors checked on the current boundary gives an intrinsic canonical representative: they either do not select, are chart-dependent, are metric-dependent, or remain extrinsic to the local theory."
            ),
        },
        "outcome": {
            "choice": "Outcome B",
            "label": "final quotient theorem justified on current checked boundary",
            "theorem": (
                "On the current checked local boundary for the clean full simple-support problem, the membrane quotient im(D_rich,eta^corr) / span(g_mem) is the final local theorem-facing selected object: every currently justified local selected invariant factors through this quotient, no checked local condition distinguishes representatives inside one quotient class, and any canonical comparison to the already closed global selected trace must therefore pass through this quotient object."
            ),
            "verification_boundary": (
                "This is a boundary-scoped finality statement. It does not claim that no future unchecked higher-order intrinsic selector could ever appear; it claims that none is currently justified on the checked local boundary."
            ),
        },
        "conclusion": {
            "closed_now": (
                "The A/B/C fork is now closed as Outcome B on the current checked boundary: the quotient object should be treated as the final local theorem-facing selected object at this boundary."
            ),
            "next_project_step": (
                "Future work should either lift this boundary-scoped quotient theorem to a stronger higher-order theorem, or derive a genuinely new intrinsic selector beyond the current checked local boundary; it should not continue blind searches for a 2D representative within the already checked data."
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
                "live_center_trace_boundary_c3g": live_center_trace_boundary_report(),
                "selected_trace_recovery_c3g": selected_trace_recovery_report(),
                "trace_normalization_reconciliation_c3h": trace_normalization_reconciliation_report(),
                "higher_order_preservation_c3i": higher_order_selected_family_report(),
                "canonical_membrane_quotient_c3j": canonical_membrane_quotient_report(),
                "canonical_representative_vs_quotient_c3k": canonical_representative_vs_quotient_report(),
                "final_boundary_fork_decision": final_boundary_fork_decision_report(),
                "conclusion": {
                    "closed_now": (
                        "The local theory is now split more sharply: the richer first-finite-center-coefficients model still leaves its low-order P0 obstruction unresolved, the singular local compatibility block expressed in the current J_0 coordinates recovers the selected 2D trace plane im(D_amp), the richer eta-normalized trace charts are reconciled with J_0 by an explicit projection map, the first checked post-leading recurrence preserves that selected trace only through a corrected one-parameter membrane thickening of the lifted family, the current canonical local object is identified only modulo that membrane direction, and no intrinsic canonical higher-order representative is yet justified on the checked boundary."
                    ),
                    "selected_trace_theorem": (
                        "At the current theorem-facing leading-center-jet layer, the continuum/local selected trace equals im(D_amp) when written in the same trace coordinates as C_center."
                    ),
                    "remaining_gap": (
                        "The exact remaining gap is now sharper: either derive an intrinsic higher-order rule that canonically selects one representative of each membrane-quotient class, or prove that the quotient object itself is already the final theorem-facing local selected object."
                    ),
                },
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()

