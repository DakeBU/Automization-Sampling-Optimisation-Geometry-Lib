import AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianBlockLaw

open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianBlockLaw

set_option autoImplicit false

-- The complete coordinate contract, including all division/remainder endpoints.
example (d n : ℕ) :
    let e : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
      ((Equiv.sumCongr
        ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
        (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
        (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
    (∀ (i : Fin n) (j : Fin (d / n)),
      (e (Sum.inl (i, j))).val = j.val * n + i.val) ∧
    (∀ i : Fin (d % n), (e (Sum.inr i)).val = (d / n) * n + i.val) ∧
    d % n = d - (d / n) * n := by
  dsimp only
  constructor
  · intro i j
    simp [finProdFinEquiv, finSumFinEquiv, Nat.mul_comm, Nat.add_comm]
  constructor
  · intro i
    simp [finProdFinEquiv, finSumFinEquiv, Nat.mul_comm]
  · have hd := Nat.div_add_mod d n
    rw [Nat.mul_comm] at hd
    omega

-- The split has the actual inverse assembly, including empty blocks/tails.
example (d n : ℕ) :
    let e : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
      ((Equiv.sumCongr
        ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
        (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
        (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
    let split : EuclideanSpace ℝ (Fin d) →
        (Fin (d / n) → EuclideanSpace ℝ (Fin n)) × EuclideanSpace ℝ (Fin (d % n)) :=
      fun x => (fun j => WithLp.toLp 2 (fun i => x (e (Sum.inl (i, j)))),
        WithLp.toLp 2 (fun i => x (e (Sum.inr i))))
    Function.Bijective split := by
  classical
  dsimp only
  let e : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
    ((Equiv.sumCongr
      ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
      (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
      (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
  let split : EuclideanSpace ℝ (Fin d) →
      (Fin (d / n) → EuclideanSpace ℝ (Fin n)) × EuclideanSpace ℝ (Fin (d % n)) :=
    fun x => (fun j => WithLp.toLp 2 (fun i => x (e (Sum.inl (i, j)))),
      WithLp.toLp 2 (fun i => x (e (Sum.inr i))))
  let join (y : (Fin (d / n) → EuclideanSpace ℝ (Fin n)) ×
      EuclideanSpace ℝ (Fin (d % n))) : EuclideanSpace ℝ (Fin d) :=
    WithLp.toLp 2 (fun i => Sum.elim (fun ij => y.1 ij.2 ij.1) (fun a => y.2 a) (e.symm i))
  have hleft : Function.LeftInverse join split := by
    intro x
    ext i
    change Sum.elim (fun ij => (split x).1 ij.2 ij.1)
      (fun a => (split x).2 a) (e.symm i) = x i
    calc
      _ = x (e (e.symm i)) := by cases e.symm i <;> rfl
      _ = x i := by rw [e.apply_symm_apply]
  have hright : Function.RightInverse join split := by
    intro y
    ext j i <;> simp [split, join]
  exact ⟨hleft.injective, hright.surjective⟩

-- A genuine consumer: both actual block and residual Gaussian marginals,
-- for every source parameter and every fixed tuple, without any sign condition.
example {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d) {κ : ℝ} (hκ : 4 ≤ κ)
    (O : Fin (d / n) → Matrix.orthogonalGroup (Fin n) ℝ) (j : Fin (d / n)) :
    let e : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
      ((Equiv.sumCongr
        ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
        (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
        (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
    let split : EuclideanSpace ℝ (Fin d) →
        (Fin (d / n) → EuclideanSpace ℝ (Fin n)) × EuclideanSpace ℝ (Fin (d % n)) :=
      fun x => (fun j => WithLp.toLp 2 (fun i => x (e (Sum.inl (i, j)))),
        WithLp.toLp 2 (fun i => x (e (Sum.inr i))))
    (multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) (blockPrecision κ O)⁻¹).map
        (fun x => (split x).1 j) =
      multivariateGaussian (0 : EuclideanSpace ℝ (Fin n)) (singleBlockPrecision κ (O j))⁻¹ ∧
    (multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) (blockPrecision κ O)⁻¹).map
        (fun x => (split x).2) = stdGaussian (EuclideanSpace ℝ (Fin (d % n))) := by
  classical
  dsimp only
  let e : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
    ((Equiv.sumCongr
      ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
      (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
      (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
  let split : EuclideanSpace ℝ (Fin d) →
      (Fin (d / n) → EuclideanSpace ℝ (Fin n)) × EuclideanSpace ℝ (Fin (d % n)) :=
    fun x => (fun j => WithLp.toLp 2 (fun i => x (e (Sum.inl (i, j)))),
      WithLp.toLp 2 (fun i => x (e (Sum.inr i))))
  let μ := multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) (blockPrecision κ O)⁻¹
  let ν (i : Fin (d / n)) := multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
    (singleBlockPrecision κ (O i))⁻¹
  let ρ := stdGaussian (EuclideanSpace ℝ (Fin (d % n)))
  have hs : Measurable split := by dsimp only [split]; fun_prop
  have h := actual_conditional_block_product hn hnd hκ O
  change μ.map split = (Measure.pi ν).prod ρ at h
  change μ.map (fun x => (split x).1 j) = ν j ∧ μ.map (fun x => (split x).2) = ρ
  constructor
  · have hm : μ.map (fun x => (split x).1 j) =
        ((μ.map split).map Prod.fst).map (Function.eval j) := by
      rw [Measure.map_map (measurable_pi_apply j) measurable_fst,
        Measure.map_map ((measurable_pi_apply j).comp measurable_fst) hs]
      rfl
    rw [hm, h, Measure.map_fst_prod]
    simp only [measure_univ, one_smul]
    exact (measurePreserving_eval (μ := ν) j).map_eq
  · rw [show μ.map (fun x => (split x).2) = (μ.map split).map Prod.snd by
      rw [Measure.map_map measurable_snd hs]; rfl, h, Measure.map_snd_prod]
    simp

-- Actual zero-dimensional Gaussian is the probability point mass, not zero measure.
example : stdGaussian (EuclideanSpace ℝ (Fin 0)) = Measure.dirac 0 := by
  ext s hs
  by_cases h : (0 : EuclideanSpace ℝ (Fin 0)) ∈ s
  · have hsu : s = Set.univ := by
      ext x
      simp only [Set.mem_univ, iff_true]
      simpa only [Subsingleton.elim x 0] using h
    simp [hsu]
  · have hse : s = ∅ := by
      ext x
      simp only [Set.mem_empty_iff_false, iff_false]
      simpa only [Subsingleton.elim x 0] using h
    simp [hse]

#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianBlockLaw.actual_conditional_block_product
