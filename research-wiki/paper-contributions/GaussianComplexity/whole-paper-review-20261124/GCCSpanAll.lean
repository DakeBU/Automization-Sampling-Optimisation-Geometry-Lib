import GCCPublicStep
import GCCExposedRank

/-! Exact revealed subspace after an image or preimage query for every rank. -/
noncomputable section
open Matrix Module
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

private theorem complementary_answer {N m : ℕ} (F : BlockFrame N m) (b : Bool) (x : Vec N) (z : S m) :
    frameComplement F (!b) (frameResponse F b x z) = ‖frameComplement F b x‖ • z.val := by
  rcases F with ⟨r,hr,D,R⟩
  subst N
  let I := queryFrame b D R
  let J := queryFrame b R D
  have hswap : queryFrame (!b) D R = J := by cases b <;> rfl
  change queryComplement (m := m) (r := r) (queryFrame (!b) D R) (responseFromSphere I J x z) = _
  rw [hswap]
  simp only [queryComplement,responseFromSphere,encodeResponse,act_inv_act,residualCoords_splitVec]
  rfl

private theorem response_realize {N m : ℕ} [NeZero m] (F : BlockFrame N m) (W : O m) (b : Bool) (x : Vec N) :
    response b (F.realize W) x = frameResponse F b x (frameObservation F b x W) := by
  cases b
  · exact frameAnswer_eq F false x W
  · exact frameAnswer_eq F true x W

private theorem latent_mem_iff {N m : ℕ} [NeZero m] (F : BlockFrame N m) (W : O m) (b : Bool) (x : Vec N) :
    (if b then response b (F.realize W) x else x) ∈ exposedSpace F.domain F.rank ↔
      frameComplement F b x = 0 := by
  cases b
  · exact (frameComplement_zero_iff F false x).symm
  · let z := frameObservation F true x W
    change response true (F.realize W) x ∈ exposedSpace F.domain F.rank ↔ _
    rw [show response true (F.realize W) x = frameResponse F true x z from frameAnswer_eq F true x W]
    change frameResponse F true x z ∈ exposedSpace (queryFrame false F.domain F.range) F.rank ↔ _
    rw [← frameComplement_zero_iff]
    rw [show frameComplement F false (frameResponse F true x z) = ‖frameComplement F true x‖ • z.val
      from complementary_answer F true x z]
    have hz : z.val ≠ 0 := norm_ne_zero_iff.mp ((mem_sphere_zero_iff_norm.mp z.property) ▸ one_ne_zero)
    simp [smul_eq_zero,hz]

private theorem full_exposed {N : ℕ} (F : BlockFrame N 0) : exposedSpace F.domain F.rank = ⊤ := by
  apply Submodule.eq_top_of_finrank_eq
  rw [exposedSpace_finrank,Module.finrank_pi,Fintype.card_fin]
  simpa using F.fits

/-- C.3(ii–iii). The updated hidden subspace equals the original one plus the span
of the queried latent vector. This includes a determined answer, an informative final
direction, and an already completely observed orthogonal map. -/
theorem nextPublic_exposed_eq {N : ℕ} (F : PublicFrame N) (W : O F.1) (b : Bool) (x : Vec N) :
    let y := response b (F.2.realize W) x
    let G := nextPublic F b x y
    exposedSpace G.2.domain G.2.rank =
      exposedSpace F.2.domain F.2.rank ⊔ Submodule.span ℝ {if b then y else x} := by
  classical
  rcases F with ⟨m,D⟩
  dsimp only
  cases m with
  | zero => simp only [nextPublic,full_exposed,top_sup_eq]
  | succ m =>
    let y := response b (D.realize W) x
    let v := if b then y else x
    have hmem : v ∈ exposedSpace D.domain D.rank ↔ frameComplement D b x = 0 := latent_mem_iff D W b x
    by_cases hc : frameComplement D b x = 0
    · have hle : Submodule.span ℝ {v} ≤ exposedSpace D.domain D.rank :=
        Submodule.span_le.mpr (Set.singleton_subset_iff.mpr (hmem.mpr hc))
      have hn : nextPublic ⟨m+1,D⟩ b x y = ⟨m+1,D⟩ := by
        cases m <;> unfold nextPublic <;> exact if_pos hc
      change exposedSpace (nextPublic ⟨m+1,D⟩ b x y).2.domain (nextPublic ⟨m+1,D⟩ b x y).2.rank =
        exposedSpace D.domain D.rank ⊔ Submodule.span ℝ {v}
      rw [hn]
      exact (sup_eq_left.mpr hle).symm
    · cases m with
      | zero =>
        have htop : exposedSpace D.domain D.rank ⊔ Submodule.span ℝ {v} = ⊤ := by
          apply Submodule.eq_top_of_finrank_eq
          rw [Submodule.finrank_sup_span_singleton (fun hv => hc (hmem.mp hv)), exposedSpace_finrank,
            Module.finrank_pi,Fintype.card_fin]
          have hN := D.fits
          omega
        let D' := fullFrame (D.realize (lastDecode (frameUnit D b x) (frameUnit D (!b) y)))
        have hn : nextPublic ⟨1,D⟩ b x y = ⟨0,D'⟩ := by unfold nextPublic; exact if_neg hc
        change exposedSpace (nextPublic ⟨1,D⟩ b x y).2.domain (nextPublic ⟨1,D⟩ b x y).2.rank = _
        rw [hn]
        exact (full_exposed D').trans htop.symm
      | succ n =>
        let z := frameObservation D b x W
        have hy : y = frameResponse D b x z := response_realize D W b x
        have hu : frameUnit D (!b) y = z := by
          rw [hy]
          exact recovered_observation D b x z hc
        change exposedSpace (nextPublic ⟨n+2,D⟩ b x y).2.domain (nextPublic ⟨n+2,D⟩ b x y).2.rank = _
        have hnext : nextPublic ⟨n+2,D⟩ b x y = ⟨n+1,frameAfter D (sectionQ n) b x z⟩ := by
          change (if frameComplement D b x = 0 then (⟨n+2,D⟩ : PublicFrame N)
            else ⟨n+1,frameAfter D (sectionQ n) b x (frameUnit D (!b) y)⟩) = _
          rw [if_neg hc,hu]
        rw [hnext]
        simpa only [← hy] using frameAfter_exposed_eq D (sectionQ n) (sectionQ_col n) b x z hc

#print axioms nextPublic_exposed_eq
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
