import AutoSamplingTheory.TechnicalLemmas.Analysis.CompactTaylorRemainder
import Mathlib.MeasureTheory.Function.ConvergenceInMeasure
import Mathlib.MeasureTheory.Constructions.BorelSpace.Basic

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoTaylorGridRemainder

open Filter MeasureTheory Metric
open scoped BigOperators Topology
open AutoSamplingTheory.TechnicalLemmas.Analysis.CompactTaylorRemainder

/-- On grids of vanishing mesh, the sum of Taylor remainders of a
continuous compact-state path tends to zero in measure when its sums of
squared increments converge in measure to a real-valued limit. -/
theorem tendstoInMeasure_sum_secondOrderRemainder_of_quadraticVariation
    {Ω E T : Type*} [MeasurableSpace Ω] {μ : Measure Ω} [IsFiniteMeasure μ]
    [NormedAddCommGroup E] [NormedSpace ℝ E] [LocallyCompactSpace E]
    [MeasurableSpace E] [BorelSpace E] [PseudoMetricSpace T] [CompactSpace T]
    {K : Set E} (hK : IsCompact K) (f : E → ℝ) (hf : ∀ x ∈ K, ContDiffAt ℝ 2 f x)
    (X : T → Ω → K) (hX : ∀ t, Measurable (X t))
    (hpaths : ∀ᵐ ω ∂μ, Continuous (fun t => X t ω))
    (N : ℕ → ℕ) (grid : ∀ n, Fin (N n + 1) → T)
    (hmesh : ∀ δ > 0, ∀ᶠ n in atTop, ∀ i : Fin (N n),
      dist (grid n i.succ) (grid n i.castSucc) < δ)
    {Q : Ω → ℝ}
    (hQV : TendstoInMeasure μ (fun n ω => ∑ i : Fin (N n),
      ‖(X (grid n i.succ) ω : E) - (X (grid n i.castSucc) ω : E)‖ ^ 2) atTop Q) :
    TendstoInMeasure μ (fun n ω => ∑ i : Fin (N n),
      secondOrderRemainder f (X (grid n i.castSucc) ω : E)
        ((X (grid n i.succ) ω : E) - (X (grid n i.castSucc) ω : E))) atTop (fun _ => 0) := by
  have : CompactSpace K := isCompact_iff_compactSpace.mp hK
  let Δ (n : ℕ) (i : Fin (N n)) (ω : Ω) :=
    (X (grid n i.succ) ω : E) - (X (grid n i.castSucc) ω : E)
  let A (n : ℕ) (ω : Ω) := ∑ i : Fin (N n), ‖Δ n i ω‖ ^ 2
  let R (n : ℕ) (ω : Ω) := ∑ i : Fin (N n),
    secondOrderRemainder f (X (grid n i.castSucc) ω : E) (Δ n i ω)
  change TendstoInMeasure μ R atTop (fun _ => 0)
  have hA : TendstoInMeasure μ A atTop Q := hQV
  have hfK : Continuous (fun x : K => f (x : E)) := continuous_iff_continuousAt.2 fun x =>
    (hf x x.property).continuousAt.comp continuous_subtype_val.continuousAt
  have hdK : Continuous (fun x : K => fderiv ℝ f (x : E)) :=
    continuous_iff_continuousAt.2 fun x =>
      ((hf x x.property).continuousAt_fderiv (by norm_num)).comp continuous_subtype_val.continuousAt
  have hHK : Continuous (fun x : K => fderiv ℝ (fderiv ℝ f) (x : E)) :=
    continuous_iff_continuousAt.2 fun x =>
      (((hf x x.property).fderiv_right (m := 1) (by norm_num)).continuousAt_fderiv one_ne_zero).comp
        continuous_subtype_val.continuousAt
  have hdif : Continuous (fun z : K × K => (z.2 : E) - (z.1 : E)) :=
    (continuous_subtype_val.comp continuous_snd).sub (continuous_subtype_val.comp continuous_fst)
  have hR : Continuous (fun z : K × K =>
      secondOrderRemainder f (z.1 : E) ((z.2 : E) - (z.1 : E))) := by
    have h := (((hfK.comp continuous_snd).sub (hfK.comp continuous_fst)).sub
      ((hdK.comp continuous_fst).clm_apply hdif)).sub
        ((continuous_const (y := (1 / 2 : ℝ))).smul
          (((hHK.comp continuous_fst).clm_apply hdif).clm_apply hdif))
    apply h.congr
    intro z
    simp [secondOrderRemainder, Function.comp_def, add_sub_cancel]
  have hRm (n : ℕ) : AEStronglyMeasurable (R n) μ := by
    have h (i : Fin (N n)) : AEStronglyMeasurable
        (fun ω => secondOrderRemainder f (X (grid n i.castSucc) ω : E) (Δ n i ω)) μ :=
      (hR.measurable.comp ((hX (grid n i.castSucc)).prodMk (hX (grid n i.succ)))).aestronglyMeasurable
    apply (Finset.aestronglyMeasurable_sum Finset.univ (fun i _ => h i)).congr
    exact Eventually.of_forall fun ω => by simp only [R, Finset.sum_apply]
  apply (exists_seq_tendstoInMeasure_atTop_iff hRm).2
  intro ns hns
  obtain ⟨ks, hks, hPathEnergy⟩ := (hA.comp hns.tendsto_atTop).exists_seq_tendsto_ae
  refine ⟨ks, hks, ?_⟩
  filter_upwards [hpaths, hPathEnergy] with ω hpath hEnergy
  let C := |Q ω| + 1
  have hC : 0 < C := by dsimp [C]; positivity
  have hQC : Q ω < C := by dsimp [C]; linarith [le_abs_self (Q ω)]
  have hBound : ∀ᶠ n in atTop, A (ns (ks n)) ω ≤ C :=
    ((tendsto_order.1 hEnergy).2 C hQC).mono fun _ hn => hn.le
  rw [Metric.tendsto_nhds]
  intro ε hε
  let a := ε / (2 * C)
  have ha : 0 < a := div_pos hε (mul_pos (by norm_num) hC)
  obtain ⟨r, hr, hRbound⟩ := exists_uniform_secondOrderRemainder_le_on_compact hK hf ha
  obtain ⟨δ, hδ, hclose⟩ := Metric.uniformContinuous_iff.1
    (CompactSpace.uniformContinuous_of_continuous hpath) r hr
  have hmesh' := (hns.comp hks).tendsto_atTop.eventually (hmesh δ hδ)
  filter_upwards [hBound, hmesh'] with n hnBound hnMesh
  let m := ns (ks n)
  have hstep (i : Fin (N m)) : ‖Δ m i ω‖ < r := by
    have h := hclose (hnMesh i)
    change dist (X (grid m i.succ) ω : E) (X (grid m i.castSucc) ω : E) < r at h
    simpa only [dist_eq_norm, Δ] using h
  change dist (R m ω) (0 : ℝ) < ε
  rw [dist_zero_right]
  calc
    ‖R m ω‖ ≤ ∑ i : Fin (N m),
        ‖secondOrderRemainder f (X (grid m i.castSucc) ω : E) (Δ m i ω)‖ :=
      norm_sum_le _ _
    _ ≤ a * A m ω := by
      change _ ≤ a * ∑ i : Fin (N m), ‖Δ m i ω‖ ^ 2
      rw [Finset.mul_sum]
      exact Finset.sum_le_sum fun i _ =>
        hRbound (X (grid m i.castSucc) ω : E) (X (grid m i.castSucc) ω).property _ (hstep i)
    _ ≤ a * C := mul_le_mul_of_nonneg_left hnBound ha.le
    _ < ε := by
      have h : a * C = ε / 2 := by dsimp [a]; field_simp [hC.ne']
      rw [h]
      exact half_lt_self hε

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoTaylorGridRemainder
