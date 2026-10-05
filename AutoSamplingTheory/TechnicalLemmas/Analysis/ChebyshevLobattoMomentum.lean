import AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoQuadrature

/-! Absolute norm budget for the actual source momentum integrals.
This does not assume or prove individual Clenshaw-Curtis weight positivity. -/
noncomputable section
open Set MeasureTheory Polynomial
open scoped BigOperators
namespace AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoMomentum

/-- The actual compact Lebesgue supremum controls the absolute total of the
actual momentum weights. Source D1 consumes this bound in a synchronous phase
comparison; the logarithmic and individual-positivity obligations stay separate. -/
theorem momentum_absolute_sum_le {J : ℕ} (_hJ : 2 ≤ J) {h : ℝ} (hh : 0 < h) :
    let t := fun i : Fin J => h/2*(1-Real.cos ((i : ℝ)/(J-1 : ℝ)*Real.pi))
    let ell := fun j : Fin J => Lagrange.basis Finset.univ t j
    let Lambda := sSup ((fun s : ℝ => ∑ j : Fin J, |(ell j).eval s|) '' Icc 0 h)
    (∑ j : Fin J, |∫ s in 0..h, (ell j).eval s|) ≤ h*Lambda := by
  classical
  dsimp only
  let t := fun i : Fin J => h/2*(1-Real.cos ((i : ℝ)/(J-1 : ℝ)*Real.pi))
  let ell := fun j : Fin J => Lagrange.basis Finset.univ t j
  let F := fun s : ℝ => ∑ j : Fin J, |(ell j).eval s|
  let Lambda := sSup (F '' Icc 0 h)
  have hF : Continuous F := continuous_finsetSum Finset.univ
    (fun j _ => (ell j).continuous.abs)
  have hbound : BddAbove (F '' Icc 0 h) := isCompact_Icc.bddAbove_image hF.continuousOn
  calc
    _ ≤ ∑ j : Fin J, ∫ s in 0..h, |(ell j).eval s| := by
      apply Finset.sum_le_sum
      intro j _
      simpa only [Real.norm_eq_abs] using
        intervalIntegral.norm_integral_le_integral_norm (f := fun s => (ell j).eval s) hh.le
    _ = ∫ s in 0..h, F s := by
      exact (intervalIntegral.integral_finsetSum
        (fun j _ => (ell j).continuous.abs.intervalIntegrable _ _)).symm
    _ ≤ ∫ s in 0..h, Lambda := by
      apply intervalIntegral.integral_mono_on hh.le (hF.intervalIntegrable _ _)
        (continuous_const.intervalIntegrable _ _)
      intro s hs
      exact le_csSup hbound (mem_image_of_mem F hs)
    _ = h*Lambda := by simp

end AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoMomentum
