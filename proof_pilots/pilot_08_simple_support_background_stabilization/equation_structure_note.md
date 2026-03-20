# Equation-Structure Note for Pilot 08

Pilot 08 does not produce a proof that the active 6-state simple-support
equations are the final correct shell equations. That remains outside the
verification boundary.

What the pilot does isolate is narrower and more concrete.

1. The active 6-state module uses the same repository-level equation block
   as the supporting `axisym_nepol(...)` path it was extracted from.
2. The implemented BC set is structurally square and matches the intended
   simple-support statement exactly.
3. Near the present ceiling, failure is accompanied by aggressive mesh
   concentration near the right edge `x approx 1`, while BC residuals stay
   tiny.
4. Modest tuning of tolerance and `max_nodes` pushes the reachable load
   upward, which is evidence for a mainly numerical / stiffness-limited
   bottleneck rather than a clean BC inconsistency.

The remaining equation-level suspicion is therefore weak and specific:
there may still be a strong right-edge stiffness / boundary-layer effect
in the current 6-state equations that the present continuation strategy is
not handling well. That is not the same thing as having detected a wrong
equation or a missing BC.
