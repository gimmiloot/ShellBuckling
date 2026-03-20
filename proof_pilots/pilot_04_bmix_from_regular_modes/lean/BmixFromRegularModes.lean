/-
Pilot 04: abstract admissibility logic for building B_mix from regular modes.

This file does not formalize the shell system or the numerical scan code.
It only checks the abstract logic used by the pilot:

1. if a boundary object is specified to come from an admissible family, then a
   non-admissible pair cannot be the pair used to build that object;
2. if B_mix is a boundary object of the center-regular family and only the
   regular pair satisfies the active center constraints, then B_mix must be
   built from the center-regular pair rather than from the non-admissible
   surrogate pair.
-/

structure ModePair (X : Type) where
  first : X
  second : X

def PairSatisfies {X : Type} (Admissible : X -> Prop) (pair : ModePair X) : Prop :=
  Admissible pair.first /\ Admissible pair.second

theorem boundary_object_not_built_from_nonadmissible_pair
    {X Y : Type}
    (build : ModePair X -> Y)
    (Admissible : X -> Prop)
    (B : Y)
    (regularPair surrogatePair : ModePair X)
    (h_regular : PairSatisfies Admissible regularPair)
    (h_boundary_uses_admissible_pairs : (pair : ModePair X) -> build pair = B -> PairSatisfies Admissible pair)
    (h_regular_builds_B : build regularPair = B)
    (h_surrogate_not_admissible : Not (PairSatisfies Admissible surrogatePair)) :
    Not (build surrogatePair = B) := by
  let _ := h_regular
  let _ := h_regular_builds_B
  intro h_surrogate_builds_B
  have h_surrogate_admissible : PairSatisfies Admissible surrogatePair :=
    h_boundary_uses_admissible_pairs surrogatePair h_surrogate_builds_B
  exact h_surrogate_not_admissible h_surrogate_admissible

theorem bmix_from_center_regular_modes_not_from_surrogate_directions
    {X Y : Type}
    (build : ModePair X -> Y)
    (CenterRegular : X -> Prop)
    (Bmix : Y)
    (regularPair surrogatePair : ModePair X)
    (h_regular_pair : PairSatisfies CenterRegular regularPair)
    (h_Bmix_is_boundary_object_of_center_regular_family :
      (pair : ModePair X) -> build pair = Bmix -> PairSatisfies CenterRegular pair)
    (h_Bmix_built_from_regular_pair : build regularPair = Bmix)
    (h_surrogate_pair_not_center_regular : Not (PairSatisfies CenterRegular surrogatePair)) :
    Not (build surrogatePair = Bmix) := by
  exact boundary_object_not_built_from_nonadmissible_pair
    build
    CenterRegular
    Bmix
    regularPair
    surrogatePair
    h_regular_pair
    h_Bmix_is_boundary_object_of_center_regular_family
    h_Bmix_built_from_regular_pair
    h_surrogate_pair_not_center_regular