import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianIntegrationByParts
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialDifferentiation
import Mathlib.RingTheory.Polynomial.Hermite.Gaussian
import Mathlib.Analysis.Calculus.Deriv.Polynomial
import Mathlib.Tactic

open MeasureTheory ProbabilityTheory Polynomial
open scoped InnerProductSpace ENNReal

noncomputable section

namespace AutoSamplingTheory.TechnicalLemmas.Probability.GaussianHermiteGram

private def hermiteR (i : ℕ) : Polynomial ℝ :=
  (hermite i).map (algebraMap ℤ ℝ)

private theorem hermiteR_eval (i : ℕ) (t : ℝ) :
    (hermiteR i).eval t = aeval t (hermite i) := by
  rw [hermiteR, Polynomial.eval_map_algebraMap]

private theorem hermiteR_succ (i : ℕ) :
    hermiteR (i+1) = X * hermiteR i - (hermiteR i).derivative := by
  unfold hermiteR
  rw [hermite_succ, Polynomial.map_sub, Polynomial.map_mul, Polynomial.map_X,
    Polynomial.derivative_map]

private theorem hermiteR_degree_le (i : ℕ) : (hermiteR i).natDegree ≤ i := by
  calc
    (hermiteR i).natDegree ≤ (hermite i).natDegree := Polynomial.natDegree_map_le
    _ = i := natDegree_hermite

private theorem hermiteR_top_iterate_derivative (i : ℕ) :
    derivative^[i] (hermiteR i) = C (i.factorial : ℝ) := by
  ext m
  cases m with
  | zero =>
      simp [coeff_iterate_derivative, hermiteR, coeff_hermite_self, Nat.descFactorial_self]
  | succ m =>
      have hz : (hermiteR i).coeff (m+1+i) = 0 :=
        coeff_eq_zero_of_natDegree_lt ((hermiteR_degree_le i).trans_lt (by omega))
      rw [coeff_iterate_derivative]
      simp [hz]

section Ridges

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

private theorem ridge_L2 (p : Polynomial ℝ) (w : E) :
    MemLp (fun x => p.eval ⟪w,x⟫_ℝ) 2 (stdGaussian E) := by
  obtain ⟨hf, _⟩ :=
    GaussianPolynomialDifferentiation.actual_gaussian_polynomial_ridge_L2_frechet_derivative
      (E := E) p
  exact hf w

private theorem ridge_product_integrable (p q : Polynomial ℝ) (u v : E) :
    Integrable (fun x => p.eval ⟪u,x⟫_ℝ * q.eval ⟪v,x⟫_ℝ) (stdGaussian E) :=
  (ridge_L2 p u).integrable_mul (ridge_L2 q v)

private theorem hermite_adjoint_step (u v : E) (hu : ‖u‖ = 1)
    (i : ℕ) (q : Polynomial ℝ) :
    (∫ x, (hermiteR (i+1)).eval ⟪u,x⟫_ℝ * q.eval ⟪v,x⟫_ℝ ∂stdGaussian E) =
      ⟪u,v⟫_ℝ * ∫ x, (hermiteR i).eval ⟪u,x⟫_ℝ * q.derivative.eval ⟪v,x⟫_ℝ ∂stdGaussian E := by
  let p := hermiteR i
  let A : E → ℝ := fun x => p.eval ⟪u,x⟫_ℝ
  let B : E → ℝ := fun x => q.eval ⟪v,x⟫_ℝ
  let AD : E → ℝ := fun x => p.derivative.eval ⟪u,x⟫_ℝ
  let BD : E → ℝ := fun x => q.derivative.eval ⟪v,x⟫_ℝ
  let XB : E → ℝ := fun x => (X*p).eval ⟪u,x⟫_ℝ * B x
  let ρ := ⟪u,v⟫_ℝ
  let f : E → ℝ := fun x => A x * B x
  have hA (x : E) : HasFDerivAt A (AD x • innerSL ℝ u) x := by
    exact (p.hasDerivAt ⟪u,x⟫_ℝ).comp_hasFDerivAt x (innerSL ℝ u).hasFDerivAt
  have hB (x : E) : HasFDerivAt B (BD x • innerSL ℝ v) x := by
    exact (q.hasDerivAt ⟪v,x⟫_ℝ).comp_hasFDerivAt x (innerSL ℝ v).hasFDerivAt
  have hf (x : E) := (hA x).mul (hB x)
  have hf' : (fun x => fderiv ℝ f x u) = fun x => AD x * B x + ρ * (A x * BD x) := by
    funext x
    change fderiv ℝ (A * B) x u = _
    rw [(hf x).fderiv]
    simp only [ContinuousLinearMap.add_apply, ContinuousLinearMap.smul_apply, smul_eq_mul,
      innerSL_apply_apply, real_inner_self_eq_norm_sq, hu, one_pow, mul_one,
      real_inner_comm u v, ρ]
    ring
  have hx : (fun x => ⟪x,u⟫_ℝ * f x) = XB := by
    funext x
    rw [real_inner_comm u x]
    simp only [XB, f, A, eval_mul, eval_X, mul_assoc]
  have hi : Integrable XB (stdGaussian E) := ridge_product_integrable (X*p) q u v
  have hAd : Integrable (fun x => AD x * B x) (stdGaussian E) :=
    ridge_product_integrable p.derivative q u v
  have hBd : Integrable (fun x => A x * BD x) (stdGaussian E) :=
    ridge_product_integrable p q.derivative u v
  have hs := GaussianIntegrationByParts.standard_gaussian_stein_of_integrable_fderiv f u
    (fun x => (hf x).differentiableAt)
    (ridge_product_integrable p q u v) (hx.symm ▸ hi)
    (hf'.symm ▸ (hAd.add (hBd.const_mul ρ)))
  rw [hx, hf', integral_add hAd (hBd.const_mul ρ), integral_const_mul] at hs
  calc
    _ = ∫ x, XB x - AD x * B x ∂stdGaussian E := by
      apply integral_congr_ae
      filter_upwards with x
      rw [hermiteR_succ]
      simp only [p, B, AD, XB, eval_sub]
      ring
    _ = _ := by
      rw [integral_sub hi hAd]
      linarith only [hs]

private theorem hermite_adjoint_iterate (u v : E) (hu : ‖u‖ = 1)
    (i : ℕ) (q : Polynomial ℝ) :
    (∫ x, (hermiteR i).eval ⟪u,x⟫_ℝ * q.eval ⟪v,x⟫_ℝ ∂stdGaussian E) =
      ⟪u,v⟫_ℝ ^ i * ∫ x, (derivative^[i] q).eval ⟪v,x⟫_ℝ ∂stdGaussian E := by
  induction i generalizing q with
  | zero => simp [hermiteR, hermite_zero]
  | succ i ih =>
      rw [hermite_adjoint_step u v hu, ih q.derivative,
        Function.iterate_succ_apply, pow_succ]
      ring

private theorem hermite_gram_le (u v : E) (hu : ‖u‖ = 1)
    (i j : ℕ) (hji : j ≤ i) :
    (∫ x, (hermiteR i).eval ⟪u,x⟫_ℝ * (hermiteR j).eval ⟪v,x⟫_ℝ ∂stdGaussian E) =
      if i = j then (i.factorial : ℝ) * ⟪u,v⟫_ℝ ^ i else 0 := by
  rw [hermite_adjoint_iterate u v hu]
  by_cases h : i = j
  · subst j
    rw [hermiteR_top_iterate_derivative]
    simp [mul_comm]
  · have hn : (hermiteR j).natDegree < i :=
      (hermiteR_degree_le j).trans_lt (lt_of_le_of_ne hji (Ne.symm h))
    rw [iterate_derivative_eq_zero hn]
    simp [h]

end Ridges

theorem gaussian_hermite_ridge_gram
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (u v : E) (hu : ‖u‖ = 1) (hv : ‖v‖ = 1) (i j : ℕ) :
    let G : E → ℝ := fun x =>
      Polynomial.aeval ⟪u,x⟫_ℝ (Polynomial.hermite i) *
        Polynomial.aeval ⟪v,x⟫_ℝ (Polynomial.hermite j)
    Integrable G (stdGaussian E) ∧
      (∫ x, G x ∂stdGaussian E) =
        if i = j then (i.factorial : ℝ) * ⟪u,v⟫_ℝ ^ i else 0 := by
  dsimp only
  simp_rw [← hermiteR_eval]
  refine ⟨ridge_product_integrable (hermiteR i) (hermiteR j) u v, ?_⟩
  rcases le_total j i with h | h
  · exact hermite_gram_le u v hu i j h
  · have hc :
        (∫ x, (hermiteR i).eval ⟪u,x⟫_ℝ * (hermiteR j).eval ⟪v,x⟫_ℝ ∂stdGaussian E) =
        ∫ x, (hermiteR j).eval ⟪v,x⟫_ℝ * (hermiteR i).eval ⟪u,x⟫_ℝ ∂stdGaussian E := by
      apply integral_congr_ae
      exact Filter.Eventually.of_forall fun _ => mul_comm _ _
    rw [hc, hermite_gram_le v u hv j i h]
    by_cases hij : i = j
    · subst j
      simp [real_inner_comm u v]
    · simp [hij, Ne.symm hij]

#print axioms gaussian_hermite_ridge_gram

end AutoSamplingTheory.TechnicalLemmas.Probability.GaussianHermiteGram
