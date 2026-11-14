import AutoSamplingTheory.ExampleCases.GaussianComplexity.AveragedBlockLaw
open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.AveragedBlockLaw
set_option autoImplicit false

-- Actual all-source-parameter marginal laws under the literal matrix prior.
example {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ) {b : ℝ} (hb : b = 1 ∨ b = -1) (j : Fin (d / n)) :
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
    let P := ν.bind (fun O => multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
      (singleBlockPrecision κ O)⁻¹)
    (D.bind γ).map (fun x => (split x).1 j) = P ∧
      (D.bind γ).map (fun x => (split x).2) =
        stdGaussian (EuclideanSpace ℝ (Fin (d % n))) := by
  classical
  dsimp only
  let : MeasurableSpace (Matrix (Fin d) (Fin d) ℝ) := borel _
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
  let P := ν.bind (fun O => multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
    (singleBlockPrecision κ O)⁻¹)
  let R := stdGaussian (EuclideanSpace ℝ (Fin (d % n)))
  have h := actual_averaged_block_product hn hnd hκ hb
  change IsProbabilityMeasure D ∧ (∀ᵐ A ∂D, A.PosDef) ∧ IsProbabilityMeasure P ∧
    IsProbabilityMeasure (D.bind γ) ∧ (D.bind γ).map split =
      (Measure.pi (fun _ : Fin (d / n) => P)).prod R at h
  let : IsProbabilityMeasure P := h.2.2.1
  have hsplit : Measurable split := by dsimp only [split]; fun_prop
  change (D.bind γ).map (fun x => (split x).1 j) = P ∧
    (D.bind γ).map (fun x => (split x).2) = R
  constructor
  · have hm : (D.bind γ).map (fun x => (split x).1 j) =
        (((D.bind γ).map split).map Prod.fst).map (Function.eval j) := by
      rw [Measure.map_map (measurable_pi_apply j) measurable_fst,
        Measure.map_map ((measurable_pi_apply j).comp measurable_fst) hsplit]
      rfl
    rw [hm, h.2.2.2.2, Measure.map_fst_prod]
    simp only [measure_univ, one_smul]
    exact (measurePreserving_eval (μ := fun _ : Fin (d / n) => P) j).map_eq
  · rw [show (D.bind γ).map (fun x => (split x).2) = ((D.bind γ).map split).map Prod.snd by
      rw [Measure.map_map measurable_snd hsplit]; rfl, h.2.2.2.2, Measure.map_snd_prod]
    simp

#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.AveragedBlockLaw.actual_averaged_block_product
