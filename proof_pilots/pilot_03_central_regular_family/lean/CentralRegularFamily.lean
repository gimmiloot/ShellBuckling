/-
Pilot 03: abstract mode-count logic for the central regular family.

This file does not formalize the shell ODE system. It only checks the abstract
logic used in the pilot:

1. if the admissible local family is characterized by exactly two free
   parameters, then the family is two-dimensional;
2. if the active regular family is uniquely parameterized by coefficients of
   two center-regular modes, then the family is two-dimensional.
-/

def TwoDimensionalFamily (X : Type) : Prop :=
  Exists fun coords : X -> Prod Int Int =>
    Exists fun decode : Prod Int Int -> X =>
      And (Function.LeftInverse decode coords) (Function.RightInverse decode coords)

theorem two_dimensional_of_two_parameter_characterization
    {X : Type}
    (coords : X -> Prod Int Int)
    (decode : Prod Int Int -> X)
    (h_left : Function.LeftInverse decode coords)
    (h_right : Function.RightInverse decode coords) :
    TwoDimensionalFamily X := by
  exact Exists.intro coords (Exists.intro decode (And.intro h_left h_right))

theorem active_regular_family_two_dimensional_of_two_center_modes
    {X : Type}
    (combine : Int -> Int -> X)
    (coords : X -> Prod Int Int)
    (h_left : (a : Int) -> (b : Int) -> coords (combine a b) = (a, b))
    (h_right : (x : X) -> combine (coords x).1 (coords x).2 = x) :
    TwoDimensionalFamily X := by
  let decode : Prod Int Int -> X := fun p => combine p.1 p.2
  have hdecode_left : Function.LeftInverse decode coords := by
    intro x
    simpa [decode] using h_right x
  have hdecode_right : Function.RightInverse decode coords := by
    intro p
    cases p with
    | mk a b =>
        simpa [decode] using h_left a b
  exact two_dimensional_of_two_parameter_characterization coords decode hdecode_left hdecode_right