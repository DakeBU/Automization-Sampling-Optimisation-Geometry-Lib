import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialGradient
open MeasureTheory ProbabilityTheory
open scoped InnerProductSpace ENNReal
noncomputable section

-- Linear Gaussian features: the literal potential has an actual ambient gradient.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (P : Measure (E × ℝ)) [IsProbabilityMeasure P]
    (hPX : P.map Prod.fst = stdGaussian E)
    (hy : MemLp (fun z : E × ℝ => z.2) 2 P)
    (μ : Measure {w : E // ‖w‖ = 1}) [IsProbabilityMeasure μ] (w : E) :
    let predictor : E → ℝ := fun x => ∫ u, ⟪u.1,x⟫_ℝ ∂μ
    let V : E → ℝ := fun v => 2 * ∫ z, (predictor z.1-z.2)*⟪v,z.1⟫_ℝ ∂P
    Integrable (fun z : E × ℝ => (predictor z.1-z.2)*⟪w,z.1⟫_ℝ) P ∧
      HasGradientAt V (gradient V w) w := by
  obtain ⟨C₁,C₂,hC₁,hC₂,hpoint,hlaw⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialGradient.gaussian_polynomial_joint_potential_projected_gradient_transport_control
      P hPX Polynomial.X hy
  simpa only [Polynomial.eval_X] using (hpoint μ inferInstance).1 w

-- The same actual linear features obey the joint law/point estimate.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (P : Measure (E × ℝ)) [IsProbabilityMeasure P]
    (hPX : P.map Prod.fst = stdGaussian E)
    (hy : MemLp (fun z : E × ℝ => z.2) 2 P) :
    let S := {w : E // ‖w‖ = 1}
    let V : Measure S → E → ℝ := fun μ w =>
      2 * ∫ z, ((∫ u, ⟪u.1,z.1⟫_ℝ ∂μ)-z.2)*⟪w,z.1⟫_ℝ ∂P
    let G : Measure S → E → E := fun μ w =>
      gradient (V μ) w-⟪gradient (V μ) w,w⟫_ℝ • w
    let c : S × S → ℝ := fun z => Real.arccos ⟪z.1.1,z.2.1⟫_ℝ
    let Q : Measure S → Measure S → ℝ≥0∞ := fun μ ν =>
      AutoSamplingTheory.TechnicalLemmas.Measure.Transport.transportCost
        (fun z => ENNReal.ofReal ((c z)^2)) μ ν
    ∃ C : ℝ, 0 < C ∧ ∀ μ ν : Measure S,
      IsProbabilityMeasure μ → IsProbabilityMeasure ν → Q μ ν ≠ ∞ ∧
        ∀ w u : S, ‖G μ w.1-G ν u.1‖ ≤
          C*((Q μ ν ^ (1 / 2 : ℝ)).toReal+c (w,u)) := by
  obtain ⟨C₁,C₂,hC₁,hC₂,hpoint,hlaw⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialGradient.gaussian_polynomial_joint_potential_projected_gradient_transport_control
      P hPX Polynomial.X hy
  refine ⟨C₂,hC₂,?_⟩
  simpa only [Polynomial.eval_X] using hlaw

-- Zero features are allowed without a nontrivial ambient space or nonzero derivative.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (P : Measure (E × ℝ)) [IsProbabilityMeasure P]
    (hPX : P.map Prod.fst = stdGaussian E)
    (hy : MemLp (fun z : E × ℝ => z.2) 2 P)
    (μ : Measure {w : E // ‖w‖ = 1}) [IsProbabilityMeasure μ] (w : E) :
    HasGradientAt (fun _ : E => (0 : ℝ))
      (gradient (fun _ : E => (0 : ℝ)) w) w := by
  obtain ⟨C₁,C₂,hC₁,hC₂,hpoint,hlaw⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialGradient.gaussian_polynomial_joint_potential_projected_gradient_transport_control
      P hPX (0 : Polynomial ℝ) hy
  simpa only [Polynomial.eval_zero, mul_zero, integral_zero] using
    ((hpoint μ inferInstance).1 w).2
