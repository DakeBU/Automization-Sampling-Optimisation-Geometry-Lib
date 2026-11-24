import GCCProjectionGeometry

noncomputable section
open Matrix
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

private def ambientIso {N : ℕ} (A : O N) : E N ≃ₗᵢ[ℝ] E N :=
  Unitary.linearIsometryEquiv
    (⟨Matrix.toEuclideanCLM (𝕜 := ℝ) A.val,
      Unitary.map_mem (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin N)) A.property⟩ :
      unitary (E N →L[ℝ] E N))

private theorem sends_exposed {m r : ℕ} (D R : O (m+r)) (W : O m) (x : Vec (m+r))
    (hx : x ∈ exposedSpace D r) : act (framed D R W) x ∈ exposedSpace R r := by
  have h := (exposedSpace_iff D x).1 hx
  have e := query_from_coordinates D x
  rw [h] at e
  apply (exposedSpace_iff R _).2
  conv_lhs => arg 3; arg 2; arg 2; rw [← e]
  rw [(zero_residual_response D R W _).1,act_inv_act,residualCoords_splitVec]

private theorem mem_exposed_iff {N m : ℕ} (F : BlockFrame N m) (W : O m) (x : E N) :
    ambientIso (F.realize W) x ∈ exposedEuclidean F.range F.rank ↔
      x ∈ exposedEuclidean F.domain F.rank := by
  rcases F with ⟨r,e,D,R⟩; subst N
  change act (framed D R W) x.ofLp ∈ exposedSpace R r ↔ x.ofLp ∈ exposedSpace D r
  refine ⟨fun h => ?_,sends_exposed D R W x.ofLp⟩
  have hh := sends_exposed R D W⁻¹ _ h
  rwa [← framed_inv,act_inv_act] at hh

/-- The ambient completion carries the exposed domain onto the exposed range and
its remaining domain onto the orthogonal complement of that range. Both identities
hold for every possible residual matrix and at rank zero or full rank. -/
theorem completion_subspaces {N m : ℕ} (F : BlockFrame N m) (W : O m) :
    let L := (Matrix.toEuclideanCLM (𝕜 := ℝ) (F.realize W).val).toLinearMap
    (exposedEuclidean F.domain F.rank).map L = exposedEuclidean F.range F.rank ∧
    (exposedEuclidean F.domain F.rank)ᗮ.map L = (exposedEuclidean F.range F.rank)ᗮ := by
  let I := ambientIso (F.realize W)
  let U := exposedEuclidean F.domain F.rank
  let V := exposedEuclidean F.range F.rank
  have hinv (x : E N) : I x ∈ V ↔ x ∈ U := mem_exposed_iff F W x
  have hco (x : E N) : I x ∈ Vᗮ ↔ x ∈ Uᗮ := by
    constructor
    · intro hx v hv
      have h := hx (I v) ((hinv v).2 hv)
      rwa [I.inner_map_map] at h
    · intro hx v hv
      obtain ⟨u,rfl⟩ := I.surjective v
      rw [I.inner_map_map]
      exact hx u ((hinv u).1 hv)
  have hmap (P Q : Submodule ℝ (E N)) (hpq : ∀ x, I x ∈ Q ↔ x ∈ P) :
      P.map I.toLinearEquiv.toLinearMap = Q := by
    ext y; constructor
    · rintro ⟨x,hx,rfl⟩; exact (hpq x).2 hx
    · intro hy
      obtain ⟨x,rfl⟩ := I.surjective y
      exact ⟨x,(hpq x).1 hy,rfl⟩
  exact ⟨hmap U V hinv,hmap Uᗮ Vᗮ hco⟩

/-- After exposing u and its image, the restriction of the remaining isometry is between
the intersections of the old domain/range complements with the two new perpendicular
hyperplanes. The hypothesis on the new domain is the span conclusion of Fact C.3. -/
theorem completion_perpendicular_restriction {N m n : ℕ} (F : BlockFrame N m) (G : BlockFrame N n)
    (W : O m) (V : O n) (same : G.realize V = F.realize W) (u : E N)
    (enlarged : exposedEuclidean G.domain G.rank =
      exposedEuclidean F.domain F.rank ⊔ ℝ ∙ u) :
    let v := Matrix.toEuclideanCLM (𝕜 := ℝ) (F.realize W).val u
    (exposedEuclidean G.domain G.rank)ᗮ = (exposedEuclidean F.domain F.rank)ᗮ ⊓ (ℝ ∙ u)ᗮ ∧
    (exposedEuclidean G.range G.rank)ᗮ = (exposedEuclidean F.range F.rank)ᗮ ⊓ (ℝ ∙ v)ᗮ := by
  let L := (Matrix.toEuclideanCLM (𝕜 := ℝ) (F.realize W).val).toLinearMap
  have old : (exposedEuclidean F.domain F.rank).map L = _ := (completion_subspaces F W).1
  have new := (completion_subspaces G V).1
  rw [same] at new
  change (exposedEuclidean G.domain G.rank).map L = _ at new
  rw [enlarged,Submodule.map_sup,old,Submodule.map_span,Set.image_singleton] at new
  rw [enlarged,← new]
  exact ⟨(Submodule.inf_orthogonal _ _).symm,(Submodule.inf_orthogonal _ _).symm⟩

#print axioms completion_subspaces
#print axioms completion_perpendicular_restriction
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
