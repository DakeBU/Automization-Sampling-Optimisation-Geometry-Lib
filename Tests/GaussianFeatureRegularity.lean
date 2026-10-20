import AutoSamplingTheory.TechnicalLemmas.Analysis.ProbabilitySegmentRisk
import AutoSamplingTheory.TechnicalLemmas.Analysis.JointEmpiricalSegmentRisk
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialAveraging
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRisk
import AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment

open MeasureTheory ProbabilityTheory
open scoped ENNReal InnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.Analysis.ProbabilitySegmentRisk
open AutoSamplingTheory.TechnicalLemmas.Analysis.JointEmpiricalSegmentRisk
open AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialAveraging
open AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRisk

namespace Tests.GaussianFeatureRegularity
noncomputable section

-- A genuine clipped probability path: its right risk derivative is -4.
example : HasDerivWithinAt
    (fun t : ℝ => ‖(∫ q : ℝ, q ∂(ENNReal.ofReal (1-t) • Measure.dirac 0 +
      ENNReal.ofReal t • Measure.dirac 1)) - 2‖^2) (-4)
    (Set.Icc (0 : ℝ) 1) 0 := by
  have h := quadratic_feature_probability_segment (Measure.dirac (0 : ℝ))
    (Measure.dirac (1 : ℝ)) (fun q : ℝ => q) (2 : ℝ)
    (integrable_dirac (by simp)) (integrable_dirac (by simp))
  dsimp only at h
  have hd := h.2.2.2.1
  convert hd using 1 <;> norm_num [Real.inner_apply]

/-- Nondegenerate responses at the same input: response is not a function of input. -/
private def noisyData : Measure (Unit × ℝ) :=
  (2 : ℝ≥0∞)⁻¹ • (Measure.dirac ((), 1) + Measure.dirac ((), 3))

private instance : IsProbabilityMeasure noisyData := by
  constructor
  change (2 : ℝ≥0∞)⁻¹ * ((Measure.dirac ((), (1 : ℝ)) + Measure.dirac ((), 3) : Measure (Unit × ℝ)) Set.univ) = 1
  simp only [Measure.add_apply, measure_univ, one_add_one_eq_two]
  exact ENNReal.inv_mul_cancel (by norm_num) (by norm_num)

private def signFeature (q : Fin 2) (_ : Unit) : ℝ := if q = 0 then 1 else -1

private def empiricalTwo (cfg : Fin 2 → Fin 2) : Measure (Fin 2) :=
  (2 : ℝ≥0∞)⁻¹ • ∑ j, Measure.dirac (cfg j)

private theorem empiricalTwo_integral (cfg : Fin 2 → Fin 2) (g : Fin 2 → ℝ) :
    (∫ q, g q ∂empiricalTwo cfg) = (g (cfg 0) + g (cfg 1)) / 2 := by
  rw [empiricalTwo, integral_smul_measure,
    integral_finsetSum_measure (fun j _ => integrable_dirac (by simp))]
  norm_num [Fin.sum_univ_two, smul_eq_mul]
  ring

private theorem noisyData_integral (g : Unit × ℝ → ℝ) :
    (∫ z, g z ∂noisyData) = (g ((), 1) + g ((), 3)) / 2 := by
  rw [noisyData, integral_smul_measure,
    integral_add_measure (integrable_dirac (by simp)) (integrable_dirac (by simp))]
  norm_num [smul_eq_mul]
  ring


-- Repeated endpoint particles and genuinely noisy labels give derivative +4.
example :
    let rho0 := empiricalTwo (fun _ => 0)
    let rho1 := empiricalTwo (fun _ => 1)
    let predictor : Measure (Fin 2) → Unit → ℝ := fun rho x => ∫ q, signFeature q x ∂rho
    let curve : ℝ → Measure (Fin 2) := fun t => ENNReal.ofReal (1-t) • rho0 + ENNReal.ofReal t • rho1
    HasDerivWithinAt (fun t => ∫ z, (predictor (curve t) z.1-z.2)^2 ∂noisyData)
      4 (Set.Icc (0 : ℝ) 1) 0 := by
  dsimp only
  haveI : IsProbabilityMeasure (noisyData.map (Prod.fst : Unit × ℝ → Unit)) :=
    Measure.isProbabilityMeasure_map measurable_fst.aemeasurable
  have hf (q : Fin 2) : MemLp (signFeature q) 2 (noisyData.map Prod.fst) := memLp_const _
  have hy : MemLp (fun z : Unit × ℝ => z.2) 2 noisyData := by
    apply MemLp.of_bound measurable_snd.aestronglyMeasurable 3
    apply Measure.ae_smul_measure (μ := Measure.dirac ((), (1 : ℝ)) + Measure.dirac ((), 3)) _ (2 : ℝ≥0∞)⁻¹
    norm_num [ae_add_measure_iff]
  have h := joint_empirical_probability_segment_derivative noisyData signFeature hy
    (N := 2) (by decide) (fun _ => 0) (fun _ => 1) (fun _ => hf 0) (fun _ => hf 1)
  dsimp only at h
  have hd := h.2.2.2
  let D : ℝ :=
    ((∫ q, 2 * ∫ z, ((∫ q, signFeature q z.1 ∂empiricalTwo (fun _ => 0))-z.2) * signFeature q z.1 ∂noisyData ∂empiricalTwo (fun _ => 1))-
     (∫ q, 2 * ∫ z, ((∫ q, signFeature q z.1 ∂empiricalTwo (fun _ => 0))-z.2) * signFeature q z.1 ∂noisyData ∂empiricalTwo (fun _ => 0)))
  change HasDerivWithinAt _ D _ _ at hd
  have hD : D = 4 := by
    dsimp only [D]
    norm_num [empiricalTwo_integral,noisyData_integral,signFeature]
  rw [hD] at hd
  exact hd

-- Width one keeps the exact empirical normalization and gives derivative -2.
example :
    let K : Fin 3 → Unit → ℝ := fun q _ => q.1
    let curve : ℝ → Measure (Fin 3) := fun t =>
      ENNReal.ofReal (1-t) • Measure.dirac 1 + ENNReal.ofReal t • Measure.dirac 2
    HasDerivWithinAt (fun t => ∫ z, ((∫ q, K q z.1 ∂curve t)-z.2)^2 ∂noisyData)
      (-2) (Set.Icc (0 : ℝ) 1) 0 := by
  dsimp only
  let K : Fin 3 → Unit → ℝ := fun q _ => q.1
  haveI : IsProbabilityMeasure (noisyData.map (Prod.fst : Unit × ℝ → Unit)) :=
    Measure.isProbabilityMeasure_map measurable_fst.aemeasurable
  have hf (q : Fin 3) : MemLp (K q) 2 (noisyData.map Prod.fst) := memLp_const _
  have hy : MemLp (fun z : Unit × ℝ => z.2) 2 noisyData := by
    apply MemLp.of_bound measurable_snd.aestronglyMeasurable 3
    apply Measure.ae_smul_measure (μ := Measure.dirac ((), (1 : ℝ)) + Measure.dirac ((), 3)) _ (2 : ℝ≥0∞)⁻¹
    norm_num [ae_add_measure_iff]
  have h := joint_empirical_probability_segment_derivative noisyData K hy
    (N := 1) (by decide) (fun _ => 1) (fun _ => 2) (fun _ => hf 1) (fun _ => hf 2)
  dsimp only at h
  have hd := h.2.2.2
  simp only [Fin.sum_univ_one,Nat.cast_one,inv_one,one_smul] at hd
  let V : Fin 3 → ℝ := fun q => 2 * ∫ z,
    ((∫ r, K r z.1 ∂Measure.dirac (1 : Fin 3))-z.2) * K q z.1 ∂noisyData
  change HasDerivWithinAt _ ((∫ q, V q ∂Measure.dirac (2 : Fin 3))-
    (∫ q, V q ∂Measure.dirac (1 : Fin 3))) _ _ at hd
  have hD : (∫ q, V q ∂Measure.dirac (2 : Fin 3))-
      (∫ q, V q ∂Measure.dirac (1 : Fin 3)) = -2 := by
    norm_num [V,K,noisyData_integral]
  rw [hD] at hd
  exact hd

private def plus : {w : ℝ // ‖w‖ = 1} := ⟨1, by norm_num⟩
private def minus : {w : ℝ // ‖w‖ = 1} := ⟨-1, by norm_num⟩
private def signLaw : Measure {w : ℝ // ‖w‖ = 1} :=
  (2 : ℝ≥0∞)⁻¹ • (Measure.dirac plus + Measure.dirac minus)
private instance : IsProbabilityMeasure signLaw := by
  apply isProbabilityMeasure_iff.mpr
  change (2 : ℝ≥0∞)⁻¹ * ((Measure.dirac plus + Measure.dirac minus : Measure _) Set.univ) = 1
  simp only [Measure.add_apply,measure_univ,one_add_one_eq_two]
  exact ENNReal.inv_mul_cancel (by norm_num) (by norm_num)

-- Non-even p(z)=z²+z: averaging opposite directions cancels its odd part.
example :
    ∃ hf : ∀ w : {w : ℝ // ‖w‖ = 1},
      MemLp (fun x : ℝ => (Polynomial.X^2+Polynomial.X : Polynomial ℝ).eval ⟪w.1,x⟫_ℝ) 2 (stdGaussian ℝ),
    ∃ hsq : MemLp (fun x : ℝ => x^2) 2 (stdGaussian ℝ),
      hsq.toLp (fun x : ℝ => x^2) =
        ∫ w, (hf w).toLp (fun x : ℝ => (Polynomial.X^2+Polynomial.X : Polynomial ℝ).eval ⟪w.1,x⟫_ℝ) ∂signLaw := by
  obtain ⟨hf,hc,havg⟩ := gaussian_polynomial_parameter_average_L2 (E := ℝ)
    (Polynomial.X^2+Polynomial.X)
  obtain ⟨_,_,hm,heq⟩ := havg signLaw inferInstance
  have raw (x : ℝ) : (∫ w : {w : ℝ // ‖w‖ = 1},
      (Polynomial.X^2+Polynomial.X : Polynomial ℝ).eval ⟪w.1,x⟫_ℝ ∂signLaw) = x^2 := by
    rw [signLaw,integral_smul_measure,
      integral_add_measure (integrable_dirac (by simp)) (integrable_dirac (by simp))]
    norm_num [plus,minus,Real.inner_apply,smul_eq_mul]
    ring
  simp only [raw] at hm heq
  exact ⟨hf,hm,heq⟩

-- Dimension zero needs no chosen direction for the actual continuity result.
example : ∃ hf : ∀ w : {w : EuclideanSpace ℝ (Fin 0) // ‖w‖ = 1},
    MemLp (fun x : EuclideanSpace ℝ (Fin 0) => (Polynomial.X : Polynomial ℝ).eval ⟪w.1,x⟫_ℝ) 2 (stdGaussian (EuclideanSpace ℝ (Fin 0))),
    Continuous (fun w => (hf w).toLp (fun x => (Polynomial.X : Polynomial ℝ).eval ⟪w.1,x⟫_ℝ)) :=
  continuous_gaussian_polynomial_ridge_L2 (Polynomial.X : Polynomial ℝ)

private def correlatedData : Measure (ℝ × ℝ) :=
  (stdGaussian ℝ).map (fun x : ℝ => (x,x))
private instance : IsProbabilityMeasure correlatedData :=
  Measure.isProbabilityMeasure_map (by fun_prop)
private theorem correlatedData_fst : correlatedData.map Prod.fst = stdGaussian ℝ := by
  rw [correlatedData,Measure.map_map (by fun_prop) (by fun_prop)]
  change Measure.map id (stdGaussian ℝ) = stdGaussian ℝ
  exact Measure.map_id
private theorem correlatedData_label : MemLp (fun z : ℝ × ℝ => z.2) 2 correlatedData := by
  apply (memLp_map_measure_iff (by fun_prop) (by fun_prop)).2
  exact IsGaussian.memLp_two_id
private def linearPredictor (rho : Measure {w : ℝ // ‖w‖ = 1}) (x : ℝ) : ℝ :=
  ∫ w, ⟪w.1,x⟫_ℝ ∂rho
private def linearRisk (rho : Measure {w : ℝ // ‖w‖ = 1}) : ℝ :=
  ∫ z, (linearPredictor rho z.1-z.2)^2 ∂correlatedData

-- The actual correlated label Y=X gives endpoint derivative -8 from -1 to +1.
example : HasDerivWithinAt
    (fun t : ℝ => linearRisk (ENNReal.ofReal (1-t) • Measure.dirac minus +
      ENNReal.ofReal t • Measure.dirac plus)) (-8) (Set.Icc (0 : ℝ) 1) 0 := by
  have h := gaussian_polynomial_joint_risk_first_variation correlatedData correlatedData_fst
    (Polynomial.X : Polynomial ℝ) correlatedData_label
  dsimp only at h
  have hc := h.2 (Measure.dirac minus) (Measure.dirac plus) inferInstance inferInstance
  simp only [Polynomial.eval_X] at hc
  have hd := hc.2.2.1
  let V : {w : ℝ // ‖w‖ = 1} → ℝ := fun w =>
    2 * ∫ z, (linearPredictor (Measure.dirac minus) z.1-z.2) * ⟪w.1,z.1⟫_ℝ ∂correlatedData
  have hp (x : ℝ) : linearPredictor (Measure.dirac minus) x = -x := by
    norm_num [linearPredictor,minus,Real.inner_apply]
  have hs : (∫ x : ℝ, x^2 ∂stdGaussian ℝ) = 1 := by
    have hh := (AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian (E := ℝ)).2
    simpa [Real.norm_eq_abs,sq_abs] using hh
  have hv (w : {w : ℝ // ‖w‖ = 1}) : V w = -4 * w.1 := by
    dsimp only [V]
    simp_rw [hp,Real.inner_apply]
    rw [correlatedData,integral_map (by fun_prop) (by fun_prop)]
    have hex : (fun x : ℝ => (-x-x) * (w.1*x)) = fun x => (-2*w.1) * x^2 := by funext x; ring
    rw [hex,integral_const_mul,hs]
    ring
  change HasDerivWithinAt _ ((∫ w, V w ∂Measure.dirac plus)-(∫ w, V w ∂Measure.dirac minus)) _ _ at hd
  norm_num only [integral_dirac,hv,plus,minus] at hd
  exact hd

-- A nonzero constant feature has zero probability-segment derivative.
example : HasDerivWithinAt
    (fun t : ℝ => ∫ z, ((∫ _ : {w : ℝ // ‖w‖ = 1}, (1 : ℝ)
      ∂(ENNReal.ofReal (1-t) • Measure.dirac minus + ENNReal.ofReal t • Measure.dirac plus))-z.2)^2
      ∂correlatedData) 0 (Set.Icc (0 : ℝ) 1) 0 := by
  have h := gaussian_polynomial_joint_risk_first_variation correlatedData correlatedData_fst
    (Polynomial.C (1 : ℝ)) correlatedData_label
  dsimp only at h
  have hd := (h.2 (Measure.dirac minus) (Measure.dirac plus) inferInstance inferInstance).2.2.1
  simpa only [Polynomial.eval_C,integral_dirac,sub_self] using hd

#print axioms quadratic_feature_probability_segment
#print axioms joint_empirical_probability_segment_derivative
#print axioms continuous_gaussian_polynomial_ridge_L2
#print axioms gaussian_polynomial_parameter_average_L2
#print axioms gaussian_polynomial_joint_risk_first_variation
end
end Tests.GaussianFeatureRegularity
