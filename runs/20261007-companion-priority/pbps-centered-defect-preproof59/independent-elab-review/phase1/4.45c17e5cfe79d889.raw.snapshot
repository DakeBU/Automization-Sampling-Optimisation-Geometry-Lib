import AutoSamplingTheory.ExampleCases.ProximalBPS.L2MacroscopicMean
import AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation
import Mathlib.Analysis.InnerProductSpace.Positive

open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 1600000

example
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    let ν := J.snd
    let Λ := J.map (fun p : E × E => (p.2,(2 : ℝ) • p.1-p.2))
    let F := fun p : E × E => (p.1,(2 : ℝ) • p.1-p.2)
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E))
        2 J).subtypeL ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
    ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν, IsSelfAdjoint T ∧
      ∃ q : Lp ℝ 2 ν, T q=q ∧ (∀ u : Lp ℝ 2 ν, inner ℝ q u=∫ y,u y ∂ν) ∧
      let H0 : Submodule ℝ (Lp ℝ 2 ν) := (innerSL ℝ q).ker
      ∃ T0 : H0 →L[ℝ] H0, IsSelfAdjoint T0 := by
  classical
  dsimp only
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := (μ.prod (stdGaussian E)).map
    (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
  let ν := J.snd
  let Λ := J.map (fun p : E × E => (p.2,(2 : ℝ) • p.1-p.2))
  let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
    (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E))
      2 J).subtypeL ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
  obtain ⟨hμ,hJ,hν,S,hS,hSd,hSc,hSf,hSs,U,hU,hUi,hUs,M,hM,T,hAll⟩ :=
    L2MacroscopicMean.actual_macroscopic_l2_mean hα hαβ hV hH hη hβη
  letI : IsProbabilityMeasure μ := hμ
  letI : IsProbabilityMeasure J := hJ
  letI : IsProbabilityMeasure ν := hν
  letI : IsMarkovKernel S := hS
  letI : Λ.IsCondKernel S := hSc
  have hPs (f g : Lp ℝ 2 J) : inner ℝ (P f) g = inner ℝ f (P g) :=
    inner_condExpL2_left_eq_right measurable_snd.comap_le
  trace "59 begin symmetry"
  have hTs : IsSelfAdjoint T := by
    apply ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mpr
    intro u v
    change inner ℝ (T u) v = inner ℝ u (T v)
    rw [← M.inner_map_map (T u) v, ← M.inner_map_map u (T v)]
    rw [(hAll u).2.1, (hAll v).2.1]
    change inner ℝ (P (U (P (M u)))) (M v) =
      inner ℝ (M u) (P (U (P (M v))))
    rw [hPs, (hAll u).1, (hAll v).1]
    calc
      inner ℝ (U (M u)) (M v) = inner ℝ (M u) (U (M v)) :=
        hUs.isSymmetric (M u) (M v)
      _ = inner ℝ (M u) (P (U (M v))) := by
        rw [← hPs, (hAll u).1]
  trace "59 symmetry constructed"
  have hcompS : ν ⊗ₘ S = Λ := by
    calc
      ν ⊗ₘ S = Λ.fst ⊗ₘ S := congrArg (fun ρ => ρ ⊗ₘ S) hSf.symm
      _ = Λ := Measure.disintegrate Λ S
  have hPreserve (u : Lp ℝ 2 ν) : (∫ y, T u y ∂ν)=∫ y, u y ∂ν := by
    have hi : Integrable (fun p : E × E => u p.2) (ν ⊗ₘ S) := by
      rw [hcompS]
      exact ((Lp.memLp u).comp_measurePreserving
        (show MeasurePreserving (Prod.snd : E × E → E) Λ ν from
          ⟨measurable_snd,hSs⟩)).integrable (by norm_num)
    rw [integral_congr_ae (hAll u).2.2.2.1, ← Measure.integral_compProd hi, hcompS]
    calc
      (∫ p : E × E, u p.2 ∂Λ) = ∫ y, u y ∂Λ.snd :=
        (integral_map (μ:=Λ) measurable_snd.aemeasurable
          (Lp.stronglyMeasurable u).aestronglyMeasurable).symm
      _ = ∫ y, u y ∂ν := by rw [hSs]
  trace "59 mean constructed"
  let q : Lp ℝ 2 ν := AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.one ν
  have hq (u : Lp ℝ 2 ν) : inner ℝ q u = ∫ y, u y ∂ν :=
    AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.inner_one_eq_integral ν u
  have hTq : T q=q := by
    apply ext_inner_right ℝ
    intro u
    calc
      inner ℝ (T q) u = inner ℝ q (T u) := hTs.isSymmetric q u
      _ = ∫ y, T u y ∂ν := hq _
      _ = ∫ y, u y ∂ν := hPreserve u
      _ = inner ℝ q u := (hq _).symm
  let H0 : Submodule ℝ (Lp ℝ 2 ν) := (innerSL ℝ q).ker
  have hH0 (u : Lp ℝ 2 ν) : u ∈ H0 ↔ (∫ y, u y ∂ν)=0 := by
    change inner ℝ q u = 0 ↔ _
    rw [hq]
  have hInv (u : H0) : T u ∈ H0 :=
    (hH0 _).mpr ((hPreserve u).trans ((hH0 _).mp u.property))
  let T0 : H0 →L[ℝ] H0 := (T.comp H0.subtypeL).codRestrict H0 hInv
  have hT0 (u : H0) : (T0 u : Lp ℝ 2 ν)=T u := rfl
  have hT0s : IsSelfAdjoint T0 := by
    apply ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mpr
    intro u v
    exact hTs.isSymmetric (u : Lp ℝ 2 ν) (v : Lp ℝ 2 ν)
  have hTn (u : Lp ℝ 2 ν) : ‖T u‖ ≤ ‖u‖ := (hAll u).2.2.1
  have hT0n (u : H0) : ‖T0 u‖ ≤ ‖u‖ := hTn u
  exact ⟨T,hTs,q,hTq,hq,T0,hT0s⟩

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator
