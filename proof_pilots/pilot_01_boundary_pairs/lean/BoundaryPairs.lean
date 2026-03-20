/-
Pilot 01: minimal logical proof for the reduced right boundary form.

This file only formalizes the coefficient-extraction step of the mixed-weak
boundary-pair argument.
-/

theorem coeffs_zero_of_linear_form_vanishes
    (Ts S H : Int)
    (h : (usHat : Int) -> (vHat : Int) -> (psiHat : Int) -> Ts * usHat + S * vHat + H * psiHat = 0) :
    And (Ts = 0) (And (S = 0) (H = 0)) := by
  have hTs : Ts = 0 := by
    simpa using h 1 0 0
  have hS : S = 0 := by
    simpa using h 0 1 0
  have hH : H = 0 := by
    simpa using h 0 0 1
  exact And.intro hTs (And.intro hS hH)

theorem natural_bc_from_admissible_variations
    (Ts Qs S Ms H : Int)
    (h : (usHat : Int) -> (unHat : Int) -> (vHat : Int) -> (varphiHat : Int) -> (psiHat : Int) ->
      Ts * usHat + Qs * (0 * unHat) + S * vHat + Ms * (0 * varphiHat) + H * psiHat = 0) :
    And (Ts = 0) (And (S = 0) (H = 0)) := by
  have hFree : (usHat : Int) -> (vHat : Int) -> (psiHat : Int) -> Ts * usHat + S * vHat + H * psiHat = 0 := by
    intro usHat vHat psiHat
    simpa using h usHat 0 vHat 0 psiHat
  exact coeffs_zero_of_linear_form_vanishes Ts S H hFree