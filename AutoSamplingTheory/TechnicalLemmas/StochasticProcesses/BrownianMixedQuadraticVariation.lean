import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianPredictableQuadraticVariationL2
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.EuclideanBrownianCoordinates

/-!
# Mixed Brownian quadratic variation with predictable weights

Unit projections of one vector Brownian motion preserve the given filtration.
Polarization then turns the mixed-coordinate increment product into a linear
combination of compensated squares of three such projections.
-/

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianMixedQuadraticVariation

open Filter MeasureTheory ProbabilityTheory
open scoped NNReal BigOperators RealInnerProductSpace
open BrownianMotion BrownianQuadraticVariation BrownianQuadraticVariationL2
  BrownianPredictableQuadraticVariationL2
  FiniteTimeGrid SampledElementaryApproximation EuclideanBrownianCoordinates

/-- A unit linear functional of the given Hilbert-space Brownian motion
is a real Brownian motion relative to the same filtration. -/
theorem standardBrownian_unit_projection
    {Omega E : Type*} [MeasurableSpace Omega]
    [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Omega)} {mu : Measure Omega}
    {B : ℝ≥0 → Omega → E}
    (hB : IsStandardBrownianMotionWithFiltration B filtration mu)
    (ell : StrongDual ℝ E) (hEll : ‖ell‖ = 1) :
    IsBrownianMotionWithFiltration (fun t omega => ell (B t omega)) filtration mu := by
  have hLaw {s t : ℝ≥0} (hst : s < t) :
      HasLaw (fun omega => ell (B t omega) - ell (B s omega))
        (gaussianReal 0 (t - s)) mu := by
    simpa [map_sub, projectedIncrementVariance, hEll] using
      hB.isStandard.2.2.1 s t hst ell
  let _ : IsProbabilityMeasure mu := (hLaw (show (0 : ℝ≥0) < 1 by norm_num)).isProbabilityMeasure
  have hzero (omega : Omega) : ell (B 0 omega) = 0 := by
    rw [hB.isStandard.1 omega, map_zero]
  have hEval (t : ℝ≥0) : HasLaw (fun omega => ell (B t omega)) (gaussianReal 0 t) mu := by
    by_cases ht : t = 0
    · subst t
      simpa using (hasLaw_dirac_of_ae_eq (Eventually.of_forall hzero) :
        HasLaw (fun omega => ell (B 0 omega)) (Measure.dirac 0) mu)
    · simpa only [hzero, sub_zero, tsub_zero] using hLaw (pos_iff_ne_zero.mpr ht)
  refine ⟨⟨?_, ?_⟩, ?_, ?_⟩
  · exact HasIndepIncrements.isPreBrownianReal_of_hasLaw hEval
      (hB.isStandard.projected_hasIndepIncrements ell)
  · filter_upwards [hB.isStandard.2.2.2] with omega hcont
    exact ell.continuous.comp hcont
  · intro t
    exact ell.continuous.comp_stronglyMeasurable (hB.stronglyAdapted t)
  · intro s t hst
    have he : (fun omega => ell (B t omega) - ell (B s omega)) =
        ell ∘ (fun omega => B t omega - B s omega) := by
      funext omega
      exact (map_sub ell _ _).symm
    rw [he, ← MeasurableSpace.comap_comp]
    have hle : (borel ℝ).comap ell ≤ borel E := by
      simpa only [← BorelSpace.measurable_eq (α := ℝ), ← BorelSpace.measurable_eq (α := E)]
        using ell.measurable.comap_le
    exact indep_of_indep_of_le (hB.incrementIndependent s t hst) le_rfl
      (MeasurableSpace.comap_mono hle)

/-- Left-past weighted mixed-coordinate products converge to zero in mean
square. Both coordinates belong to the same Euclidean Brownian driver. -/
theorem dyadic_predictable_mixed_increment_sum_L2
    {Omega kappa : Type*} [MeasurableSpace Omega] [Fintype kappa] [DecidableEq kappa]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Omega)} {mu : Measure Omega}
    {B : ℝ≥0 → Omega → EuclideanSpace ℝ kappa}
    (hB : IsStandardBrownianMotionWithFiltration B filtration mu)
    {j k : kappa} (hjk : j ≠ k) (T : ℝ≥0)
    (weight : (level : ℕ) → Fin (2 ^ level) → Omega → ℝ)
    (hAdapted : ∀ level i,
      StronglyMeasurable[filtration
        (regularGridTimes (dyadicMesh T level) (2 ^ level) i.castSucc)] (weight level i))
    (hWeight : ∀ level i, MemLp (weight level i) 2 mu)
    (C : ℝ) (hC : ∀ level i, (∫ omega, (weight level i omega)^2 ∂mu) ≤ C) :
    let error := fun level omega =>
      let times := regularGridTimes (dyadicMesh T level) (2 ^ level)
      ∑ i, weight level i omega *
        ((B (times i.succ) omega j - B (times i.castSucc) omega j) *
          (B (times i.succ) omega k - B (times i.castSucc) omega k))
    (∀ level, MemLp (error level) 2 mu) ∧
      Tendsto (fun level => ∫ omega, (error level omega)^2 ∂mu) atTop (nhds 0) := by
  let basis := EuclideanSpace.basisFun kappa ℝ
  let a := (Real.sqrt 2)⁻¹
  let ell := InnerProductSpace.toDualMap ℝ (EuclideanSpace ℝ kappa)
    (a • (basis j + basis k))
  have hBasis : ‖basis j + basis k‖ = Real.sqrt 2 := by
    have hSq : ‖basis j + basis k‖^2 = 2 := by
      rw [norm_add_sq_real, basis.orthonormal.norm_eq_one j, basis.orthonormal.norm_eq_one k,
        basis.orthonormal.inner_eq_zero hjk]
      norm_num
    rw [← hSq, Real.sqrt_sq (norm_nonneg _)]
  have hEll : ‖ell‖ = 1 := by
    dsimp [ell]
    rw [LinearIsometry.norm_map, norm_smul, Real.norm_eq_abs, abs_of_nonneg
      (inv_nonneg.mpr (Real.sqrt_nonneg _)), hBasis, inv_mul_cancel₀ (by positivity)]
  have ha : a^2 = 1/2 := by
    dsimp [a]
    rw [inv_pow, Real.sq_sqrt (by norm_num)]
    norm_num
  have hValue (x : EuclideanSpace ℝ kappa) : ell x = a * (x j + x k) := by
    change inner ℝ (a • (basis j + basis k)) x = _
    rw [real_inner_smul_left, inner_add_left]
    simp only [basis, EuclideanSpace.basisFun_inner]
  let U : ℝ≥0 → Omega → ℝ := fun t omega => ell (B t omega)
  let J : ℝ≥0 → Omega → ℝ := fun t omega => B t omega j
  let K : ℝ≥0 → Omega → ℝ := fun t omega => B t omega k
  have hU : IsBrownianMotionWithFiltration U filtration mu := standardBrownian_unit_projection hB ell hEll
  have hJ : IsBrownianMotionWithFiltration J filtration mu := (coordinateFamily hB).isBrownian j
  have hK : IsBrownianMotionWithFiltration K filtration mu := (coordinateFamily hB).isBrownian k
  let times (level : ℕ) := regularGridTimes (dyadicMesh T level) (2 ^ level)
  let err (X : ℝ≥0 → Omega → ℝ) (level : ℕ) (omega : Omega) : ℝ :=
    ∑ i, weight level i omega * centeredSquaredIncrement X (times level) i omega
  let cross (level : ℕ) (omega : Omega) : ℝ :=
    ∑ i, weight level i omega *
      ((J (times level i.succ) omega - J (times level i.castSucc) omega) *
        (K (times level i.succ) omega - K (times level i.castSucc) omega))
  have hPolar (level : ℕ) (i : Fin (2^level)) (omega : Omega) :
      (J (times level i.succ) omega - J (times level i.castSucc) omega) *
          (K (times level i.succ) omega - K (times level i.castSucc) omega) =
        centeredSquaredIncrement U (times level) i omega -
          centeredSquaredIncrement J (times level) i omega / 2 -
          centeredSquaredIncrement K (times level) i omega / 2 := by
    have hInc : U (times level i.succ) omega - U (times level i.castSucc) omega =
        a * ((J (times level i.succ) omega - J (times level i.castSucc) omega) +
          (K (times level i.succ) omega - K (times level i.castSucc) omega)) := by
      simp only [U,J,K,hValue]
      ring
    simp only [centeredSquaredIncrement, hInc, mul_pow, ha]
    ring
  have hCross (level : ℕ) (omega : Omega) :
      cross level omega = err U level omega - err J level omega / 2 - err K level omega / 2 := by
    simp only [cross,err,hPolar,mul_sub,mul_div_assoc,Finset.sum_sub_distrib,Finset.sum_div]
  have hMem (X : ℝ≥0 → Omega → ℝ)
      (hX : IsBrownianMotionWithFiltration X filtration mu) (level : ℕ) :
      MemLp (err X level) 2 mu := by
    have hmono : Monotone (times level) := by
      intro p q hpq
      unfold times regularGridTimes
      gcongr
      exact_mod_cast hpq
    exact (predictable_weighted_quadraticVariationError_L2 hX hmono
      (weight level) (hAdapted level) (hWeight level)).1
  have hCrossMem (level : ℕ) : MemLp (cross level) 2 mu := by
    have hm := ((hMem U hU level).sub ((hMem J hJ level).const_mul (1/2 : ℝ))).sub
      ((hMem K hK level).const_mul (1/2 : ℝ))
    refine (memLp_congr_ae ?_).1 hm
    filter_upwards [] with omega
    simp only [Pi.sub_apply, hCross]
    ring
  have hSquare (x y z : ℝ) :
      (x - y/2 - z/2)^2 ≤ 3*x^2 + (3/4)*y^2 + (3/4)*z^2 := by
    nlinarith [sq_nonneg (x+y/2), sq_nonneg (x+z/2), sq_nonneg ((y-z)/2)]
  have hUpper (level : ℕ) :
      (∫ omega, (cross level omega)^2 ∂mu) ≤
        3 * (∫ omega, (err U level omega)^2 ∂mu) +
          (3/4) * (∫ omega, (err J level omega)^2 ∂mu) +
          (3/4) * (∫ omega, (err K level omega)^2 ∂mu) := by
    have hu := (hMem U hU level).integrable_sq.const_mul 3
    have hj := (hMem J hJ level).integrable_sq.const_mul (3/4)
    have hk := (hMem K hK level).integrable_sq.const_mul (3/4)
    calc
      _ ≤ ∫ omega, 3 * (err U level omega)^2 +
          (3/4) * (err J level omega)^2 + (3/4) * (err K level omega)^2 ∂mu :=
        integral_mono (hCrossMem level).integrable_sq ((hu.add hj).add hk) (fun omega => by
          rw [hCross]
          exact hSquare _ _ _)
      _ = _ := by
        have hOuter := integral_add (hu.add hj) hk
        have hInner := integral_add hu hj
        simp only [Pi.add_apply] at hOuter hInner
        rw [hOuter, hInner]
        simp only [integral_const_mul]
  have hLimit (X : ℝ≥0 → Omega → ℝ) (hX : IsBrownianMotionWithFiltration X filtration mu) :
      Tendsto (fun level => ∫ omega, (err X level omega)^2 ∂mu) atTop (nhds 0) :=
    tendsto_integral_dyadic_predictable_weighted_quadraticVariationError_sq hX T
      weight hAdapted hWeight C hC
  have hLimitUpper := (((hLimit U hU).const_mul 3).add
    ((hLimit J hJ).const_mul (3/4))).add ((hLimit K hK).const_mul (3/4))
  refine ⟨hCrossMem, ?_⟩
  change Tendsto (fun level => ∫ omega, (cross level omega)^2 ∂mu) atTop (nhds 0)
  refine tendsto_const_nhds.squeeze ?_ (fun level => integral_nonneg fun _ => sq_nonneg _) hUpper
  simpa using hLimitUpper

/-- The mean-square convergence consequence of the full mixed-coordinate estimate. -/
theorem tendsto_integral_dyadic_predictable_mixed_increment_sum_sq
    {Omega kappa : Type*} [MeasurableSpace Omega] [Fintype kappa] [DecidableEq kappa]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Omega)} {mu : Measure Omega}
    {B : ℝ≥0 → Omega → EuclideanSpace ℝ kappa}
    (hB : IsStandardBrownianMotionWithFiltration B filtration mu)
    {j k : kappa} (hjk : j ≠ k) (T : ℝ≥0)
    (weight : (level : ℕ) → Fin (2 ^ level) → Omega → ℝ)
    (hAdapted : ∀ level i,
      StronglyMeasurable[filtration
        (regularGridTimes (dyadicMesh T level) (2 ^ level) i.castSucc)] (weight level i))
    (hWeight : ∀ level i, MemLp (weight level i) 2 mu)
    (C : ℝ) (hC : ∀ level i, (∫ omega, (weight level i omega)^2 ∂mu) ≤ C) :
    Tendsto (fun level =>
      let times := regularGridTimes (dyadicMesh T level) (2 ^ level)
      ∫ omega, (∑ i, weight level i omega *
        ((B (times i.succ) omega j - B (times i.castSucc) omega j) *
          (B (times i.succ) omega k - B (times i.castSucc) omega k)))^2 ∂mu)
      atTop (nhds 0) :=
  (dyadic_predictable_mixed_increment_sum_L2 hB hjk T weight hAdapted hWeight C hC).2

#print axioms dyadic_predictable_mixed_increment_sum_L2
#print axioms standardBrownian_unit_projection
#print axioms tendsto_integral_dyadic_predictable_mixed_increment_sum_sq

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianMixedQuadraticVariation
