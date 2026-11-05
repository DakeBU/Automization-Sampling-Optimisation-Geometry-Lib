import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.CompactGradientSqrtPerturbation
import Mathlib.Analysis.Calculus.Gradient.Basic

open MeasureTheory Filter
open scoped Topology ContDiff

-- Independent, bounded API/edge verification. No production declaration added.
example : (∞ : WithTop ℕ∞) ≠ (⊤ : WithTop ℕ∞) := by simp

#check @ContDiff.continuous_fderiv
#check @HasCompactSupport.comp_left
#check @Continuous.integrable_of_hasCompactSupport
#check @ContDiff.sqrt
#check @MeasureTheory.MemLp.of_bound
#check @IsCompact.exists_bound_of_continuousOn
#check @Real.continuous_mul_log
#check @Real.sq_sqrt
#check @MeasureTheory.Integrable.mono'
#check @toDual_gradient
#check @AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.CompactGradientSqrtPerturbation.eventually_contDiff_and_integrable_sqrt_perturbation

-- An ordinary eventual neighborhood includes its base point, unlike a punctured one.
example {p : ℝ → Prop} (hp : ∀ᶠ e in 𝓝 (0 : ℝ), p e) : p 0 :=
  mem_of_mem_nhds hp

-- The literal noncompactness phrase in lesson step 3 has a compact-domain exception.
example {E : Type*} [TopologicalSpace E] [CompactSpace E] (u : E → ℝ) :
    HasCompactSupport u :=
  isClosed_tsupport u |>.isCompact

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.CompactGradientSqrtPerturbation.eventually_contDiff_and_integrable_sqrt_perturbation
