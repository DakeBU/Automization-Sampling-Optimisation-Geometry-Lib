import AutoSamplingTheory.ExampleCases.GaussianComplexity.PoissonNormalization
open Matrix MeasureTheory
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.ColumnTransport
set_option autoImplicit false
/-!
Actual full-Haar first-column law and selected Gaussian integral transport.
This is the bounded source-implicit adapter preceding Appendix A.1 in the
proof of Zhou--Suzuki arXiv:2610.20492v1 B.7. It does not identify canonical
normalized surface measure or evaluate either Poisson integral.
-/
theorem selected_column_transport {n : ℕ} (hn : 3 ≤ n) {κ : ℝ}
    (hκ : 4 ≤ κ) :
    let s : ℝ := Real.sqrt κ
    let r : ℝ := (1 - 1 / (n : ℝ)) * ((s - 1) / (s + 1))
    let ℓ : ℝ := (4 * (n : ℝ) * s + (s - 1) ^ 2) /
      (8 * (n : ℝ) * ((n : ℝ) - 1))
    let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
    let c : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) :=
      fun O => WithLp.toLp 2 (fun i => (O : Matrix (Fin n) (Fin n) ℝ) i j0)
    let ν : Measure (EuclideanSpace ℝ (Fin n)) := (orthogonalHaar n).map c
    let f : EuclideanSpace ℝ (Fin n) → ℝ := fun y =>
      ((s + 1) * WithLp.ofLp y j0 - (s - 1)) /
        (1 + r ^ 2 - 2 * r * WithLp.ofLp y j0) ^ ((n : ℝ) / 2)
    let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
      fun O => ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ O)⁻¹
    IsProbabilityMeasure ν ∧
      (∀ᵐ y ∂ν, ‖y‖ = 1) ∧
      (∀ Q : Matrix.orthogonalGroup (Fin n) ℝ,
        ν.map (fun y => Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n) (Q : Matrix (Fin n) (Fin n) ℝ) y) = ν) ∧
      Integrable f ν ∧
      (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        (O : Matrix (Fin n) (Fin n) ℝ).det *
          (∫ x : EuclideanSpace ℝ (Fin n), Real.exp (-ℓ * ‖x‖ ^ 2) ∂γ O)
        ∂orthogonalHaar n) =
        (((-1 : ℝ) ^ (n - 1) * (s - 1) ^ (n - 1)) / (s + 1) ^ n) *
          (1 - 1 / (n : ℝ)) ^ ((n : ℝ) / 2) * (∫ y, f y ∂ν) := by
  classical
  let s : ℝ := Real.sqrt κ
  let r : ℝ := (1 - 1 / (n : ℝ)) * ((s - 1) / (s + 1))
  let ℓ : ℝ := (4 * (n : ℝ) * s + (s - 1) ^ 2) /
    (8 * (n : ℝ) * ((n : ℝ) - 1))
  let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
  let c : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) :=
    fun O => WithLp.toLp 2 (fun i => (O : Matrix (Fin n) (Fin n) ℝ) i j0)
  let ν : Measure (EuclideanSpace ℝ (Fin n)) := (orthogonalHaar n).map c
  let f : EuclideanSpace ℝ (Fin n) → ℝ := fun y =>
    ((s + 1) * WithLp.ofLp y j0 - (s - 1)) /
      (1 + r ^ 2 - 2 * r * WithLp.ofLp y j0) ^ ((n : ℝ) / 2)
  let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
    fun O => ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
      (singleBlockPrecision κ O)⁻¹
  change IsProbabilityMeasure ν ∧ (∀ᵐ y ∂ν, ‖y‖ = 1) ∧
    (∀ Q : Matrix.orthogonalGroup (Fin n) ℝ,
      ν.map (fun y => Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n)
        (Q : Matrix (Fin n) (Fin n) ℝ) y) = ν) ∧ Integrable f ν ∧ _
  have hc : Continuous c :=
    (PiLp.continuous_toLp 2 (fun _ : Fin n => ℝ)).comp
      (continuous_pi (fun i => continuous_subtype_val.matrix_elem i j0))
  have hf : Measurable f := by dsimp [f]; fun_prop
  let := (orthogonalHaar_spec n).1
  have hprob : IsProbabilityMeasure ν := Measure.isProbabilityMeasure_map hc.measurable.aemeasurable
  have hnorm (O : Matrix.orthogonalGroup (Fin n) ℝ) : ‖c O‖ = 1 := by
    have hu := Unitary.map_mem (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n)) O.property
    have hh := ContinuousLinearMap.norm_map_of_mem_unitary hu (PiLp.single 2 j0 (1 : ℝ))
    have he : Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n)
        (O : Matrix (Fin n) (Fin n) ℝ) (PiLp.single 2 j0 (1 : ℝ)) = c O := by
      apply (WithLp.equiv 2 (Fin n → ℝ)).injective
      change (O : Matrix (Fin n) (Fin n) ℝ) *ᵥ Pi.single j0 1 = fun i =>
        (O : Matrix (Fin n) (Fin n) ℝ) i j0
      rw [Matrix.mulVec_single_one]
      rfl
    rw [he] at hh
    simpa [PiLp.norm_single] using hh
  have hsphere : ∀ᵐ y ∂ν, ‖y‖ = 1 :=
    (ae_map_iff hc.measurable.aemeasurable
      (isClosed_eq continuous_norm continuous_const).measurableSet).2
        (Filter.Eventually.of_forall hnorm)
  have hinvariant (Q : Matrix.orthogonalGroup (Fin n) ℝ) :
      ν.map (fun y => Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n)
        (Q : Matrix (Fin n) (Fin n) ℝ) y) = ν := by
    let T := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin n)
      (Q : Matrix (Fin n) (Fin n) ℝ)
    have heq : (fun y => T y) ∘ c = c ∘ (fun O => Q * O) := by
      funext O
      apply (WithLp.equiv 2 (Fin n → ℝ)).injective
      ext i
      simp [T, c, Matrix.mul_apply, Matrix.mulVec, dotProduct]
    change ((orthogonalHaar n).map c).map (fun y => T y) = (orthogonalHaar n).map c
    rw [Measure.map_map T.continuous.measurable hc.measurable, heq,
      ← Measure.map_map hc.measurable (measurable_const_mul Q), orthogonalHaar_map_mul_left]
  have hp := PoissonNormalization.selected_gaussian_normalization hn hκ
  change Integrable (f ∘ c) (orthogonalHaar n) ∧ _ at hp
  have hL : Integrable f ν :=
    (integrable_map_measure hf.aestronglyMeasurable hc.measurable.aemeasurable).2 hp.1
  refine ⟨hprob, hsphere, hinvariant, hL, ?_⟩
  rw [integral_map hc.measurable.aemeasurable hL.aestronglyMeasurable]
  exact hp.2

end AutoSamplingTheory.ExampleCases.GaussianComplexity.ColumnTransport
