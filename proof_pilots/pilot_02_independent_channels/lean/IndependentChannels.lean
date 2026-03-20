/-
Pilot 02: abstract witness-separation logic for the mixed-weak channel split.

This file intentionally stays abstract. The shell-specific formulas live in the
CAS and markdown layers. Lean only checks the witness-based independence logic.
-/

def CannotReduceTo {alpha beta : Type} (F G : Prod alpha beta -> Int) : Prop :=
  Not (Exists fun c : Int => forall x : Prod alpha beta, F x = c * G x)

def StructurallyIndependent {alpha beta : Type} (F G : Prod alpha beta -> Int) : Prop :=
  And (CannotReduceTo F G) (CannotReduceTo G F)

theorem separating_witnesses_imply_structural_independence
    {alpha beta : Type}
    (F G : Prod alpha beta -> Int)
    (hFG : Exists fun x : Prod alpha beta => And (Not (F x = 0)) (G x = 0))
    (hGF : Exists fun y : Prod alpha beta => And (F y = 0) (Not (G y = 0))) :
    StructurallyIndependent F G := by
  apply And.intro
  case left =>
    intro hReduce
    cases hFG with
    | intro x hx =>
        cases hx with
        | intro hFx hGx =>
            cases hReduce with
            | intro c hc =>
                have hEval : F x = c * G x := hc x
                have hZero : F x = 0 := by
                  simpa [hGx] using hEval
                exact hFx hZero
  case right =>
    intro hReduce
    cases hGF with
    | intro y hy =>
        cases hy with
        | intro hFy hGy =>
            cases hReduce with
            | intro c hc =>
                have hEval : G y = c * F y := hc y
                have hZero : G y = 0 := by
                  simpa [hFy] using hEval
                exact hGy hZero

theorem vS_type_channel_independent_of_psiHchi_type_channel
    {alpha beta : Type}
    (vSChannel psiHchiChannel : Prod alpha beta -> Int)
    (hvS : Exists fun x : Prod alpha beta => And (Not (vSChannel x = 0)) (psiHchiChannel x = 0))
    (hPsi : Exists fun y : Prod alpha beta => And (vSChannel y = 0) (Not (psiHchiChannel y = 0))) :
    StructurallyIndependent vSChannel psiHchiChannel := by
  exact separating_witnesses_imply_structural_independence vSChannel psiHchiChannel hvS hPsi
