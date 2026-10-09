import AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianReflection
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel
import Mathlib.Probability.Kernel.CondDistrib
import Mathlib.MeasureTheory.Function.ConditionalExpectation.Basic
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Tactic.NoncommRing

/-!
# Actual reflection and conditional-projection blocks

Source: arXiv:2609.06905v1, Appendix B.1, equations (B.1)-(B.5).
This constructs the operators on the actual Gaussian augmentation. No strict
coercivity, half-turn dynamics or mixing bound is asserted.
-/

open MeasureTheory ProbabilityTheory

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionL2

universe u

/-- Actual reflection is an L2 self-adjoint isometric involution. The actual
conditional projection has the normalized quadratic-tilt kernel representation
almost everywhere, and its reflection blocks satisfy the source algebra and
macroscopic energy-transfer identity. -/
theorem actual_reflection_block_identities
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (μ : Measure E) [IsProbabilityMeasure μ] {η : ℝ} (hη : 0 < η) :
    let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
      (μ.prod (stdGaussian E))
    let F := fun p : E × E => (p.1,(2:ℝ) • p.1-p.2)
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)) 2 J).subtypeL
        ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
    ∃ R : Kernel E E, IsMarkovKernel R ∧
      (∀ y, R y = μ.tilted (fun x => -‖x-y‖^2/(2*η))) ∧
      ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
        (∀ f, U f =ᵐ[J] f ∘ F) ∧ Function.Involutive U ∧
        IsSelfAdjoint U.toContinuousLinearMap ∧
        (∀ f : Lp ℝ 2 J, (P f : E × E → ℝ) =ᵐ[J]
          fun p => ∫ x, f (x,p.2) ∂R p.2) ∧
        let A := P * U.toContinuousLinearMap * P
        let B := (1-P) * U.toContinuousLinearMap * P
        let D := (1-P) * U.toContinuousLinearMap * (1-P)
        star B*B=P-A^2 ∧ star B*D= -(A*star B) ∧
          (∀ f, P f=f → ‖B f‖^2 = ‖f‖^2-‖A f‖^2) := by
  let J₀ := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    (μ.prod (stdGaussian E))
  let H := Lp ℝ 2 J₀
  have reflection_lift (μ : Measure E) [IsProbabilityMeasure μ] (η : ℝ) (hη : 0 < η) :
      let J := Measure.map (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2))
        (μ.prod (stdGaussian E))
      let R := fun p : E × E => (p.1, (2:ℝ) • p.1-p.2)
      ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
        (∀ f, U f =ᵐ[J] f ∘ R) ∧ Function.Involutive U ∧ IsSelfAdjoint U.toContinuousLinearMap := by
    dsimp only
    let J := Measure.map (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2))
      (μ.prod (stdGaussian E))
    let R := fun p : E × E => (p.1, (2:ℝ) • p.1-p.2)
    obtain ⟨hinv, hmap⟩ :=
      AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianReflection.reflection_preserves_augmentation μ η hη
    have hp : MeasurePreserving R J J := ⟨by fun_prop, hmap⟩
    let U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J := Lp.compMeasurePreservingₗᵢ ℝ R hp
    have hU : Function.Involutive U := by
      intro f
      change Lp.compMeasurePreserving R hp (Lp.compMeasurePreserving R hp f) = f
      rw [← Lp.compMeasurePreserving_comp_apply]
      have hRR : R ∘ R = id := funext hinv
      simp only [hRR, Lp.compMeasurePreserving_id_apply]
    refine ⟨U, fun f => Lp.coeFn_compMeasurePreserving f hp, hU, ?_⟩
    apply ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.2
    intro f g
    change inner ℝ (U f) g = inner ℝ f (U g)
    calc
      inner ℝ (U f) g = inner ℝ (U f) (U (U g)) := by rw [hU g]
      _ = inner ℝ f (U g) := U.inner_map_map f (U g)

  have kernel_condExp (J : Measure (E × E)) [IsProbabilityMeasure J]
      (R : Kernel E E) [IsMarkovKernel R] [(J.map Prod.swap).IsCondKernel R]
      (f : E × E → ℝ) (hf : Integrable f J) :
      J[f | MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)] =ᵐ[J]
        fun p => ∫ x, f (x,p.2) ∂R p.2 := by
    have hswap : Integrable (fun p : E × E => f p.swap) (J.map Prod.swap) := by
      apply (integrable_map_equiv (MeasurableEquiv.prodComm : E × E ≃ᵐ E × E) _).2
      change Integrable f J
      exact hf
    have h := condExp_prod_ae_eq_integral_condDistrib'
      (μ := J) (X := Prod.snd) (Y := Prod.fst)
      (f := fun p : E × E => f p.swap) measurable_snd measurable_fst.aemeasurable hswap
    have heq : R =ᵐ[(J.map Prod.swap).fst] (J.map Prod.swap).condKernel :=
      eq_condKernel_of_measure_eq_compProd R (Measure.disintegrate _ _).symm
    rw [Measure.fst_map_swap] at heq
    have heq' : ∀ᵐ p ∂J, R p.2 = (J.map Prod.swap).condKernel p.2 := by
      exact ae_of_ae_map measurable_snd.aemeasurable heq
    filter_upwards [h, heq'] with p hp he
    rw [he]
    simp only [condDistrib] at hp
    exact hp

  have projection_kernel (μ : Measure E) [IsProbabilityMeasure μ] {η : ℝ} (hη : 0 < η) :
      let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
        (μ.prod (stdGaussian E))
      ∃ R : Kernel E E, IsMarkovKernel R ∧
        (∀ y, R y = μ.tilted (fun x => -‖x-y‖^2/(2*η))) ∧
        (∀ f : Lp ℝ 2 J,
          (condExpL2 ℝ ℝ (μ := J) measurable_snd.comap_le f : E × E → ℝ) =ᵐ[J]
            fun p => ∫ x, f (x,p.2) ∂R p.2) := by
    dsimp only
    let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
      (μ.prod (stdGaussian E))
    have : IsProbabilityMeasure J := Measure.isProbabilityMeasure_map (by fun_prop)
    obtain ⟨R,hR,hformula,hcond⟩ :=
      AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel μ hη
    let _ := hR
    let _ : (J.map Prod.swap).IsCondKernel R := hcond
    refine ⟨R,hR,hformula,?_⟩
    intro f
    have hL2 := (Lp.memLp f).condExpL2_ae_eq_condExp (𝕜 := ℝ) measurable_snd.comap_le
    rw [Lp.toLp_coeFn] at hL2
    exact hL2.trans (kernel_condExp J R f ((Lp.memLp f).integrable (by norm_num)))

  have block_algebra {A : Type u} [Ring A] [StarRing A] (U P : A)
      (hU : star U = U) (hP : star P = P) (hUU : U*U=1) (hPP : P*P=P) :
      let B := (1-P)*U*P
      let D := (1-P)*U*(1-P)
      let A₀ := P*U*P
      star B*B=P-A₀^2 ∧ star B*D= -(A₀*star B) := by
    have hpt (X : A) : P*(P*X)=P*X := by rw [← mul_assoc,hPP]
    have hut (X : A) : U*(U*X)=X := by rw [← mul_assoc,hUU,one_mul]
    dsimp only
    simp only [star_mul,star_sub,star_one,hU,hP]
    constructor <;> noncomm_ring [hPP,hUU,hpt,hut]

  have block_energy (P A B : H →L[ℝ] H) (hA : IsSelfAdjoint A)
      (hBB : star B * B = P-A^2) (f : H) (hf : P f=f) :
      ‖B f‖^2 = ‖f‖^2-‖A f‖^2 := by
    have h := B.apply_norm_sq_eq_inner_adjoint_right f
    have he : B.adjoint.comp B = P-A^2 := hBB
    rw [he] at h
    have hAf : inner ℝ f ((A^2) f) = ‖A f‖^2 := by
      rw [pow_two]
      change inner ℝ f (A (A f)) = _
      calc
        inner ℝ f (A (A f)) = inner ℝ f (A.adjoint (A f)) := by rw [hA.adjoint_eq]
        _ = inner ℝ (A f) (A f) := A.adjoint_inner_right f (A f)
        _ = ‖A f‖^2 := real_inner_self_eq_norm_sq (A f)
    simpa only [sub_apply, hf, inner_sub_right,
      hAf, real_inner_self_eq_norm_sq, RCLike.re_to_real] using h

  dsimp only
  let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    (μ.prod (stdGaussian E))
  let mY : MeasurableSpace (E × E) := MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E)
  let _ : MeasurableSpace (E × E) := Prod.instMeasurableSpace
  have hmY : mY ≤ Prod.instMeasurableSpace := measurable_snd.comap_le
  let S := lpMeas ℝ ℝ mY 2 J
  have : Fact (mY ≤ Prod.instMeasurableSpace) := ⟨hmY⟩
  let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J := S.subtypeL ∘L condExpL2 ℝ ℝ (μ := J) hmY
  have hPdef : P = S.starProjection := rfl
  have hP : IsSelfAdjoint P := by rw [hPdef]; exact isSelfAdjoint_starProjection S
  have hPP : P*P=P := by rw [hPdef]; exact S.isIdempotentElem_starProjection
  obtain ⟨U,hUae,hUi,hUs⟩ := reflection_lift μ η hη
  obtain ⟨R,hR,hRf,hRp⟩ := projection_kernel μ hη
  have hUU : U.toContinuousLinearMap * U.toContinuousLinearMap = 1 := by
    apply ContinuousLinearMap.ext
    intro f
    exact hUi f
  obtain ⟨hBB,hBD⟩ := block_algebra U.toContinuousLinearMap P hUs.star_eq hP.star_eq hUU hPP
  have hA : IsSelfAdjoint (P*U.toContinuousLinearMap*P) := by
    change star (P*U.toContinuousLinearMap*P) = P*U.toContinuousLinearMap*P
    simp only [star_mul,hP.star_eq,hUs.star_eq,mul_assoc]
  refine ⟨R,hR,hRf,U,hUae,hUi,hUs,hRp,hBB,hBD,?_⟩
  intro f hf
  exact block_energy P (P*U.toContinuousLinearMap*P) ((1-P)*U.toContinuousLinearMap*P) hA hBB f hf

end AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionL2
