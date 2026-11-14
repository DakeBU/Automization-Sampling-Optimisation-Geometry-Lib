import AutoSamplingTheory.ExampleCases.GaussianComplexity.ProductDensity

open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal BigOperators
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity

/-! Genuine downstream integration consumers on the actual source prior and
Gaussian bind, for every allowed parameter and either common sign. -/

example {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ) {b : ℝ} (hb : b = 1 ∨ b = -1) :
    letI : MeasurableSpace (Matrix (Fin d) (Fin d) ℝ) := borel _
    let e : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
      ((Equiv.sumCongr
        ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
        (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
        (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
    let split : EuclideanSpace ℝ (Fin d) →
        (Fin (d / n) → EuclideanSpace ℝ (Fin n)) × EuclideanSpace ℝ (Fin (d % n)) :=
      fun x => (fun j => WithLp.toLp 2 (fun i => x (e (Sum.inl (i, j)))),
        WithLp.toLp 2 (fun i => x (e (Sum.inr i))))
    let ν := (2 : ℝ≥0∞) • (orthogonalHaar n).restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = b}
    let D := (Measure.pi (fun _ : Fin (d / n) => ν)).map (blockPrecision κ)
    let γ : Matrix (Fin d) (Fin d) ℝ → Measure (EuclideanSpace ℝ (Fin d)) :=
      fun A => multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹
    let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision κ O).det /
        (2 * Real.pi) ^ ((n : ℝ) / 2) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ
          (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
    let pb : EuclideanSpace ℝ (Fin n) → ℝ := fun x => ∫ O, p O x ∂ν
    let φ : EuclideanSpace ℝ (Fin (d % n)) → ℝ :=
      fun z => (2 * Real.pi) ^ (-((d % n : ℕ) : ℝ) / 2) * Real.exp (-‖z‖ ^ 2 / 2)
    let q : (Fin (d / n) → EuclideanSpace ℝ (Fin n)) ×
        EuclideanSpace ℝ (Fin (d % n)) → ℝ :=
      fun y => (∏ j, pb (y.1 j)) * φ y.2
    ∀ B : Set (EuclideanSpace ℝ (Fin d)), MeasurableSet B →
      (D.bind γ) B = ∫⁻ x in B, ENNReal.ofReal (q (split x)) := by
  classical
  have h := ProductDensity.actual_product_density hn hnd hκ hb
  dsimp only at h ⊢
  rcases h with ⟨hvol,h0,hm,hi,h1,hcoord,hambient,hunit⟩
  intro B hB
  rw [hambient, withDensity_apply _ hB]

example {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ) {b : ℝ} (hb : b = 1 ∨ b = -1) :
    letI : MeasurableSpace (Matrix (Fin d) (Fin d) ℝ) := borel _
    let e : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
      ((Equiv.sumCongr
        ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
        (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
        (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
    let split : EuclideanSpace ℝ (Fin d) →
        (Fin (d / n) → EuclideanSpace ℝ (Fin n)) × EuclideanSpace ℝ (Fin (d % n)) :=
      fun x => (fun j => WithLp.toLp 2 (fun i => x (e (Sum.inl (i, j)))),
        WithLp.toLp 2 (fun i => x (e (Sum.inr i))))
    let ν := (2 : ℝ≥0∞) • (orthogonalHaar n).restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = b}
    let D := (Measure.pi (fun _ : Fin (d / n) => ν)).map (blockPrecision κ)
    let γ : Matrix (Fin d) (Fin d) ℝ → Measure (EuclideanSpace ℝ (Fin d)) :=
      fun A => multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹
    let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision κ O).det /
        (2 * Real.pi) ^ ((n : ℝ) / 2) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ
          (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
    let pb : EuclideanSpace ℝ (Fin n) → ℝ := fun x => ∫ O, p O x ∂ν
    let φ : EuclideanSpace ℝ (Fin (d % n)) → ℝ :=
      fun z => (2 * Real.pi) ^ (-((d % n : ℕ) : ℝ) / 2) * Real.exp (-‖z‖ ^ 2 / 2)
    let q : (Fin (d / n) → EuclideanSpace ℝ (Fin n)) ×
        EuclideanSpace ℝ (Fin (d % n)) → ℝ :=
      fun y => (∏ j, pb (y.1 j)) * φ y.2
    ∀ B : Set ((Fin (d / n) → EuclideanSpace ℝ (Fin n)) ×
        EuclideanSpace ℝ (Fin (d % n))), MeasurableSet B →
      ((D.bind γ).map split) B = ∫⁻ y in B, ENNReal.ofReal (q y) := by
  classical
  have h := ProductDensity.actual_product_density hn hnd hκ hb
  dsimp only at h ⊢
  rcases h with ⟨hvol,h0,hm,hi,h1,hcoord,hambient,hunit⟩
  intro B hB
  rw [hcoord, withDensity_apply _ hB]

#print axioms ProductDensity.actual_product_density
