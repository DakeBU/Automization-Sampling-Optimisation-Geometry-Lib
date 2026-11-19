import B2JointLaw
import HaarOrientedSection
import ParameterizedPushforward

/-!
The single-observation conditional laws in Appendix B.1, Lemma B.2 of
Zhou–Suzuki, arXiv:2610.20492v1. The exact composition-product equations
specify a regular conditional distribution. In the inverse experiment,
the second coordinate is the transpose of the original draw.
-/

open Matrix MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarOrientedSection
open AutoSamplingTheory.TechnicalLemmas.Probability.ParameterizedPushforward

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional

set_option autoImplicit false

private theorem map_fiber_eq_one {A B V : Type*} [MeasurableSpace A]
    [MeasurableSpace B] [MeasurableSpace V] [MeasurableSingletonClass A]
    (ν : Measure V) [IsProbabilityMeasure ν] {obs : B → A} (hobs : Measurable obs)
    (z : A) {reconstruct : V → B} (hr : Measurable reconstruct)
    (h : ∀ v, obs (reconstruct v) = z) :
    ν.map reconstruct {W | obs W = z} = 1 := by
  have hs : MeasurableSet {W | obs W = z} := hobs (measurableSet_singleton z)
  have hpre : reconstruct ⁻¹' {W | obs W = z} = Set.univ := by
    ext v
    exact iff_of_true (h v) (Set.mem_univ v)
  rw [Measure.map_apply hr hs, hpre, measure_univ]

set_option maxHeartbeats 600000 in
/-- For either observation direction, the actual spherical marginal and a
pointwise version of the regular conditional law are given by the uniform
sphere and the independent Haar residual block of the same sign. -/
theorem component_conditional_law (n : ℕ) :
    let σ := sphereProbability (n + 2)
    ∃ Q : S (n + 2) → O (n + 2), Measurable Q ∧
      (∀ z, (Q z).val.det = 1 ∧
        (Q z).val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = WithLp.ofLp z.val) ∧
      ∀ (b : ℝ), b = -1 ∨ b = 1 → ∀ (u : S (n + 2)),
        let μ := componentHaar (n + 2) b
        let ν := componentHaar (n + 1) b
        ∃ κ : Kernel (S (n + 2)) (O (n + 2)), IsMarkovKernel κ ∧
          (∀ z, κ z = ν.map (assemble Q u z)) ∧
          (∀ z, κ z {W | rotate W u = z} = 1) ∧
          μ.map (fun W => rotate W u) = σ ∧
          μ.map (fun W => rotate W⁻¹ u) = σ ∧
          μ.map (fun W => (rotate W u, W)) = σ ⊗ₘ κ ∧
          μ.map (fun W => (rotate W⁻¹ u, W⁻¹)) = σ ⊗ₘ κ := by
  obtain ⟨Q, hQ, hcols⟩ := exists_measurable_oriented_section n
  refine ⟨Q, hQ, hcols, ?_⟩
  intro b hb u
  let : NeZero (n + 2) := ⟨by omega⟩
  let := isProbabilityMeasure_sphereProbability (n + 2)
  let := isProbabilityMeasure_componentHaar (n := n + 1) (by omega) hb
  let σ := sphereProbability (n + 2)
  let μ := componentHaar (n + 2) b
  let ν := componentHaar (n + 1) b
  let κ := kernel ν (assemble Q u)
  have hF := measurable_assemble hQ u
  have hκ : IsMarkovKernel κ := isMarkovKernel_kernel ν (assemble Q u) hF
  let := hκ
  have hAt (z : S (n + 2)) : κ z = ν.map (assemble Q u z) :=
    kernel_apply ν (assemble Q u) hF z
  have hJoint := component_observation_joint_law_of_section n b u Q hQ
    (fun z => (hcols z).2) (fun z => (hcols z).1)
  have hComp : (σ.prod ν).map (fun p : S (n + 2) × O (n + 1) =>
      (p.1, assemble Q u p.1 p.2)) = σ ⊗ₘ κ :=
    map_prod_eq_compProd σ ν (assemble Q u) hF
  have hf : μ.map (fun W => (rotate W u, W)) = σ ⊗ₘ κ := hJoint.1.trans hComp
  have hi : μ.map (fun W => (rotate W⁻¹ u, W⁻¹)) = σ ⊗ₘ κ := hJoint.2.trans hComp
  have hmf : μ.map (fun W => rotate W u) = σ := by
    calc
      _ = (μ.map (fun W => (rotate W u, W))).fst :=
        (Measure.fst_map_prodMk (Y := id) measurable_id).symm
      _ = σ := by rw [hf, Measure.fst_compProd]
  have hmi : μ.map (fun W => rotate W⁻¹ u) = σ := by
    calc
      _ = (μ.map (fun W => (rotate W⁻¹ u, W⁻¹))).fst :=
        (Measure.fst_map_prodMk (Y := Inv.inv) measurable_inv).symm
      _ = σ := by rw [hi, Measure.fst_compProd]
  have hobs : Measurable (fun W : O (n + 2) => rotate W u) :=
    (continuous_rotate.comp (continuous_id.prodMk continuous_const)).measurable
  have hSupport (z : S (n + 2)) : κ z {W | rotate W u = z} = 1 := by
    have hFz : Measurable (assemble Q u z) := hF.of_uncurry_left
    rw [hAt z]
    exact map_fiber_eq_one ν hobs z hFz (assemble_rotate (fun z =>
      (first_column_iff_rotate_coordinate 0 _ z).mp (hcols z).2) u z)
  exact ⟨κ, hκ, hAt, hSupport, hmf, hmi, hf, hi⟩

#print axioms component_conditional_law
#check component_conditional_law 0

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
