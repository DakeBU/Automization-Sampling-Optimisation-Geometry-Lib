import AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoPositiveWeights

open Polynomial AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoPositiveWeights

-- The whole all-J statement uses the actual source nodes and ordinary integral.
example {J : ℕ} (hJ : 2 ≤ J) {h : ℝ} (hh : 0<h) (j : Fin J) :
    0 ≤ ∫ s in (0 : ℝ)..h,
      (Lagrange.basis Finset.univ
        (fun i : Fin J => h/2*(1-Real.cos ((i : ℝ)/(J-1 : ℝ)*Real.pi))) j).eval s :=
  nonnegative_momentum_weights hJ hh j

-- More than two nodes: both even and odd polynomial degrees, all nodes and all h>0.
example {h : ℝ} (hh : 0<h) (j : Fin 4) :
    0 ≤ ∫ s in (0 : ℝ)..h,
      (Lagrange.basis Finset.univ
        (fun i : Fin 4 => h/2*(1-Real.cos ((i : ℝ)/3*Real.pi))) j).eval s := by
  simpa only [Nat.cast_ofNat,show (4 : ℝ)-1=3 by norm_num] using nonnegative_momentum_weights (by norm_num : 2 ≤ 4) hh j

example {h : ℝ} (hh : 0<h) (j : Fin 5) :
    0 ≤ ∫ s in (0 : ℝ)..h,
      (Lagrange.basis Finset.univ
        (fun i : Fin 5 => h/2*(1-Real.cos ((i : ℝ)/4*Real.pi))) j).eval s := by
  simpa only [Nat.cast_ofNat,show (5 : ℝ)-1=4 by norm_num] using nonnegative_momentum_weights (by norm_num : 2 ≤ 5) hh j

-- The minimal J=2 rule is included without a separate supplied formula.
example {h : ℝ} (hh : 0<h) (j : Fin 2) :
    0 ≤ ∫ s in (0 : ℝ)..h,
      (Lagrange.basis Finset.univ
        (fun i : Fin 2 => h/2*(1-Real.cos ((i : ℝ)*Real.pi))) j).eval s := by
  simpa only [Nat.cast_ofNat,show (2 : ℝ)-1=1 by norm_num,div_one] using nonnegative_momentum_weights (by norm_num : 2 ≤ 2) hh j

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoPositiveWeights.nonnegative_momentum_weights
