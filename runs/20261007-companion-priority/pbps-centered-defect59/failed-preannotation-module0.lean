import AutoSamplingTheory.ExampleCases.ProximalBPS.L2MacroscopicMean
import AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation
import Mathlib.Analysis.InnerProductSpace.Positive

open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 1600000

theorem actual_centered_selfadjoint_defect
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
    IsProbabilityMeasure μ ∧ IsProbabilityMeasure J ∧ IsProbabilityMeasure ν ∧
    ∃ S : Kernel E E, IsMarkovKernel S ∧
      (∀ y, S y = (volume : Measure E).tilted
        (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η))) ∧
      Λ.IsCondKernel S ∧ Λ.fst = ν ∧ Λ.snd = ν ∧
      ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
        (∀ g : Lp ℝ 2 J, (U g : E × E → ℝ) =ᵐ[J] g ∘ F) ∧
        Function.Involutive U ∧ IsSelfAdjoint U.toContinuousLinearMap ∧
        ∃ M : Lp ℝ 2 ν →ₗᵢ[ℝ] Lp ℝ 2 J,
          (∀ u : Lp ℝ 2 ν, (M u : E × E → ℝ) =ᵐ[J] u ∘ Prod.snd) ∧
          ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
            IsSelfAdjoint T ∧
            (∀ u : Lp ℝ 2 ν,
              P (M u) = M u ∧
              M (T u) = (P * U.toContinuousLinearMap * P) (M u) ∧
              ‖T u‖ ≤ ‖u‖ ∧
              (T u : E → ℝ) =ᵐ[ν] (fun y => ∫ x, u x ∂S y) ∧
              (∫ y, T u y ∂ν) = ∫ y, u y ∂ν) ∧
            ∃ q : Lp ℝ 2 ν,
              (q : E → ℝ) =ᵐ[ν] (fun _ => (1 : ℝ)) ∧ T q = q ∧
              (∀ u : Lp ℝ 2 ν, inner ℝ q u = ∫ y, u y ∂ν) ∧
              let H0 : Submodule ℝ (Lp ℝ 2 ν) := (innerSL ℝ q).ker
              (∀ u : Lp ℝ 2 ν, u ∈ H0 ↔ (∫ y, u y ∂ν) = 0) ∧
              (1-T*T).IsPositive ∧ (1-T*T) q = 0 ∧
              (∀ u : Lp ℝ 2 ν,
                inner ℝ ((1-T*T) u) u = ‖u‖^2-‖T u‖^2) ∧
              ∃ T0 : H0 →L[ℝ] H0,
                (∀ u : H0, (T0 u : Lp ℝ 2 ν) = T u) ∧
                IsSelfAdjoint T0 ∧ (∀ u : H0, ‖T0 u‖ ≤ ‖u‖) ∧
                (1-T0*T0).IsPositive ∧
                (∀ u : H0, ((1-T0*T0) u : Lp ℝ 2 ν) = (1-T*T) u) ∧
                (∀ u : H0,
                  inner ℝ ((1-T0*T0) u) u = ‖u‖^2-‖T0 u‖^2) := by
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
  have hBase := L2MacroscopicMean.actual_macroscopic_l2_mean hα hαβ hV hH hη hβη
  rcases hBase with ⟨hμ,hJ,hν,S,hS,hSd,hSc,hSf,hSs,U,hU,hUi,hUs,M,hM,T,hAll⟩
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
  have hDef (u : Lp ℝ 2 ν) : inner ℝ ((1-T*T) u) u = ‖u‖^2-‖T u‖^2 := by
    simp only [ContinuousLinearMap.sub_apply, ContinuousLinearMap.one_apply,
      ContinuousLinearMap.mul_apply, inner_sub_left]
    have hs : inner ℝ (T (T u)) u = inner ℝ (T u) (T u) := hTs.isSymmetric (T u) u
    rw [hs, real_inner_self_eq_norm_sq, real_inner_self_eq_norm_sq]
  trace "59 full defect identity constructed"
  have hD : (1-T*T).IsPositive := by
    apply (ContinuousLinearMap.isPositive_iff' _).mpr
    refine ⟨(isSelfAdjoint_one.sub (by simpa only [pow_two] using hTs.pow 2)),?_⟩
    intro u
    rw [hDef]
    exact sub_nonneg.mpr ((sq_le_sq₀ (norm_nonneg _) (norm_nonneg _)).mpr (hTn u))
  have hDef0 (u : H0) : inner ℝ ((1-T0*T0) u) u = ‖u‖^2-‖T0 u‖^2 := by
    simp only [ContinuousLinearMap.sub_apply, ContinuousLinearMap.one_apply,
      ContinuousLinearMap.mul_apply, inner_sub_left]
    have hs : inner ℝ (T0 (T0 u)) u = inner ℝ (T0 u) (T0 u) := hT0s.isSymmetric (T0 u) u
    rw [hs, real_inner_self_eq_norm_sq, real_inner_self_eq_norm_sq]
  have hD0 : (1-T0*T0).IsPositive := by
    apply (ContinuousLinearMap.isPositive_iff' _).mpr
    refine ⟨isSelfAdjoint_one.sub (by simpa only [pow_two] using hT0s.pow 2),?_⟩
    intro u
    rw [hDef0]
    exact sub_nonneg.mpr ((sq_le_sq₀ (norm_nonneg _) (norm_nonneg _)).mpr (hT0n u))
  trace "59 positivity constructed; assemble witnesses"
  have hqa : (q : E → ℝ) =ᵐ[ν] (fun _ => (1 : ℝ)) :=
    Lp.coeFn_const (α:=E) (μ:=ν) (p:=(2 : ℝ≥0∞)) (c:=(1 : ℝ))
  refine ⟨hμ,hJ,hν,S,hS,hSd,hSc,hSf,hSs,U,hU,hUi,hUs,M,hM,T,hTs,?_,
    q,hqa,hTq,hq,?_⟩
  · intro u
    exact ⟨(hAll u).1,(hAll u).2.1,hTn u,(hAll u).2.2.2.1,hPreserve u⟩
  · refine ⟨hH0,hD,?_,hDef,T0,hT0,hT0s,hT0n,hD0,?_,hDef0⟩
    · simp only [ContinuousLinearMap.sub_apply,ContinuousLinearMap.one_apply,
        ContinuousLinearMap.mul_apply,hTq,sub_self]
    · intro u
      rfl

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator

#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator.actual_centered_selfadjoint_defect
