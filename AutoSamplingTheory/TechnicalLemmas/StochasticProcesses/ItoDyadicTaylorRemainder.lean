import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoTaylorGridRemainder
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteTimeGrid
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicElementaryRefinement

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicTaylorRemainder

open Filter MeasureTheory Set
open scoped BigOperators NNReal
open AutoSamplingTheory.TechnicalLemmas.Analysis.CompactTaylorRemainder
open AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoTaylorGridRemainder
open FiniteTimeGrid ElementaryItoIntegral SampledElementaryApproximation DyadicElementaryRefinement

/-- The Taylor remainder limit on the regular dyadic grids used for
completed Itô integrals and quadratic variation. -/
theorem tendstoInMeasure_dyadic_sum_secondOrderRemainder
    {Ω E : Type*} [MeasurableSpace Ω] {μ : Measure Ω} [IsFiniteMeasure μ]
    [NormedAddCommGroup E] [NormedSpace ℝ E] [LocallyCompactSpace E]
    [MeasurableSpace E] [BorelSpace E] {K : Set E}
    (hK : IsCompact K) (f : E → ℝ) (hf : ∀ x ∈ K, ContDiffAt ℝ 2 f x)
    {T : ℝ≥0} (hT : 0 < T) (X : ℝ≥0 → Ω → K) (hX : ∀ t, Measurable (X t))
    (hpaths : ∀ᵐ ω ∂μ, ContinuousOn (fun t => X t ω) (Icc 0 T))
    {Q : Ω → ℝ}
    (hQV : TendstoInMeasure μ (fun n ω =>
      let times := regularGridTimes (dyadicMesh T n) (2 ^ n)
      ∑ i : Fin (2 ^ n), ‖(X (times i.succ) ω : E) - (X (times i.castSucc) ω : E)‖ ^ 2)
      atTop Q) :
    TendstoInMeasure μ (fun n ω =>
      let times := regularGridTimes (dyadicMesh T n) (2 ^ n)
      ∑ i : Fin (2 ^ n), secondOrderRemainder f (X (times i.castSucc) ω : E)
        ((X (times i.succ) ω : E) - (X (times i.castSucc) ω : E))) atTop (fun _ => 0) := by
  let times (n : ℕ) := regularGridTimes (dyadicMesh T n) (2 ^ n)
  let S := Icc (0 : ℝ≥0) T
  have : CompactSpace S := isCompact_iff_compactSpace.mp isCompact_Icc
  have htime (n : ℕ) (i : Fin (2 ^ n + 1)) : times n i ≤ T :=
    ((regularGridTimes_strictMono (dyadicMesh_pos hT n) _).monotone (Fin.le_last i)).trans_eq
      (regularDyadic_last_time T n)
  let grid (n : ℕ) (i : Fin (2 ^ n + 1)) : S := ⟨times n i, bot_le, htime n i⟩
  let Y (t : S) := X (t : ℝ≥0)
  have hY (t : S) : Measurable (Y t) := hX t
  have hYpaths : ∀ᵐ ω ∂μ, Continuous (fun t : S => Y t ω) :=
    hpaths.mono fun _ hω => hω.domRestrict
  have hmesh (δ : ℝ) (hδ : 0 < δ) : ∀ᶠ n in atTop, ∀ i : Fin (2 ^ n),
      dist (grid n i.succ) (grid n i.castSucc) < δ := by
    filter_upwards [eventually_dyadicMesh_lt T hδ] with n hn i
    change dist ((times n i.succ : ℝ≥0) : ℝ) ((times n i.castSucc : ℝ≥0) : ℝ) < δ
    have h := dyadic_activeCell_right (T := T) i
    change times n i.succ = times n i.castSucc + dyadicMesh T n at h
    rw [h, NNReal.coe_add, Real.dist_eq, add_sub_cancel_left, abs_of_nonneg (NNReal.coe_nonneg _)]
    exact hn
  exact tendstoInMeasure_sum_secondOrderRemainder_of_quadraticVariation hK f hf Y hY
    hYpaths (fun n => 2 ^ n) grid hmesh hQV

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicTaylorRemainder
