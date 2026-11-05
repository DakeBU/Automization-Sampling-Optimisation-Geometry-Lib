import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.RadialCalculus
import Mathlib.Analysis.Calculus.LocalExtr.Basic
import Mathlib.Analysis.Calculus.Deriv.Slope
import Mathlib.Analysis.Normed.Module.Ball.Pointwise
import Mathlib.Analysis.SpecialFunctions.SmoothTransition
import Mathlib.MeasureTheory.Constructions.HaarToSphere
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

/-!
Explicit ball-flux formula with the literal polar sphere measure. Local C1
regularity, both integrabilities and the radius factor are handled internally.
The proof uses the existing compact-field whole-space divergence theorem,
polar decomposition and a smooth shell limit. This is an ASTIS library
specification, not the full smooth-domain geometric divergence theorem.
-/

open MeasureTheory Metric Set Filter
open scoped Topology RealInnerProductSpace

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.BallFlux

set_option autoImplicit false
noncomputable section

private theorem local_c1_extension {n : ℕ}
    (F : EuclideanSpace ℝ (Fin n) → EuclideanSpace ℝ (Fin n))
    (a : EuclideanSpace ℝ (Fin n)) (R : ℝ) (hR : 0 < R)
    (hF : ∀ x ∈ closedBall a R, ContDiffAt ℝ 1 F x) :
    ∃ G : EuclideanSpace ℝ (Fin n) → EuclideanSpace ℝ (Fin n),
      ContDiff ℝ 1 G ∧ HasCompactSupport G ∧
      ∀ x ∈ closedBall a R, G =ᶠ[𝓝 x] F := by
  let U : Set (EuclideanSpace ℝ (Fin n)) := {x | ContDiffAt ℝ 1 F x}
  have hU : IsOpen U := isOpen_iff_mem_nhds.mpr fun x hx =>
    (show ContDiffAt ℝ 1 F x from hx).eventually (by norm_num)
  obtain ⟨δ, hδ, hδU⟩ :=
    (isCompact_closedBall a R).exists_cthickening_subset_open hU hF
  have hgood : ∀ x ∈ closedBall a (δ + R), ContDiffAt ℝ 1 F x := by
    simpa only [cthickening_closedBall hδ.le hR.le a, U, Set.subset_def,
      Set.mem_ofPred_eq] using hδU
  let b : ContDiffBump a :=
    ⟨R + δ / 3, R + 2 * δ / 3, by linarith, by linarith⟩
  let G : EuclideanSpace ℝ (Fin n) → EuclideanSpace ℝ (Fin n) := fun x => b x • F x
  refine ⟨G, ?_, b.hasCompactSupport.smul_right, ?_⟩
  · apply contDiff_iff_contDiffAt.mpr
    intro x
    by_cases hx : x ∈ closedBall a (δ + R)
    · exact b.contDiff.contDiffAt.smul (hgood x hx)
    · have hxb : x ∉ tsupport (b : EuclideanSpace ℝ (Fin n) → ℝ) := by
        rw [b.tsupport_eq]
        exact fun h => hx (closedBall_subset_closedBall (by dsimp [b]; linarith) h)
      apply (contDiffAt_const : ContDiffAt ℝ 1 (fun _ : EuclideanSpace ℝ (Fin n) =>
        (0 : EuclideanSpace ℝ (Fin n))) x).congr_of_eventuallyEq
      filter_upwards [notMem_tsupport_iff_eventuallyEq.mp hxb] with y hy
      simp [G, hy]
  · intro x hx
    have hxb : x ∈ ball a b.rIn := by
      have hxR := mem_closedBall.mp hx
      change dist x a < R + δ / 3
      linarith
    filter_upwards [b.eventuallyEq_one_of_mem_ball hxb] with y hy
    simp [G, hy]

private theorem divergence_continuous {n : ℕ}
    (F : EuclideanSpace ℝ (Fin n) → EuclideanSpace ℝ (Fin n))
    (hF : ContDiff ℝ 1 F) : Continuous (Divergence.coordinateDivergence F) := by
  have heq : Divergence.coordinateDivergence F = fun x =>
      ∑ i, fderiv ℝ F x (EuclideanSpace.single i (1 : ℝ)) i := by
    funext x
    exact Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_differentiableAt
      (hF.differentiable one_ne_zero x)
  rw [heq]
  apply continuous_finsetSum
  intro i _
  exact (PiLp.proj (p := 2) (𝕜 := ℝ) (fun _ : Fin n => ℝ) i).continuous.comp
    ((hF.continuous_fderiv one_ne_zero).clm_apply continuous_const)

private theorem compact_divergence_integral {n : ℕ}
    (F : EuclideanSpace ℝ (Fin (n + 1)) → EuclideanSpace ℝ (Fin (n + 1)))
    (hF : ContDiff ℝ 1 F) (hFc : HasCompactSupport F) :
    (∫ x, Divergence.coordinateDivergence F x) = 0 := by
  let e := PiLp.continuousLinearEquiv 2 ℝ (fun _ : Fin (n + 1) => ℝ)
  let G : (Fin (n + 1) → ℝ) → Fin (n + 1) → ℝ := fun x => e (F (e.symm x))
  have hG : ContDiff ℝ 1 G := e.contDiff.comp (hF.comp e.symm.contDiff)
  have hGc : HasCompactSupport G :=
    (hFc.comp_homeomorph e.symm.toHomeomorph).comp_left e.map_zero
  have hzero :=
    Divergence.integral_coordinateDivergence_wrapped_eq_zero_of_contDiff_of_hasCompactSupport
      G hG hGc
  have htransport := (PiLp.volume_preserving_toLp (Fin (n + 1))).integral_comp
    (MeasurableEquiv.measurableEmbedding (MeasurableEquiv.toLp 2 (Fin (n + 1) → ℝ)))
    (Divergence.coordinateDivergence F)
  simpa [G, e] using htransport.symm.trans hzero

private theorem divergence_integrable {n : ℕ}
    (F : EuclideanSpace ℝ (Fin n) → EuclideanSpace ℝ (Fin n))
    (hF : ContDiff ℝ 1 F) (hFc : HasCompactSupport F) :
    Integrable (Divergence.coordinateDivergence F) := by
  apply (divergence_continuous F hF).integrable_of_hasCompactSupport
  have heq : Divergence.coordinateDivergence F = fun x =>
      ∑ i, fderiv ℝ F x (EuclideanSpace.single i (1 : ℝ)) i := by
    funext x
    exact Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_differentiableAt
      (hF.differentiable one_ne_zero x)
  rw [heq]
  exact (hFc.fderiv ℝ).comp_left (g := fun
    (L : EuclideanSpace ℝ (Fin n) →L[ℝ] EuclideanSpace ℝ (Fin n)) =>
    ∑ i : Fin n, L (EuclideanSpace.single i (1 : ℝ)) i) (by simp)

private theorem polar_integral {n : ℕ}
    (g : EuclideanSpace ℝ (Fin (n + 1)) → ℝ) (hg : Integrable g) :
    (∫ x, g x) = ∫ r in Ioi (0 : ℝ), r ^ n *
      ∫ ζ : sphere (0 : EuclideanSpace ℝ (Fin (n + 1))) 1,
        g (r • ζ.1) ∂(volume : Measure (EuclideanSpace ℝ (Fin (n + 1)))).toSphere := by
  let E := EuclideanSpace ℝ (Fin (n + 1))
  let τ := (volume : Measure E).toSphere
  let f : sphere (0 : E) 1 × Ioi (0 : ℝ) → ℝ := fun p => g (p.2.1 • p.1.1)
  have hsub : Integrable (fun x : ({0}ᶜ : Set E) => g x.1)
      ((volume : Measure E).comap Subtype.val) :=
    (integrableOn_iff_comap_subtypeVal (measurableSet_singleton 0).compl).mp hg.restrict
  have hmp := (volume : Measure E).measurePreserving_homeomorphUnitSphereProd
  have hcomp : f ∘ homeomorphUnitSphereProd E = fun x : ({0}ᶜ : Set E) => g x.1 := by
    funext x
    change g ((homeomorphUnitSphereProd E).symm (homeomorphUnitSphereProd E x)).1 = g x.1
    rw [Homeomorph.symm_apply_apply]
  have hf : Integrable f (τ.prod (Measure.volumeIoiPow n)) := by
    have h := (hmp.integrable_comp_emb (Homeomorph.measurableEmbedding _)).mp
      (hcomp.symm ▸ hsub)
    simpa [E, τ] using h
  calc
    (∫ x, g x) = ∫ x : ({0}ᶜ : Set E), g x.1 ∂(volume : Measure E).comap Subtype.val := by
      rw [integral_subtype_comap (measurableSet_singleton _).compl,
        restrict_compl_singleton]
    _ = ∫ p, f p ∂τ.prod (Measure.volumeIoiPow n) := by
      have h := hmp.integral_comp (Homeomorph.measurableEmbedding _) f
      change (∫ x : ({0}ᶜ : Set E), (f ∘ homeomorphUnitSphereProd E) x
        ∂(volume : Measure E).comap Subtype.val) = _ at h
      rw [hcomp] at h
      simpa [E, τ] using h
    _ = ∫ r : Ioi (0 : ℝ), (∫ ζ, g (r.1 • ζ.1) ∂τ) ∂Measure.volumeIoiPow n :=
      integral_prod_symm f hf
    _ = _ := by
      simp only [Measure.volumeIoiPow, ENNReal.ofReal]
      rw [integral_withDensity_eq_integral_smul]
      · rw [integral_subtype_comap measurableSet_Ioi (fun r : ℝ =>
          Real.toNNReal (r ^ n) • ∫ ζ : sphere (0 : E) 1, g (r • ζ.1) ∂τ)]
        apply setIntegral_congr_fun measurableSet_Ioi
        intro r hr
        dsimp only
        rw [NNReal.smul_def, Real.coe_toNNReal _ (pow_nonneg hr.le _), smul_eq_mul]
      · exact (measurable_subtype_coe.pow_const n).real_toNNReal

private theorem radial_flux_integrable {n : ℕ}
    (F : EuclideanSpace ℝ (Fin n) → EuclideanSpace ℝ (Fin n))
    (hF : Continuous F) (a : EuclideanSpace ℝ (Fin n)) (r : ℝ) :
    Integrable (fun ζ : sphere (0 : EuclideanSpace ℝ (Fin n)) 1 =>
      inner ℝ (F (a + r • ζ.1)) ζ.1)
      (volume : Measure (EuclideanSpace ℝ (Fin n))).toSphere := by
  have hc : Continuous (fun ζ : sphere (0 : EuclideanSpace ℝ (Fin n)) 1 =>
      inner ℝ (F (a + r • ζ.1)) ζ.1) := by fun_prop
  exact hc.integrable_of_hasCompactSupport (HasCompactSupport.of_compactSpace _)

private theorem radial_flux_continuous {n : ℕ}
    (F : EuclideanSpace ℝ (Fin n) → EuclideanSpace ℝ (Fin n))
    (hF : Continuous F) (a : EuclideanSpace ℝ (Fin n)) :
    Continuous (fun r : ℝ => r ^ (n - 1) *
      ∫ ζ : sphere (0 : EuclideanSpace ℝ (Fin n)) 1,
        inner ℝ (F (a + r • ζ.1)) ζ.1
          ∂(volume : Measure (EuclideanSpace ℝ (Fin n))).toSphere) := by
  apply (continuous_id.pow _).mul
  have hc : Continuous (Function.uncurry (fun (r : ℝ)
      (ζ : sphere (0 : EuclideanSpace ℝ (Fin n)) 1) =>
      inner ℝ (F (a + r • ζ.1)) ζ.1)) := by fun_prop
  simpa using continuous_parametric_integral_of_continuous
    (μ := (volume : Measure (EuclideanSpace ℝ (Fin n))).toSphere) hc isCompact_univ

private def shellProfile (R ε s : ℝ) : ℝ :=
  1 - Real.smoothTransition ((s - R ^ 2) / ((R + ε) ^ 2 - R ^ 2))

private def shellCutoff {n : ℕ} (a : EuclideanSpace ℝ (Fin n)) (R ε : ℝ)
    (x : EuclideanSpace ℝ (Fin n)) : ℝ := shellProfile R ε (‖x - a‖ ^ 2)

private theorem shellProfile_smooth (R ε : ℝ) : ContDiff ℝ 2 (shellProfile R ε) := by
  unfold shellProfile
  exact contDiff_const.sub (Real.smoothTransition.contDiff.comp
    ((contDiff_id.sub contDiff_const).div_const _))

private theorem shellCutoff_smooth {n : ℕ} (a : EuclideanSpace ℝ (Fin n)) (R ε : ℝ) :
    ContDiff ℝ 2 (shellCutoff a R ε) :=
  (shellProfile_smooth R ε).comp ((contDiff_id.sub contDiff_const).norm_sq ℝ)

private theorem shellCutoff_bounds {n : ℕ} (a : EuclideanSpace ℝ (Fin n))
    (R ε : ℝ) (x : EuclideanSpace ℝ (Fin n)) :
    0 ≤ shellCutoff a R ε x ∧ shellCutoff a R ε x ≤ 1 := by
  dsimp [shellCutoff, shellProfile]
  constructor
  · exact sub_nonneg.mpr (Real.smoothTransition.le_one _)
  · exact sub_le_self _ (Real.smoothTransition.nonneg _)

private theorem shellCutoff_one {n : ℕ} (a : EuclideanSpace ℝ (Fin n))
    (R ε : ℝ) (hR : 0 < R) (hε : 0 < ε)
    (x : EuclideanSpace ℝ (Fin n)) (hx : x ∈ closedBall a R) :
    shellCutoff a R ε x = 1 := by
  have hD : 0 < (R + ε) ^ 2 - R ^ 2 := by nlinarith
  have hxR : ‖x - a‖ ≤ R := mem_closedBall_iff_norm.mp hx
  have hs : ‖x - a‖ ^ 2 - R ^ 2 ≤ 0 := by nlinarith [norm_nonneg (x - a)]
  simp [shellCutoff, shellProfile, Real.smoothTransition.zero_of_nonpos
    (div_nonpos_of_nonpos_of_nonneg hs hD.le)]

private theorem shellCutoff_zero {n : ℕ} (a : EuclideanSpace ℝ (Fin n))
    (R ε : ℝ) (hR : 0 < R) (hε : 0 < ε)
    (x : EuclideanSpace ℝ (Fin n)) (hx : R + ε ≤ ‖x - a‖) :
    shellCutoff a R ε x = 0 := by
  have hD : 0 < (R + ε) ^ 2 - R ^ 2 := by nlinarith
  have hs : (R + ε) ^ 2 - R ^ 2 ≤ ‖x - a‖ ^ 2 - R ^ 2 := by
    nlinarith [norm_nonneg (x - a)]
  have harg : 1 ≤ (‖x - a‖ ^ 2 - R ^ 2) / ((R + ε) ^ 2 - R ^ 2) := by
    exact (le_div_iff₀ hD).mpr (by simpa only [one_mul] using hs)
  simp [shellCutoff, shellProfile, Real.smoothTransition.one_of_one_le harg]

private theorem shellProfile_bounds (R ε s : ℝ) :
    0 ≤ shellProfile R ε s ∧ shellProfile R ε s ≤ 1 := by
  dsimp [shellProfile]
  exact ⟨sub_nonneg.mpr (Real.smoothTransition.le_one _),
    sub_le_self _ (Real.smoothTransition.nonneg _)⟩

private theorem shellProfile_deriv (R ε s : ℝ) :
    deriv (shellProfile R ε) s =
      -(deriv Real.smoothTransition ((s - R ^ 2) / ((R + ε) ^ 2 - R ^ 2)) /
        ((R + ε) ^ 2 - R ^ 2)) := by
  have hd := (hasDerivAt_const s (1 : ℝ)).sub
    (((Real.smoothTransition.contDiff (n := 1)).differentiable one_ne_zero _).hasDerivAt.comp s
      (((hasDerivAt_id s).sub_const (R ^ 2)).div_const ((R + ε) ^ 2 - R ^ 2)))
  convert! hd.deriv using 1
  simp [div_eq_mul_inv]

private def shellWeight (R ε r : ℝ) : ℝ :=
  -(2 * r * deriv (shellProfile R ε) (r ^ 2))

private theorem shellWeight_continuous (R ε : ℝ) : Continuous (shellWeight R ε) := by
  exact ((continuous_const.mul continuous_id).mul
    (((shellProfile_smooth R ε).continuous_deriv (by norm_num)).comp
      (continuous_id.pow 2))).neg

private theorem shellWeight_nonneg (R ε r : ℝ) (hR : 0 < R) (hε : 0 < ε)
    (hr : 0 ≤ r) : 0 ≤ shellWeight R ε r := by
  have hD : 0 < (R + ε) ^ 2 - R ^ 2 := by nlinarith
  rw [shellWeight, shellProfile_deriv]
  have ht := Real.smoothTransition.monotone.deriv_nonneg
    (x := (r ^ 2 - R ^ 2) / ((R + ε) ^ 2 - R ^ 2))
  have hq := div_nonneg ht hD.le
  nlinarith

private theorem shellWeight_derivative (R ε r : ℝ) :
    HasDerivAt (fun t : ℝ => -(shellProfile R ε (t ^ 2))) (shellWeight R ε r) r := by
  have h := (((shellProfile_smooth R ε).differentiable (by norm_num) (r ^ 2)).hasDerivAt.comp r
    ((hasDerivAt_id r).pow 2)).neg
  convert! h using 1
  simp [shellWeight]
  ring

private theorem shellWeight_mass (R ε : ℝ) (hR : 0 < R) (hε : 0 < ε) :
    (∫ r in R..R + ε, shellWeight R ε r) = 1 := by
  have hD : 0 < (R + ε) ^ 2 - R ^ 2 := by nlinarith
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt
    (fun r _ => shellWeight_derivative R ε r)
    ((shellWeight_continuous R ε).intervalIntegrable R (R + ε))
  simpa [shellProfile, div_self hD.ne'] using h

private theorem shellWeight_zero_inner (R ε r : ℝ) (hR : 0 < R) (hε : 0 < ε)
    (hr : 0 ≤ r) (hrR : r ≤ R) : shellWeight R ε r = 0 := by
  have hD : 0 < (R + ε) ^ 2 - R ^ 2 := by nlinarith
  have hs : shellProfile R ε (r ^ 2) = 1 := by
    have harg : (r ^ 2 - R ^ 2) / ((R + ε) ^ 2 - R ^ 2) ≤ 0 :=
      div_nonpos_of_nonpos_of_nonneg (by nlinarith) hD.le
    simp [shellProfile, Real.smoothTransition.zero_of_nonpos harg]
  have hmax : IsLocalMax (shellProfile R ε) (r ^ 2) := by
    show ∀ᶠ s in 𝓝 (r ^ 2), shellProfile R ε s ≤ shellProfile R ε (r ^ 2)
    exact Eventually.of_forall (fun s => hs ▸ (shellProfile_bounds R ε s).2)
  simp [shellWeight, hmax.deriv_eq_zero]

private theorem shellWeight_zero_outer (R ε r : ℝ) (hR : 0 < R) (hε : 0 < ε)
    (hr : R + ε ≤ r) : shellWeight R ε r = 0 := by
  have hD : 0 < (R + ε) ^ 2 - R ^ 2 := by nlinarith
  have hs : shellProfile R ε (r ^ 2) = 0 := by
    have harg : 1 ≤ (r ^ 2 - R ^ 2) / ((R + ε) ^ 2 - R ^ 2) := by
      apply (le_div_iff₀ hD).mpr
      nlinarith
    simp [shellProfile, Real.smoothTransition.one_of_one_le harg]
  have hmin : IsLocalMin (shellProfile R ε) (r ^ 2) := by
    show ∀ᶠ s in 𝓝 (r ^ 2), shellProfile R ε (r ^ 2) ≤ shellProfile R ε s
    exact Eventually.of_forall (fun s => hs ▸ (shellProfile_bounds R ε s).1)
  simp [shellWeight, hmin.deriv_eq_zero]

private theorem shellWeight_limit (R : ℝ) (hR : 0 < R)
    (H : ℝ → ℝ) (hH : Continuous H) :
    Tendsto (fun ε : ℝ => ∫ r in R..R + ε, shellWeight R ε r * H r)
      (𝓝[>] 0) (𝓝 (H R)) := by
  apply Metric.tendsto_nhds.mpr
  intro δ hδ
  obtain ⟨η, hη, hHη⟩ := Metric.continuousAt_iff.mp
    (show ContinuousAt H R from hH.continuousAt) (δ / 2) (by positivity)
  filter_upwards [Ioo_mem_nhdsGT hη] with ε hε
  have hW := shellWeight_continuous R ε
  have hmass := shellWeight_mass R ε hR hε.1
  have heq : (∫ r in R..R + ε, shellWeight R ε r * (H r - H R)) =
      (∫ r in R..R + ε, shellWeight R ε r * H r) - H R := by
    have hi1 : IntervalIntegrable (fun r => shellWeight R ε r * H r) volume R (R + ε) :=
      (hW.mul hH).intervalIntegrable R (R + ε)
    have hi2 : IntervalIntegrable (fun r => shellWeight R ε r * H R) volume R (R + ε) :=
      (hW.mul continuous_const).intervalIntegrable R (R + ε)
    simp_rw [mul_sub]
    rw [intervalIntegral.integral_sub hi1 hi2,
      intervalIntegral.integral_mul_const, hmass, one_mul]
  have hbound : ‖∫ r in R..R + ε, shellWeight R ε r * (H r - H R)‖ ≤ δ / 2 := by
    have h := intervalIntegral.norm_integral_le_of_norm_le
      (show R ≤ R + ε by linarith [hε.1])
      (f := fun r => shellWeight R ε r * (H r - H R))
      (g := fun r => shellWeight R ε r * (δ / 2))
      (Eventually.of_forall fun r hr => ?_)
      (show IntervalIntegrable (fun r => shellWeight R ε r * (δ / 2)) volume R (R + ε) from
        (hW.mul continuous_const).intervalIntegrable R (R + ε))
    · simpa [intervalIntegral.integral_mul_const, hmass] using h
    · have hr0 : 0 ≤ r := le_trans hR.le hr.1.le
      have hWr := shellWeight_nonneg R ε r hR hε.1 hr0
      have hrη : dist r R < η := by
        rw [Real.dist_eq, abs_of_nonneg (sub_nonneg.mpr hr.1.le)]
        linarith [hr.2, hε.2]
      have hHr : ‖H r - H R‖ ≤ δ / 2 := (hHη hrη).le
      rw [norm_mul, Real.norm_eq_abs (shellWeight R ε r), abs_of_nonneg hWr]
      exact mul_le_mul_of_nonneg_left hHr hWr
  rw [dist_eq_norm, ← heq]
  exact hbound.trans_lt (by linarith)

private theorem divergence_scalar_product {n : ℕ}
    (χ : EuclideanSpace ℝ (Fin n) → ℝ)
    (F : EuclideanSpace ℝ (Fin n) → EuclideanSpace ℝ (Fin n))
    (x : EuclideanSpace ℝ (Fin n))
    (hχ : DifferentiableAt ℝ χ x) (hF : DifferentiableAt ℝ F x) :
    Divergence.coordinateDivergence (fun y => χ y • F y) x =
      χ x * Divergence.coordinateDivergence F x + inner ℝ (gradient χ x) (F x) := by
  change Divergence.coordinateDivergence (χ • F) x = _
  rw [Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_hasFDerivAt
    (hχ.hasFDerivAt.smul hF.hasFDerivAt),
    Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_differentiableAt hF]
  simp only [add_apply, smul_apply,
    ContinuousLinearMap.smulRight_apply, PiLp.add_apply, PiLp.smul_apply, smul_eq_mul]
  rw [Finset.sum_add_distrib, ← Finset.mul_sum]
  congr 1
  calc
    (∑ i, fderiv ℝ χ x (EuclideanSpace.single i (1 : ℝ)) * F x i) =
        ∑ i, (gradient χ x) i * F x i := by
      apply Finset.sum_congr rfl
      intro i _
      rw [← inner_gradient_left, EuclideanSpace.inner_single_right]
      simp
    _ = inner ℝ (gradient χ x) (F x) := by
      rw [PiLp.inner_apply]
      apply Finset.sum_congr rfl
      intro i _
      simp [mul_comm]

private theorem scalar_cutoff_integral {n : ℕ}
    (F : EuclideanSpace ℝ (Fin (n + 1)) → EuclideanSpace ℝ (Fin (n + 1)))
    (hF : ContDiff ℝ 1 F) (hFc : HasCompactSupport F)
    (χ : EuclideanSpace ℝ (Fin (n + 1)) → ℝ) (hχ : ContDiff ℝ 1 χ)
    (hχbound : ∀ x, ‖χ x‖ ≤ 1) :
    Integrable (fun x => -(inner ℝ (gradient χ x) (F x))) ∧
    (∫ x, χ x * Divergence.coordinateDivergence F x) =
      ∫ x, -(inner ℝ (gradient χ x) (F x)) := by
  have hχF : ContDiff ℝ 1 (fun x => χ x • F x) := hχ.smul hF
  have hχFc : HasCompactSupport (fun x => χ x • F x) := hFc.smul_left (f := χ)
  have hdivχF := divergence_integrable _ hχF hχFc
  have hχdiv : Integrable (fun x => χ x * Divergence.coordinateDivergence F x) :=
    (divergence_integrable F hF hFc).bdd_mul (c := 1) hχ.continuous.aestronglyMeasurable
      (Eventually.of_forall hχbound)
  have hcross : Integrable (fun x => inner ℝ (gradient χ x) (F x)) :=
    (hdivχF.sub hχdiv).congr (Eventually.of_forall fun x => by
      change Divergence.coordinateDivergence (fun y => χ y • F y) x -
        χ x * Divergence.coordinateDivergence F x = inner ℝ (gradient χ x) (F x)
      rw [divergence_scalar_product χ F x
        (hχ.differentiable one_ne_zero x) (hF.differentiable one_ne_zero x)]
      ring)
  have heq : Divergence.coordinateDivergence (fun x => χ x • F x) =
      fun x => χ x * Divergence.coordinateDivergence F x + inner ℝ (gradient χ x) (F x) := by
    funext x
    exact divergence_scalar_product χ F x
      (hχ.differentiable one_ne_zero x) (hF.differentiable one_ne_zero x)
  have hz := compact_divergence_integral _ hχF hχFc
  rw [heq, integral_add hχdiv hcross] at hz
  refine ⟨hcross.neg, ?_⟩
  rw [integral_neg]
  linarith

private theorem cutoff_sphere_pairing {n : ℕ}
    (F : EuclideanSpace ℝ (Fin n) → EuclideanSpace ℝ (Fin n))
    (a : EuclideanSpace ℝ (Fin n)) (R ε r : ℝ)
    (ζ : sphere (0 : EuclideanSpace ℝ (Fin n)) 1) :
    -(inner ℝ (gradient (shellCutoff a R ε) (a + r • ζ.1)) (F (a + r • ζ.1))) =
      shellWeight R ε r * inner ℝ (F (a + r • ζ.1)) ζ.1 := by
  have hgrad := (RadialCalculus.radial_gradient_laplacian (shellProfile R ε)
    a (a + r • ζ.1) (shellProfile_smooth R ε).contDiffAt).1
  have hζ : ‖(ζ : EuclideanSpace ℝ (Fin n))‖ = 1 := by
    simpa only [mem_sphere, dist_zero_right] using ζ.property
  change -(inner ℝ (gradient (fun x => shellProfile R ε (‖x - a‖ ^ 2))
    (a + r • ζ.1)) (F (a + r • ζ.1))) = _
  rw [hgrad]
  simp only [add_sub_cancel_left, norm_smul, Real.norm_eq_abs, hζ, mul_one,
    sq_abs, real_inner_smul_left]
  rw [real_inner_comm ζ.1]
  dsimp [shellWeight]
  ring

private theorem cutoff_volume_limit {n : ℕ}
    (D : EuclideanSpace ℝ (Fin (n + 1)) → ℝ) (hD : Integrable D)
    (a : EuclideanSpace ℝ (Fin (n + 1))) (R : ℝ) (hR : 0 < R) :
    Tendsto (fun ε : ℝ => ∫ x, shellCutoff a R ε x * D x)
      (𝓝[>] 0) (𝓝 (∫ x in ball a R, D x)) := by
  have hS : ∀ᵐ x : EuclideanSpace ℝ (Fin (n + 1)), x ∉ sphere a R :=
    measure_eq_zero_iff_ae_notMem.mp ((volume : Measure (EuclideanSpace ℝ (Fin (n + 1)))).addHaar_sphere a R)
  have hlim := tendsto_integral_filter_of_dominated_convergence (fun x => ‖D x‖)
    (f := (ball a R).indicator D) (l := 𝓝[>] (0 : ℝ))
    (F := fun ε x => shellCutoff a R ε x * D x)
    (Eventually.of_forall fun ε =>
      (shellCutoff_smooth a R ε).continuous.aestronglyMeasurable.mul hD.aestronglyMeasurable)
    (Eventually.of_forall fun ε => Eventually.of_forall fun x => by
      rw [norm_mul]
      have hχ : ‖shellCutoff a R ε x‖ ≤ 1 := by
        rw [Real.norm_eq_abs, abs_of_nonneg (shellCutoff_bounds a R ε x).1]
        exact (shellCutoff_bounds a R ε x).2
      simpa only [one_mul] using mul_le_mul_of_nonneg_right hχ (norm_nonneg (D x)))
    hD.norm (hS.mono fun x hxS => ?_)
  · simpa only [integral_indicator measurableSet_ball] using hlim
  · by_cases hx : x ∈ ball a R
    · have heq : (fun ε => shellCutoff a R ε x * D x) =ᶠ[𝓝[>] (0 : ℝ)]
          (fun _ => (ball a R).indicator D x) := by
        filter_upwards [self_mem_nhdsWithin] with ε hε
        rw [shellCutoff_one a R ε hR hε x (ball_subset_closedBall hx)]
        simp [hx]
      exact (tendsto_congr' heq).mpr tendsto_const_nhds
    · have hxR : R < ‖x - a‖ := by
        have hle : R ≤ ‖x - a‖ := by simpa only [mem_ball_iff_norm, not_lt] using hx
        have hne : ‖x - a‖ ≠ R := by simpa only [mem_sphere_iff_norm] using hxS
        exact lt_of_le_of_ne hle hne.symm
      have heq : (fun ε => shellCutoff a R ε x * D x) =ᶠ[𝓝[>] (0 : ℝ)]
          (fun _ => (ball a R).indicator D x) := by
        filter_upwards [Ioo_mem_nhdsGT (sub_pos.mpr hxR)] with ε hε
        rw [shellCutoff_zero a R ε hR hε.1 x (by linarith [hε.2])]
        simp [hx]
      exact (tendsto_congr' heq).mpr tendsto_const_nhds

private theorem cutoff_flux_identity {n : ℕ}
    (F : EuclideanSpace ℝ (Fin (n + 1)) → EuclideanSpace ℝ (Fin (n + 1)))
    (hF : ContDiff ℝ 1 F) (hFc : HasCompactSupport F)
    (a : EuclideanSpace ℝ (Fin (n + 1))) (R ε : ℝ) (hR : 0 < R) (hε : 0 < ε) :
    (∫ x, shellCutoff a R ε x * Divergence.coordinateDivergence F x) =
      ∫ r in R..R + ε, shellWeight R ε r * (r ^ n *
        ∫ ζ : sphere (0 : EuclideanSpace ℝ (Fin (n + 1))) 1,
          inner ℝ (F (a + r • ζ.1)) ζ.1
            ∂(volume : Measure (EuclideanSpace ℝ (Fin (n + 1)))).toSphere) := by
  let E := EuclideanSpace ℝ (Fin (n + 1))
  let τ := (volume : Measure E).toSphere
  let χ := shellCutoff a R ε
  let K : E → ℝ := fun x => -(inner ℝ (gradient χ x) (F x))
  let H : ℝ → ℝ := fun r => r ^ n * ∫ ζ : sphere (0 : E) 1,
    inner ℝ (F (a + r • ζ.1)) ζ.1 ∂τ
  have hχ : ContDiff ℝ 1 χ := (shellCutoff_smooth a R ε).of_le (by norm_num)
  have hb : ∀ x, ‖χ x‖ ≤ 1 := fun x => by
    rw [Real.norm_eq_abs, abs_of_nonneg (shellCutoff_bounds a R ε x).1]
    exact (shellCutoff_bounds a R ε x).2
  have hdata := scalar_cutoff_integral F hF hFc χ hχ hb
  have hKt : Integrable (fun x => K (a + x)) :=
    ((measurePreserving_add_left (volume : Measure E) a).integrable_comp_emb
      (MeasurableEquiv.addLeft a).measurableEmbedding).mpr hdata.1
  have hinner (r : ℝ) : (∫ ζ : sphere (0 : E) 1, K (a + r • ζ.1) ∂τ) =
      shellWeight R ε r * ∫ ζ : sphere (0 : E) 1, inner ℝ (F (a + r • ζ.1)) ζ.1 ∂τ := by
    calc
      _ = ∫ ζ : sphere (0 : E) 1,
          shellWeight R ε r * inner ℝ (F (a + r • ζ.1)) ζ.1 ∂τ := by
        apply integral_congr_ae
        exact Eventually.of_forall (fun ζ => cutoff_sphere_pairing F a R ε r ζ)
      _ = _ := integral_const_mul _ _
  calc
    _ = ∫ x, K x := hdata.2
    _ = ∫ x, K (a + x) := (integral_add_left_eq_self K a).symm
    _ = ∫ r in Ioi (0 : ℝ), r ^ n * ∫ ζ : sphere (0 : E) 1, K (a + r • ζ.1) ∂τ :=
      polar_integral _ hKt
    _ = ∫ r in Ioi (0 : ℝ), shellWeight R ε r * H r := by
      apply setIntegral_congr_fun measurableSet_Ioi
      intro r _
      dsimp only
      rw [hinner]
      dsimp [H]
      ring
    _ = ∫ r in R..R + ε, shellWeight R ε r * H r := by
      rw [intervalIntegral.integral_of_le (show R ≤ R + ε by linarith)]
      apply setIntegral_eq_of_subset_of_forall_sdiff_eq_zero measurableSet_Ioi
        (fun r hr => lt_trans hR hr.1)
      intro r hr
      have hr0 : 0 < r := hr.1
      have hout : r ≤ R ∨ R + ε < r := by simpa only [mem_Ioc, not_and_or, not_lt, not_le] using hr.2
      rcases hout with h | h
      · rw [shellWeight_zero_inner R ε r hR hε hr0.le h, zero_mul]
      · rw [shellWeight_zero_outer R ε r hR hε h.le, zero_mul]
    _ = _ := rfl

private theorem compact_ball_flux {n : ℕ}
    (F : EuclideanSpace ℝ (Fin (n + 1)) → EuclideanSpace ℝ (Fin (n + 1)))
    (hF : ContDiff ℝ 1 F) (hFc : HasCompactSupport F)
    (a : EuclideanSpace ℝ (Fin (n + 1))) (R : ℝ) (hR : 0 < R) :
    IntegrableOn (Divergence.coordinateDivergence F) (ball a R) ∧
    Integrable (fun ζ : sphere (0 : EuclideanSpace ℝ (Fin (n + 1))) 1 =>
      inner ℝ (F (a + R • ζ.1)) ζ.1)
      (volume : Measure (EuclideanSpace ℝ (Fin (n + 1)))).toSphere ∧
    (∫ x in ball a R, Divergence.coordinateDivergence F x) = R ^ n *
      ∫ ζ : sphere (0 : EuclideanSpace ℝ (Fin (n + 1))) 1,
        inner ℝ (F (a + R • ζ.1)) ζ.1
          ∂(volume : Measure (EuclideanSpace ℝ (Fin (n + 1)))).toSphere := by
  have hD := divergence_integrable F hF hFc
  refine ⟨hD.restrict, radial_flux_integrable F hF.continuous a R, ?_⟩
  let H : ℝ → ℝ := fun r => r ^ n *
    ∫ ζ : sphere (0 : EuclideanSpace ℝ (Fin (n + 1))) 1,
      inner ℝ (F (a + r • ζ.1)) ζ.1
        ∂(volume : Measure (EuclideanSpace ℝ (Fin (n + 1)))).toSphere
  have hH : Continuous H := by
    simpa [H] using radial_flux_continuous F hF.continuous a
  have heq : (fun ε => ∫ x, shellCutoff a R ε x * Divergence.coordinateDivergence F x)
      =ᶠ[𝓝[>] (0 : ℝ)] (fun ε => ∫ r in R..R + ε, shellWeight R ε r * H r) := by
    filter_upwards [self_mem_nhdsWithin] with ε hε
    exact cutoff_flux_identity F hF hFc a R ε hR hε
  exact tendsto_nhds_unique (cutoff_volume_limit _ hD a R hR)
    ((tendsto_congr' heq).mpr (shellWeight_limit R hR H hH))

/-- The literal polar-sphere flux of a locally C1 field equals its ball
divergence integral. Both actual integrabilities are derived internally. -/
theorem ball_flux_eq_integral_divergence {n : ℕ}
    (F : EuclideanSpace ℝ (Fin n) → EuclideanSpace ℝ (Fin n))
    (a : EuclideanSpace ℝ (Fin n)) (R : ℝ) (hR : 0 < R)
    (hF : ∀ x ∈ Metric.closedBall a R, ContDiffAt ℝ 1 F x) :
    let τ : MeasureTheory.Measure (Metric.sphere (0 : EuclideanSpace ℝ (Fin n)) 1) :=
      (MeasureTheory.volume : MeasureTheory.Measure (EuclideanSpace ℝ (Fin n))).toSphere
    MeasureTheory.IntegrableOn
      (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence F)
      (Metric.ball a R) ∧
    MeasureTheory.Integrable (fun ζ : Metric.sphere (0 : EuclideanSpace ℝ (Fin n)) 1 =>
      inner ℝ (F (a + R • (ζ : EuclideanSpace ℝ (Fin n))))
        (ζ : EuclideanSpace ℝ (Fin n))) τ ∧
    (∫ x in Metric.ball a R,
      AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence F x) =
      R ^ (n - 1) * ∫ ζ : Metric.sphere (0 : EuclideanSpace ℝ (Fin n)) 1,
        inner ℝ (F (a + R • (ζ : EuclideanSpace ℝ (Fin n))))
          (ζ : EuclideanSpace ℝ (Fin n)) ∂τ := by
  dsimp only
  cases n with
  | zero =>
    have ht : (volume : Measure (EuclideanSpace ℝ (Fin 0))).toSphere = 0 :=
      (Measure.toSphere_eq_zero_iff_finrank _).mpr (by simp)
    simp [ht, Divergence.coordinateDivergence, IntegrableOn]
  | succ n =>
    obtain ⟨G, hG, hGc, hGF⟩ := local_c1_extension F a R hR hF
    obtain ⟨hD, hB, heq⟩ := compact_ball_flux G hG hGc a R hR
    have hdiv (x : EuclideanSpace ℝ (Fin (n + 1))) (hx : x ∈ closedBall a R) :
        Divergence.coordinateDivergence F x = Divergence.coordinateDivergence G x := by
      rw [Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_differentiableAt
        ((hF x hx).differentiableAt one_ne_zero),
        Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_differentiableAt
        (hG.differentiable one_ne_zero x), (hGF x hx).fderiv_eq]
    have hmem (ζ : sphere (0 : EuclideanSpace ℝ (Fin (n + 1))) 1) :
        a + R • ζ.1 ∈ closedBall a R := by
      have hζ : ‖(ζ : EuclideanSpace ℝ (Fin (n + 1)))‖ = 1 := by
        simpa only [mem_sphere, dist_zero_right] using ζ.property
      simp only [mem_closedBall_iff_norm, add_sub_cancel_left, norm_smul,
        Real.norm_eq_abs, abs_of_pos hR, hζ, mul_one, le_refl]
    have hboundary :
        (fun ζ : sphere (0 : EuclideanSpace ℝ (Fin (n + 1))) 1 =>
          inner ℝ (F (a + R • ζ.1)) ζ.1) =
        (fun ζ : sphere (0 : EuclideanSpace ℝ (Fin (n + 1))) 1 =>
          inner ℝ (G (a + R • ζ.1)) ζ.1) := by
      funext ζ
      rw [(hGF _ (hmem ζ)).eq_of_nhds]
    have hD' : IntegrableOn (Divergence.coordinateDivergence F) (ball a R) :=
      hD.congr (by
        filter_upwards [ae_restrict_mem measurableSet_ball] with x hx
        exact (hdiv x (ball_subset_closedBall hx)).symm)
    refine ⟨hD', ?_, ?_⟩
    · rw [hboundary]
      exact hB
    · calc
        _ = ∫ x in ball a R, Divergence.coordinateDivergence G x :=
          setIntegral_congr_fun measurableSet_ball (fun x hx => hdiv x (ball_subset_closedBall hx))
        _ = _ := heq
        _ = _ := by rw [hboundary, Nat.add_sub_cancel]

end
end AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.BallFlux
