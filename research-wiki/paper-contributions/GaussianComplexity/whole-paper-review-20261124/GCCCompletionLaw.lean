import GCCChartRange
import GC3PublicFrames

/-! The uniform completion of a partial orthogonal isometry does not depend
on the two frames used to represent it. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory Set
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

theorem orthogonalHaar_map_mul_right (n : ℕ) (R : O n) :
    (orthogonalHaar n).map (fun U => U * R) = orthogonalHaar n := by
  let := (orthogonalHaar_spec n).1
  let := (orthogonalHaar_spec n).2.1
  exact (orthogonalHaar_spec n).2.2 _
    (Measure.isProbabilityMeasure_map (measurable_mul_const R).aemeasurable) inferInstance

/-- Independent domain and range coordinate changes preserve the uniform
orthogonal isometry between two Euclidean spaces in their orthonormal coordinates. -/
theorem haar_two_frame_changes (m : ℕ) (D R : O m) :
    MeasurePreserving (fun w : O m => R * w * D⁻¹) (orthogonalHaar m) (orthogonalHaar m) := by
  exact ((⟨measurable_mul_const D⁻¹,orthogonalHaar_map_mul_right m D⁻¹⟩ :
    MeasurePreserving (fun w : O m => w * D⁻¹) (orthogonalHaar m) (orthogonalHaar m)).comp
    (⟨measurable_const_mul R,orthogonalHaar_map_mul_left m R⟩ :
      MeasurePreserving (fun w : O m => R * w) (orthogonalHaar m) (orthogonalHaar m)))

private theorem mapped_product {X Y Z : Type*} [MeasurableSpace X] [MeasurableSpace Y]
    [MeasurableSpace Z] (μ : Measure X) [IsProbabilityMeasure μ] (ν : Measure Y)
    [IsProbabilityMeasure ν] (g : X × Y → Z) (hg : Measurable g) (ρ : Measure Z)
    (hs : ∀ x, ν.map (fun y => g (x,y)) = ρ) :
    (μ.prod ν).map g = ρ := by
  ext s h
  rw [Measure.map_apply hg h,Measure.prod_apply (hg h)]
  have he x : ν (Prod.mk x ⁻¹' g ⁻¹' s) = ρ s := by
    rw [← hs x, Measure.map_apply (show Measurable (fun y => g (x,y)) from
      hg.comp measurable_prodMk_left) h]
    rfl
  simp_rw [he]
  simp

private theorem realize_ternary {N m : ℕ} (F : BlockFrame N m) (u v w : O m) :
    F.realize u * (F.realize v)⁻¹ * F.realize w = F.realize (u*v⁻¹*w) := by
  rcases F with ⟨r,e,D,R⟩; subst N
  change (R * prefixEmbed m r u * D⁻¹) * (R * prefixEmbed m r v * D⁻¹)⁻¹ *
    (R * prefixEmbed m r w * D⁻¹) = R * prefixEmbed m r (u*v⁻¹*w) * D⁻¹
  rw [map_mul,map_mul,map_inv]
  group

def completionInFrame {N m : ℕ} (F : BlockFrame N m) : Measure (O N) :=
  (orthogonalHaar m).map F.realize

theorem completion_eq_of_range_eq {N m n : ℕ} (F : BlockFrame N m) (G : BlockFrame N n)
    (hr : range F.realize = range G.realize) : completionInFrame F = completionInFrame G := by
  let μ := orthogonalHaar m
  let ν := orthogonalHaar n
  let : IsProbabilityMeasure μ := (orthogonalHaar_spec m).1
  let : IsProbabilityMeasure ν := (orthogonalHaar_spec n).1
  let base := F.realize 1
  obtain ⟨v,hv⟩ : base ∈ range G.realize := hr ▸ mem_range_self (1 : O m)
  let mix (p : O m × O n) := F.realize p.1 * base⁻¹ * G.realize p.2
  have hm : Measurable mix := ((F.measurable_realize.comp measurable_fst).mul_const base⁻¹).mul
    (G.measurable_realize.comp measurable_snd)
  have hg : (μ.prod ν).map mix = completionInFrame G := by
    apply mapped_product _ _ mix hm
    intro x
    obtain ⟨u,hu⟩ : F.realize x ∈ range G.realize := hr ▸ mem_range_self x
    have he : (fun y => mix (x,y)) = G.realize ∘ (fun y => (u*v⁻¹)*y) := by
      funext y
      change F.realize x * base⁻¹ * G.realize y = _
      rw [← hu,← hv,realize_ternary]; rfl
    rw [he,← Measure.map_map G.measurable_realize (measurable_const_mul _),
      orthogonalHaar_map_mul_left]
    rfl
  have hf : (ν.prod μ).map (mix ∘ Prod.swap) = completionInFrame F := by
    apply mapped_product _ _ _ (hm.comp measurable_swap)
    intro y
    obtain ⟨u,hu⟩ : G.realize y ∈ range F.realize := hr.symm ▸ mem_range_self y
    have he : (fun x => (mix ∘ Prod.swap) (y,x)) = F.realize ∘ (fun x => x*u) := by
      funext x
      change F.realize x * (F.realize 1)⁻¹ * G.realize y = _
      rw [← hu,realize_ternary,inv_one,mul_one]; rfl
    rw [he,← Measure.map_map F.measurable_realize (measurable_mul_const _),
      orthogonalHaar_map_mul_right]
    rfl
  rw [← Measure.map_map hm measurable_swap,Measure.prod_swap] at hf
  exact hf.symm.trans hg

def observationOf {N m : ℕ} (F : BlockFrame N m) : Mat N × Mat N :=
  frameObservation F.rank (F.domain,F.range)

theorem completion_eq_of_observation {N m n : ℕ} {F : BlockFrame N m} {G : BlockFrame N n}
    (he : observationOf F = observationOf G) : completionInFrame F = completionInFrame G := by
  apply completion_eq_of_range_eq
  rw [range_realize_eq_compatible,range_realize_eq_compatible]
  change {A : O N | A.val*(observationOf F).1=(observationOf F).2} = _
  rw [he]; rfl

/-- The intrinsic Haar completion law is defined from the projection and the observed
partial isometry. Invalid observation pairs use the identity point mass. -/
def intrinsicCompletion {N : ℕ} (p : Mat N × Mat N) : Measure (O N) := by
  classical
  exact if h : ∃ F : PublicFrame N, observationOf F.2 = p
    then completionInFrame (Classical.choose h).2 else Measure.dirac 1

theorem intrinsicCompletion_eq {N m : ℕ} (F : BlockFrame N m) :
    intrinsicCompletion (observationOf F) = completionInFrame F := by
  classical
  have h : ∃ G : PublicFrame N, observationOf G.2 = observationOf F := ⟨⟨m,F⟩,rfl⟩
  rw [intrinsicCompletion, dif_pos h]
  exact completion_eq_of_observation (Classical.choose_spec h)

#print axioms intrinsicCompletion_eq
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
