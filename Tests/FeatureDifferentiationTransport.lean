import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialDifferentiation
import AutoSamplingTheory.TechnicalLemmas.Geometry.QuadraticFeatureTangentGradient
import AutoSamplingTheory.TechnicalLemmas.Measure.BochnerMeanTransport

open MeasureTheory ProbabilityTheory
open scoped ENNReal InnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialDifferentiation
open AutoSamplingTheory.TechnicalLemmas.Geometry.QuadraticFeatureTangentGradient
open AutoSamplingTheory.TechnicalLemmas.Measure.BochnerMeanTransport
open AutoSamplingTheory.TechnicalLemmas.Measure.Transport

namespace Tests.FeatureDifferentiationTransport
noncomputable section

-- The odd part of p(z)=z²+z survives its actual derivative at the origin.
example :
    ∃ hf : ∀ w : ℝ, MemLp (fun x : ℝ => (w*x)^2+w*x) 2 (stdGaussian ℝ),
    ∃ hx : MemLp (fun x : ℝ => x) 2 (stdGaussian ℝ),
    ∃ D : ℝ →L[ℝ] Lp ℝ 2 (stdGaussian ℝ),
      HasFDerivAt (fun w => (hf w).toLp (fun x => (w*x)^2+w*x)) D 0 ∧
      D 1 = hx.toLp (fun x => x) := by
  obtain ⟨hf,hdf,D,hr,hd⟩ :=
    actual_gaussian_polynomial_ridge_L2_frechet_derivative (E := ℝ)
      (Polynomial.X^2+Polynomial.X)
  dsimp only at hf hdf hr hd
  simp only [Polynomial.eval_add,Polynomial.eval_pow,Polynomial.eval_X,Real.inner_apply] at hf hd
  have he : (fun x : ℝ => (Polynomial.X^2+Polynomial.X : Polynomial ℝ).derivative.eval
      ⟪(0 : ℝ),x⟫_ℝ * ⟪(1 : ℝ),x⟫_ℝ) = fun x : ℝ => x := by
    funext x
    norm_num [Real.inner_apply,Polynomial.derivative_add,Polynomial.derivative_pow]
  have hx : MemLp (fun x : ℝ => x) 2 (stdGaussian ℝ) := by simpa only [he] using hdf 0 1
  refine ⟨hf,hx,D 0,hd 0,?_⟩
  simpa only [he] using hr 0 1

-- The ambient domain is present even when its unit sphere is empty.
example : ∃ hf : ∀ w : EuclideanSpace ℝ (Fin 0),
    MemLp (fun x => (3 : ℝ)) 2 (stdGaussian (EuclideanSpace ℝ (Fin 0))),
    ∃ D : EuclideanSpace ℝ (Fin 0) → EuclideanSpace ℝ (Fin 0) →L[ℝ]
      Lp ℝ 2 (stdGaussian (EuclideanSpace ℝ (Fin 0))),
      ∀ w, HasFDerivAt (fun u => (hf u).toLp (fun _ => (3 : ℝ))) (D w) w := by
  obtain ⟨hf,hdf,D,_,hd⟩ :=
    actual_gaussian_polynomial_ridge_L2_frechet_derivative
      (E := EuclideanSpace ℝ (Fin 0)) (Polynomial.C (3 : ℝ))
  dsimp only at hf hd
  simp only [Polynomial.eval_C] at hf hd
  exact ⟨hf,D,hd⟩

-- The produced bounds act on the same genuine derivative at opposite endpoints.
example : ∃ hf : ∀ w : ℝ,
    MemLp (fun x : ℝ => (w*x)^2+w*x) 2 (stdGaussian ℝ),
    ∃ D : ℝ → ℝ →L[ℝ] Lp ℝ 2 (stdGaussian ℝ),
    ∃ M₁ M₂ : ℝ, 0 < M₁ ∧ 0 < M₂ ∧
      HasFDerivAt (fun w => (hf w).toLp (fun x => (w*x)^2+w*x)) (D 0) 0 ∧
      ‖D 0‖ ≤ M₁ ∧ ‖D 1-D (-1)‖ ≤ 2*M₂ := by
  obtain ⟨hf,hdf,D,_,hd,M₁,M₂,h₁,h₂,hb,hl⟩ :=
    actual_gaussian_polynomial_ridge_L2_derivative_bounds (E := ℝ)
      (Polynomial.X^2+Polynomial.X)
  dsimp only at hf hd hb hl
  simp only [Polynomial.eval_add,Polynomial.eval_pow,Polynomial.eval_X,Real.inner_apply] at hf hd
  refine ⟨hf,D,M₁,M₂,h₁,h₂,hd 0,hb 0 (by norm_num),?_⟩
  have hh := hl (-1) 1 (by norm_num) (by norm_num)
  norm_num [mul_comm] at hh
  simpa only [mul_comm M₂ (2 : ℝ)] using hh

-- An actual identity feature has D=id; its tangent field is the concrete projection.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    (r q w u : E) (hw : ‖w‖ = 1) (hu : ‖u‖ = 1) :
    ⟪w,(2 : ℝ) • (r-⟪r,w⟫_ℝ • w)⟫_ℝ = 0 ∧
    ‖(2 : ℝ) • (r-⟪r,w⟫_ℝ • w)-(2 : ℝ) • (q-⟪q,u⟫_ℝ • u)‖ ≤
      2*‖r-q‖+4*‖q‖*‖w-u‖ := by
  have h := quadratic_feature_potential_tangent_gradient (fun z : E => z)
    (fun _ => ContinuousLinearMap.id ℝ E) (fun _ => hasFDerivAt_id _)
    1 0 (by norm_num) (by norm_num)
    (fun _ _ => ContinuousLinearMap.norm_id_le)
    (fun _ _ _ _ => by simp)
  dsimp only at h
  have hh := And.intro (h.2.1 r w hw).1 (h.2.2 r q w u hw hu)
  norm_num [ContinuousLinearMap.adjoint_id] at hh
  exact hh

private def bitFeature (b : Bool) : ℝ := if b then 1 else 0
private def bitCost (z : Bool × Bool) : ℝ := if z.1=z.2 then 0 else 1
private theorem bitBounds (b : Bool) : ‖bitFeature b‖ ≤ (1 : ℝ) := by cases b <;> norm_num [bitFeature]
private theorem bitLip (b d : Bool) : ‖bitFeature b-bitFeature d‖ ≤ (1 : ℝ)*bitCost (b,d) := by
  cases b <;> cases d <;> norm_num [bitFeature,bitCost]

-- Exact positive transport cost: two different Dirac laws, not an assumed optimizer.
example : transportCost (fun z => ENNReal.ofReal ((bitCost z)^2))
    (Measure.dirac false) (Measure.dirac true) = 1 := by
  let cost : Bool × Bool → ℝ≥0∞ := fun z => ENNReal.ofReal ((bitCost z)^2)
  let Q := transportCost cost (Measure.dirac false) (Measure.dirac true)
  have h := bounded_bochner_mean_quadratic_transport_control bitFeature
    (measurable_of_finite _).stronglyMeasurable 1 1 1 (by norm_num) (by norm_num) (by norm_num)
    bitBounds bitCost (measurable_of_finite _)
    (fun z => by unfold bitCost;split_ifs <;> norm_num)
    (fun z => by unfold bitCost;split_ifs <;> norm_num) bitLip
    (Measure.dirac false) (Measure.dirac true)
  dsimp only at h
  have hlo : 1 ≤ (Q ^ (1 / 2 : ℝ)).toReal := by
    simpa [Q,cost,bitFeature] using h.2.2.2.1
  have hpow : ((Q ^ (1 / 2 : ℝ)).toReal)^2 = Q.toReal := by
    rw [← ENNReal.toReal_pow,← ENNReal.rpow_two,← ENNReal.rpow_mul]
    norm_num
  have hlower : (1 : ℝ) ≤ Q.toReal := by nlinarith
  have hupper : Q ≤ 1 := by
    have hh := transportCost_le_lintegral_of_isCoupling cost
      (Measure.dirac false) (Measure.dirac true)
      ((Measure.dirac false).prod (Measure.dirac true))
      (isCoupling_prod (Measure.dirac false) (Measure.dirac true))
    simpa [Q,cost,bitCost,Measure.dirac_prod_dirac] using hh
  apply le_antisymm hupper
  exact (ENNReal.toReal_le_toReal (by norm_num) h.2.2.1).mp (by simpa using hlower)

-- L=0 is a genuine admitted case and forces equal feature means without dividing by L.
example : ‖(∫ _ : Bool, (7 : ℝ) ∂Measure.dirac false)-
    (∫ _ : Bool, (7 : ℝ) ∂Measure.dirac true)‖ ≤ 0 := by
  have h := bounded_bochner_mean_quadratic_transport_control (fun _ : Bool => (7 : ℝ))
    stronglyMeasurable_const 7 1 0 (by norm_num) (by norm_num) (by norm_num)
    (fun _ => by norm_num) bitCost (measurable_of_finite _)
    (fun z => by unfold bitCost;split_ifs <;> norm_num)
    (fun z => by unfold bitCost;split_ifs <;> norm_num)
    (fun _ _ => by simp) (Measure.dirac false) (Measure.dirac true)
  simpa only [zero_mul] using h.2.2.2.1

#print axioms actual_gaussian_polynomial_ridge_L2_frechet_derivative
#print axioms actual_gaussian_polynomial_ridge_L2_derivative_bounds
#print axioms quadratic_feature_potential_tangent_gradient
#print axioms bounded_bochner_mean_quadratic_transport_control
end
end Tests.FeatureDifferentiationTransport
