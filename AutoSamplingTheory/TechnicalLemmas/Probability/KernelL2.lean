import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Probability.Kernel.Invariance
import Mathlib.Probability.Kernel.Composition.IntegralCompProd
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Function.LpSpace.Indicator
import Mathlib.MeasureTheory.Function.AEEqOfIntegral

/-!
# The real L2 operator of a finite invariant Markov kernel

This source-neutral shared prerequisite constructs the observable operator, not a
law-density operator or a semigroup. Finiteness makes every L2 observable L1.
Kernel integration is asserted only almost everywhere, with genuine fiber
integrability, for every representative. Order positivity is not Hilbert positive
semidefiniteness; self-adjointness needs detailed balance, not just invariance.

Motivating consumers are PBPS arXiv:2609.06905v1 A.2/A.9 (retained-coordinate
half-turn) and B.1 (one-step update). Their actual kernel adapters remain separate.
The standard joint-measure/adjoint proof below is not the paper's source topology.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Probability.KernelL2

open MeasureTheory ProbabilityTheory
open scoped ENNReal InnerProductSpace

noncomputable section
set_option autoImplicit false

private def invariant_kernel_l2_statement {X : Type*} [MeasurableSpace X]
    (μ : Measure X) [IsFiniteMeasure μ]
    (κ : Kernel X X) [IsMarkovKernel κ] (hκ : κ.Invariant μ) : Prop :=
    ∃ A : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ, ‖A‖ ≤ 1 ∧
      (∀ f : X → ℝ, ∀ hf : MemLp f 2 μ,
        (∀ᵐ x ∂μ, Integrable f (κ x)) ∧
        (A (hf.toLp f) : X → ℝ) =ᵐ[μ] fun x => ∫ z, f z ∂κ x) ∧
      (∀ f : Lp ℝ 2 μ, (∀ᵐ x ∂μ, 0 ≤ f x) → ∀ᵐ x ∂μ, 0 ≤ A f x) ∧
      A (Lp.const 2 μ (1 : ℝ)) = Lp.const 2 μ (1 : ℝ) ∧
      (∀ f : Lp ℝ 2 μ, (∫ x, A f x ∂μ) = ∫ x, f x ∂μ) ∧
      (κ.IsReversible μ → IsSelfAdjoint A)

private lemma pair_operator {X : Type*} [MeasurableSpace X]
    (μ : Measure X) [IsFiniteMeasure μ] (κ : Kernel X X) [IsMarkovKernel κ]
    (hκ : κ.Invariant μ) :
    ∃ A : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ, ‖A‖ ≤ 1 ∧
      ∀ f g : Lp ℝ 2 μ,
        ⟪f, A g⟫_ℝ = ∫ p : X × X, f p.1 * g p.2 ∂(μ ⊗ₘ κ) := by
  let ν := μ ⊗ₘ κ
  have hfst : MeasurePreserving Prod.fst ν μ :=
    ⟨measurable_fst, Measure.fst_compProd μ κ⟩
  have hsnd : MeasurePreserving Prod.snd ν μ :=
    ⟨measurable_snd, (Measure.snd_compProd μ κ).trans hκ.def⟩
  let B : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 ν :=
    (Lp.compMeasurePreservingₗᵢ ℝ Prod.fst hfst).toContinuousLinearMap
  let C : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 ν :=
    (Lp.compMeasurePreservingₗᵢ ℝ Prod.snd hsnd).toContinuousLinearMap
  let A := B.adjoint.comp C
  have hB : ‖B‖ ≤ 1 := LinearIsometry.norm_toContinuousLinearMap_le _
  have hC : ‖C‖ ≤ 1 := LinearIsometry.norm_toContinuousLinearMap_le _
  refine ⟨A, ?_, ?_⟩
  · calc
      ‖A‖ ≤ ‖B.adjoint‖ * ‖C‖ := ContinuousLinearMap.opNorm_comp_le _ _
      _ = ‖B‖ * ‖C‖ := by rw [ContinuousLinearMap.adjoint.norm_map]
      _ ≤ 1 * 1 := mul_le_mul hB hC (norm_nonneg _) zero_le_one
      _ = 1 := one_mul 1
  · intro f g
    change ⟪f, B.adjoint (C g)⟫_ℝ = _
    rw [ContinuousLinearMap.adjoint_inner_right, L2.inner_def]
    have hb := Lp.coeFn_compMeasurePreserving f hfst
    have hc := Lp.coeFn_compMeasurePreserving g hsnd
    apply integral_congr_ae
    filter_upwards [hb, hc] with p hp hq
    change B f p = f p.1 at hp
    change C g p = g p.2 at hq
    rw [hp, hq]
    simp [RCLike.inner_apply, mul_comm]

/-- A finite invariant Markov kernel induces a real L2 contraction realizing its
genuine conditional integrals. It preserves order, one and the mean; detailed
balance additionally makes it self-adjoint. No topology or nonempty premise is
required. See the sealed statement for all representative and AE quantifiers. -/
theorem invariant_kernel_l2_operator {X : Type*} [MeasurableSpace X]
    (μ : Measure X) [IsFiniteMeasure μ]
    (κ : Kernel X X) [IsMarkovKernel κ] (hκ : κ.Invariant μ) :
    invariant_kernel_l2_statement μ κ hκ := by
  classical
  obtain ⟨A, hA, hpair⟩ := pair_operator μ κ hκ
  let ν := μ ⊗ₘ κ
  have hfst : MeasurePreserving Prod.fst ν μ :=
    ⟨measurable_fst, Measure.fst_compProd μ κ⟩
  have hsnd : MeasurePreserving Prod.snd ν μ :=
    ⟨measurable_snd, (Measure.snd_compProd μ κ).trans hκ.def⟩
  have hrep : ∀ G : X → ℝ, ∀ hG : MemLp G 2 μ,
      (∀ᵐ x ∂μ, Integrable G (κ x)) ∧
      (A (hG.toLp G) : X → ℝ) =ᵐ[μ] fun x => ∫ z, G z ∂κ x := by
    intro G hG
    have hprod : Integrable (fun p : X × X => G p.2) ν :=
      (hG.comp_measurePreserving hsnd).integrable (by norm_num)
    have hc : Integrable G ((κ ∘ₖ Kernel.const Unit μ) ()) := by
      simpa only [Kernel.comp_const, Kernel.const_apply, hκ.def] using
        hG.integrable (by norm_num)
    have hop : Integrable (fun x => ∫ z, G z ∂κ x) μ := by
      simpa only [Kernel.const_apply] using hc.integral_comp
    have hAg : Integrable (A (hG.toLp G) : X → ℝ) μ :=
      (Lp.memLp _).integrable (by norm_num)
    refine ⟨Measure.ae_integrable_of_integrable_comp (by
      simpa only [hκ.def] using hG.integrable (by norm_num)), ?_⟩
    apply Integrable.ae_eq_of_forall_setIntegral_eq _ _ hAg hop
    intro s hs hms
    let i : Lp ℝ 2 μ := indicatorConstLp 2 hs hms.ne (1 : ℝ)
    have hi : (i : X → ℝ) =ᵐ[μ] s.indicator (fun _ => (1 : ℝ)) :=
      indicatorConstLp_coeFn
    have hi' := hfst.quasiMeasurePreserving.ae_eq hi
    have hg' := hsnd.quasiMeasurePreserving.ae_eq hG.coeFn_toLp
    let F : X × X → ℝ := fun p => s.indicator (fun _ => (1 : ℝ)) p.1 * G p.2
    have hF : Integrable F ν := by
      have he : F = (Prod.fst ⁻¹' s).indicator (fun p : X × X => G p.2) := by
        funext p
        by_cases hp : p.1 ∈ s <;> simp [F, Set.indicator, hp]
      rw [he]
      exact hprod.indicator (hs.preimage measurable_fst)
    calc
      (∫ x in s, A (hG.toLp G) x ∂μ) = ⟪i, A (hG.toLp G)⟫_ℝ :=
        (L2.inner_indicatorConstLp_one hs hms.ne _).symm
      _ = ∫ p : X × X, i p.1 * (hG.toLp G) p.2 ∂ν := hpair i (hG.toLp G)
      _ = ∫ p, F p ∂ν := by
        apply integral_congr_ae
        filter_upwards [hi', hg'] with p hp hq
        change i p.1 = s.indicator (fun _ => (1 : ℝ)) p.1 at hp
        change (hG.toLp G) p.2 = G p.2 at hq
        simp only [F, hp, hq]
      _ = ∫ x, ∫ z, F (x, z) ∂κ x ∂μ := Measure.integral_compProd hF
      _ = ∫ x, s.indicator (fun _ => (1 : ℝ)) x * (∫ z, G z ∂κ x) ∂μ := by
        simp only [F, integral_const_mul]
      _ = ∫ x in s, (∫ z, G z ∂κ x) ∂μ := by
        rw [← integral_indicator hs]
        congr 1
        funext x
        by_cases hx : x ∈ s <;> simp [Set.indicator, hx]
  have hrepLp (f : Lp ℝ 2 μ) :
      (A f : X → ℝ) =ᵐ[μ] fun x => ∫ z, f z ∂κ x := by
    simpa only [Lp.toLp_coeFn] using (hrep f (Lp.memLp f)).2
  refine ⟨A, hA, hrep, ?_, ?_, ?_, ?_⟩
  · intro f hf
    have hp : ∀ᵐ x ∂μ, ∀ᵐ z ∂κ x, 0 ≤ f z :=
      Measure.ae_ae_of_ae_comp (by simpa only [hκ.def] using hf)
    filter_upwards [hrepLp f, hp] with x hx hp
    rw [hx]
    exact integral_nonneg_of_ae hp
  · have hc := (hrep (fun _ : X => (1 : ℝ)) (memLp_const (1 : ℝ))).2
    rw [MemLp.toLp_const] at hc
    apply Lp.ext
    filter_upwards [hc, Lp.coeFn_const (p := 2) (μ := μ) (c := (1 : ℝ))] with x hx h1
    calc
      A (Lp.const 2 μ (1 : ℝ)) x = 1 := by simpa [measureReal_def] using hx
      _ = Lp.const 2 μ (1 : ℝ) x := h1.symm
  · intro f
    have hprod : Integrable (fun p : X × X => f p.2) ν :=
      ((Lp.memLp f).comp_measurePreserving hsnd).integrable (by norm_num)
    calc
      (∫ x, A f x ∂μ) = ∫ x, ∫ z, f z ∂κ x ∂μ := integral_congr_ae (hrepLp f)
      _ = ∫ p : X × X, f p.2 ∂ν := (Measure.integral_compProd hprod).symm
      _ = ∫ x, f x ∂ν.map Prod.snd :=
        (integral_map_of_stronglyMeasurable measurable_snd (Lp.stronglyMeasurable f)).symm
      _ = ∫ x, f x ∂μ := by rw [hsnd.map_eq]
  · intro hrev
    have hswap : ν.map Prod.swap = ν := by
      apply Measure.ext_prod
      intro s t hs ht
      rw [Measure.map_apply measurable_swap (hs.prod ht)]
      have he : Prod.swap ⁻¹' (s ×ˢ t) = t ×ˢ s := by ext p; simp [and_comm]
      rw [he, Measure.compProd_apply_prod ht hs, Measure.compProd_apply_prod hs ht]
      exact hrev ht hs
    apply ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mpr
    intro f g
    calc
      ⟪A f, g⟫_ℝ = ⟪g, A f⟫_ℝ := real_inner_comm _ _
      _ = ∫ p : X × X, g p.1 * f p.2 ∂ν := hpair g f
      _ = ∫ p : X × X, g p.1 * f p.2 ∂ν.map Prod.swap := by rw [hswap]
      _ = ∫ p : X × X, g p.2 * f p.1 ∂ν := by
        have hm : StronglyMeasurable (fun p : X × X => g p.1 * f p.2) :=
          ((Lp.stronglyMeasurable g).comp_measurable measurable_fst).mul
            ((Lp.stronglyMeasurable f).comp_measurable measurable_snd)
        exact integral_map_of_stronglyMeasurable measurable_swap hm
      _ = ∫ p : X × X, f p.1 * g p.2 ∂ν := by simp only [mul_comm]
      _ = ⟪f, A g⟫_ℝ := (hpair f g).symm

end
end AutoSamplingTheory.TechnicalLemmas.Probability.KernelL2
