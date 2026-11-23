import GC43Exposed

open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
noncomputable section
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

variable {H Y : Type*} [MeasurableSpace H] [MeasurableSpace Y] {N m n : ℕ}

theorem measurable_frameFamily (F : H → BlockFrame N m)
    (f : H → BlockFrame N m → Y)
    (hf : ∀ r (e : m+r=N), Measurable (fun h => f h ⟨r,e,(F h).domain,(F h).range⟩)) :
    Measurable (fun h => f h (F h)) := by
  cases isEmpty_or_nonempty H with
  | inl h => exact measurable_of_empty _
  | inr h =>
    obtain ⟨p⟩ := h
    let r := (F p).rank
    have e : m+r=N := (F p).fits
    have he (h : H) : F h = ⟨r,e,(F h).domain,(F h).range⟩ := by
      cases F h with
      | mk k hk D R =>
        have hk' : k = r := by omega
        subst k; rfl
    have hh := funext fun h => congrArg (f h) (he h)
    rw [hh]
    exact hf r e

theorem measurable_frameComplement {F : H → BlockFrame N m} {b : H → Bool} {v : H → Vec N}
    (hD : Measurable fun h => (F h).domain) (hR : Measurable fun h => (F h).range)
    (hb : Measurable b) (hv : Measurable v) : Measurable (fun h => frameComplement (F h) (b h) (v h)) := by
  apply measurable_frameFamily F (fun h f => frameComplement f (b h) (v h))
  intro r e; subst N
  exact measurable_queryComplement (measurable_queryFrame hb hD hR) hv

theorem measurable_frameUnit [NeZero m] {F : H → BlockFrame N m} {b : H → Bool} {v : H → Vec N}
    (hD : Measurable fun h => (F h).domain) (hR : Measurable fun h => (F h).range)
    (hb : Measurable b) (hv : Measurable v) : Measurable (fun h => frameUnit (F h) (b h) (v h)) :=
  (measurable_unitOrFirst m).comp (measurable_frameComplement hD hR hb hv)

theorem measurable_frameResponse {F : H → BlockFrame N m} {b : H → Bool} {v : H → Vec N} {z : H → S m}
    (hD : Measurable fun h => (F h).domain) (hR : Measurable fun h => (F h).range)
    (hb : Measurable b) (hv : Measurable v) (hz : Measurable z) :
    Measurable (fun h => frameResponse (F h) (b h) (v h) (z h)) := by
  apply measurable_frameFamily F (fun h f => frameResponse f (b h) (v h) (z h))
  intro r e; subst N
  exact (measurable_responseFromSphere (r := r) (m := m) (measurable_queryFrame hb hD hR)
    (measurable_queryFrame hb hR hD) hv).comp (measurable_id.prodMk hz)

theorem measurable_frameAfter {F : H → BlockFrame N (n+2)} (Q : S (n+2) → O (n+2))
    (hQ : Measurable Q) {b : H → Bool} {v : H → Vec N} {z : H → S (n+2)}
    (hD : Measurable fun h => (F h).domain) (hR : Measurable fun h => (F h).range)
    (hb : Measurable b) (hv : Measurable v) (hz : Measurable z) :
    Measurable (fun h => (frameAfter (F h) Q (b h) (v h) (z h)).domain) ∧
    Measurable (fun h => (frameAfter (F h) Q (b h) (v h) (z h)).range) := by
  let u := fun h => frameUnit (F h) (b h) (v h)
  have hu : Measurable u := measurable_frameUnit hD hR hb hv
  let dir := fun h => if b h then z h else u h
  let ran := fun h => if b h then u h else z h
  have hdir : Measurable dir := Measurable.ite (hb (measurableSet_singleton true)) hz hu
  have hran : Measurable ran := Measurable.ite (hb (measurableSet_singleton true)) hu hz
  have hpre {g : H → O (n+2)} (hg : Measurable g) :
      Measurable (fun h => castOrthogonal (F h).fits (prefixEmbed (n+2) (F h).rank (g h))) := by
    apply measurable_frameFamily F (fun h f => castOrthogonal f.fits (prefixEmbed (n+2) f.rank (g h)))
    intro r e; subst N
    exact (continuous_prefixEmbed _ r).measurable.comp hg
  exact ⟨hD.mul (hpre (hQ.comp hdir)), hR.mul (hpre (hQ.comp hran))⟩

theorem recovered_observation {N m : ℕ} [NeZero m] (F : BlockFrame N m) (b : Bool)
    (v : Vec N) (z : S m) (hc : frameComplement F b v ≠ 0) :
    unitOrFirst (frameComplement F (!b) (frameResponse F b v z)) = z := by
  rcases F with ⟨r,hr,D,R⟩
  subst N
  let I := queryFrame b D R
  let J := queryFrame b R D
  let c := queryComplement (m := m) (r := r) I v
  change c ≠ 0 at hc
  have hswap : queryFrame (!b) D R = J := by cases b <;> rfl
  change unitOrFirst (queryComplement (queryFrame (!b) D R) (responseFromSphere I J v z)) = z
  rw [hswap]
  have he : queryComplement J (responseFromSphere I J v z) = ‖c‖ • z.val := by
    simp only [queryComplement,responseFromSphere,encodeResponse,act_inv_act,residualCoords_splitVec]
    rfl
  rw [he]
  have hn := (mem_sphere_zero_iff_norm.mp z.property)
  have hnz : ‖c‖ • z.val ≠ 0 := by
    rw [smul_ne_zero_iff]
    exact ⟨norm_ne_zero_iff.mpr hc, norm_ne_zero_iff.mp (hn ▸ one_ne_zero)⟩
  apply Subtype.ext
  simp [unitOrFirst,hnz,residualUnit,norm_smul,hn,smul_smul,hc]

#print axioms measurable_frameAfter
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
