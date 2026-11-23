import GC43HaarFrame

open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarStabilizerBlock
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
noncomputable section

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

def castVec {m n : ℕ} (e : m=n) (x : Vec m) : Vec n := e ▸ x

def frameComplement {N m : ℕ} (F : BlockFrame N m) (back : Bool) (v : Vec N) : E m :=
  queryComplement (m := m) (r := F.rank)
    (castOrthogonal F.fits.symm (queryFrame back F.domain F.range)) (castVec F.fits.symm v)

def unitOrFirst {m : ℕ} [NeZero m] (x : E m) : S m := by
  classical
  exact if h : x ≠ 0 then residualUnit ⟨x,h⟩ else coordinatePoint 0

theorem measurable_unitOrFirst (m : ℕ) [NeZero m] : Measurable (@unitOrFirst m _) := by
  classical
  exact Measurable.dite (s := {x : E m | x ≠ 0}) (continuous_residualUnit m).measurable
    (g := fun _ => coordinatePoint 0) measurable_const (measurableSet_singleton (0:E m)).compl

theorem scaled_unitOrFirst {m : ℕ} [NeZero m] (x : E m) :
    ‖x‖ • WithLp.ofLp (unitOrFirst x).val = WithLp.ofLp x := by
  by_cases h : x ≠ 0
  · simpa [unitOrFirst,h] using scaled_residualUnit ⟨x,h⟩
  · simp [not_ne_iff.mp h]

def frameUnit {N m : ℕ} [NeZero m] (F : BlockFrame N m) (back : Bool) (v : Vec N) : S m :=
  unitOrFirst (frameComplement F back v)

def frameResponse {N m : ℕ} (F : BlockFrame N m) (back : Bool) (v : Vec N) (z : S m) : Vec N :=
  castVec F.fits (responseFromSphere (m := m) (r := F.rank)
    (castOrthogonal F.fits.symm (queryFrame back F.domain F.range))
    (castOrthogonal F.fits.symm (queryFrame back F.range F.domain)) (castVec F.fits.symm v) z)

def frameObservation {N m : ℕ} [NeZero m] (F : BlockFrame N m) (back : Bool) (v : Vec N)
    (W : O m) : S m := rotate (if back then W⁻¹ else W) (frameUnit F back v)

def frameAfter {N n : ℕ} (F : BlockFrame N (n+2)) (Q : S (n+2) → O (n+2))
    (back : Bool) (v : Vec N) (z : S (n+2)) : BlockFrame N (n+1) where
  rank := F.rank+1
  fits := by have h := F.fits; omega
  domain := F.domain * castOrthogonal F.fits
    (prefixEmbed (n+2) F.rank (Q (if back then z else frameUnit F back v)))
  range := F.range * castOrthogonal F.fits
    (prefixEmbed (n+2) F.rank (Q (if back then frameUnit F back v else z)))

/-- Every residual realization's answer is the public response at its sphere observation.
The formula also applies when the queried residual component vanishes. -/
theorem frameAnswer_eq {N m : ℕ} [NeZero m] (F : BlockFrame N m) (back : Bool)
    (v : Vec N) (W : O m) :
    (if back then act (F.realize W)⁻¹ v else act (F.realize W) v) =
      frameResponse F back v (frameObservation F back v W) := by
  rcases F with ⟨r,hr,D,R⟩
  subst N
  let input := queryFrame back D R
  let c := queryComplement (m := m) (r := r) input v
  let a := exposedCoords m r (act input⁻¹ v)
  let u := unitOrFirst c
  have hx : act input (splitVec r a (‖c‖ • WithLp.ofLp u.val)) = v := by
    rw [scaled_unitOrFirst]
    exact query_from_coordinates input v
  cases back
  · exact (congrArg (act (framed D R W)) hx.symm).trans (normalized_responses D R W a ‖c‖ u).1
  · exact (congrArg (act (framed D R W)⁻¹) hx.symm).trans (normalized_responses D R W a ‖c‖ u).2

theorem frameResponse_zero {N m : ℕ} (F : BlockFrame N m) (back : Bool) (v : Vec N)
    (hc : frameComplement F back v = 0) (z z' : S m) :
    frameResponse F back v z = frameResponse F back v z' := by
  rcases F with ⟨r,hr,D,R⟩
  subst N
  change queryComplement (m := m) (r := r) (queryFrame back D R) v = 0 at hc
  change responseFromSphere (queryFrame back D R) (queryFrame back R D) v z =
    responseFromSphere (queryFrame back D R) (queryFrame back R D) v z'
  simp [responseFromSphere, hc,encodeResponse]

private theorem castOfHEq {a b : ℕ} (e : a=b) {A : O a} {B : O b}
    (h : HEq A B) : castOrthogonal e A = B := by subst b; exact eq_of_heq h

theorem frame_reconstruct {N n : ℕ} (F : BlockFrame N (n+2)) (Q : S (n+2) → O (n+2))
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (back : Bool) (v : Vec N) (W : O (n+2)) :
    let p := selectedHaarStep Q hfirst back (frameUnit F back v) W
    F.realize W = (frameAfter F Q back v p.1).realize p.2 := by
  rcases F with ⟨r,hr,D,R⟩
  subst N
  let u := frameUnit (⟨r,rfl,D,R⟩ : BlockFrame ((n+2)+r) (n+2)) back v
  let e : (n+1)+(r+1) = (n+2)+r := by omega
  have hblock (V : O (n+1)) : castOrthogonal e (prefixEmbed (n+1) (r+1) V) =
      prefixEmbed (n+2) r (residualEmbed (n+1) V) :=
    castOfHEq e (prefixEmbed_next r V).symm
  cases back
  · change framed D R W = extendFrame R (Q (rotate W u)) *
        castOrthogonal e (prefixEmbed (n+1) (r+1) (extractResidual Q hfirst u W)) *
        (extendFrame D (Q u))⁻¹
    rw [hblock,residualEmbed_extractResidual]
    simp only [framed,extendFrame,map_mul,map_inv,_root_.mul_inv_rev]
    group
  · change framed D R W = extendFrame R (Q u) *
        castOrthogonal e (prefixEmbed (n+1) (r+1) (extractResidual Q hfirst u W⁻¹)⁻¹) *
        (extendFrame D (Q (rotate W⁻¹ u)))⁻¹
    rw [hblock,residualEmbed_extractResidual_inverse]
    simp only [framed,extendFrame,map_mul,map_inv,_root_.mul_inv_rev]
    group

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
