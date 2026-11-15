import AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap
import Mathlib.Topology.Algebra.Module.FiniteDimension

/-! Positive definiteness of the true probability mean. This author-derived
canonical background reuses the existing PSD integral node and proves strict
positivity separately for every nonzero quadratic-form test vector. Generic
integrability and AE-PD data must be derived internally by source consumers.
Empty finite matrix indices are allowed. -/

open MeasureTheory
open scoped Matrix.Norms.L2Operator
noncomputable section
universe u v
namespace AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveDefIntegral

theorem integral_posDef :
∀ {ι : Type u} {Ω : Type v} [Fintype ι] [DecidableEq ι] [MeasurableSpace Ω]
  {μ : Measure Ω} [IsProbabilityMeasure μ],
  ∀ (f : Ω → Matrix ι ι ℝ), Integrable f μ →
    (∀ᵐ ω ∂μ, (f ω).PosDef) → (∫ ω, f ω ∂μ).PosDef
 := by
  classical
  intro ι Ω _ _ _ μ _ f hf hpos
  have hpsd :=
    AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef
      f hf (hpos.mono fun _ h => h.posSemidef)
  apply Matrix.PosDef.of_dotProduct_mulVec_pos hpsd.isHermitian
  intro x hx
  let L : Matrix ι ι ℝ →ₗ[ℝ] ℝ :=
    { toFun := fun A => dotProduct (star x) (A.mulVec x)
      map_add' := by intro A B; simp [Matrix.add_mulVec, dotProduct_add]
      map_smul' := by intro c A; simp [Matrix.smul_mulVec, dotProduct_smul] }
  let φ : Matrix ι ι ℝ →L[ℝ] ℝ := L.toContinuousLinearMap
  have hfi : Integrable (fun ω => φ (f ω)) μ := φ.integrable_comp hf
  have hstrict : ∀ᵐ ω ∂μ, 0 < φ (f ω) := by
    filter_upwards [hpos] with ω hω
    exact hω.dotProduct_mulVec_pos hx
  have hnonneg : ∀ᵐ ω ∂μ, 0 ≤ φ (f ω) := hstrict.mono fun _ h => h.le
  have hintpos : 0 < ∫ ω, φ (f ω) ∂μ := by
    have hne : (∫ ω, φ (f ω) ∂μ) ≠ 0 := by
      intro hz
      have hzAE := (integral_eq_zero_iff_of_nonneg_ae hnonneg hfi).mp hz
      obtain ⟨ω, hωpos, hωzero⟩ := (hstrict.and hzAE).exists
      exact (ne_of_gt hωpos) hωzero
    exact lt_of_le_of_ne (integral_nonneg_of_ae hnonneg) (Ne.symm hne)
  rw [φ.integral_comp_comm hf] at hintpos
  exact hintpos

end AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveDefIntegral
