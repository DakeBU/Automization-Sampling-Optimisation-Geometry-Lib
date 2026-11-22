import B3PrimitiveQuery

/-!
# Fixed ambient frames for one primitive query

In the backward proof of Zhou–Suzuki, Lemma B.4, a queried block may
expose one auxiliary unit direction even when the query has zero
residual component. Its ambient response is then constant in the sphere
observation. One residual dimension per query suffices under the cap.
-/

open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarStabilizerBlock
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

/-- Domain and range frames in a fixed ambient space with `d` residual coordinates. -/
structure BlockFrame (N d : ℕ) where
  rank : ℕ
  fits : d + rank = N
  domain : O N
  range : O N

namespace BlockFrame

variable {N d : ℕ}

/-- Decode a residual matrix into the original ambient oracle. -/
noncomputable def realize (F : BlockFrame N d) (W : O d) : O N :=
  F.range * castOrthogonal F.fits (prefixEmbed d F.rank W) * F.domain⁻¹

theorem measurable_realize (F : BlockFrame N d) : Measurable F.realize := by
  rcases F with ⟨r, hr, D, R⟩
  subst N
  exact ((continuous_const.mul (continuous_prefixEmbed d r)).mul_const D⁻¹).measurable

def initial (N : ℕ) : BlockFrame N N := ⟨0, rfl, 1, 1⟩

@[simp] theorem initial_realize (N : ℕ) (W : O N) : (initial N).realize W = W := by
  change 1 * W * (1 : O N)⁻¹ = W
  simp

private theorem castOrthogonal_of_heq {a b : ℕ} (e : a = b) {A : O a} {B : O b}
    (h : HEq A B) : castOrthogonal e A = B := by
  subst b
  exact eq_of_heq h

private theorem exists_direction {m : ℕ} [NeZero m] (c : E m) :
    ∃ u : S m, ‖c‖ • WithLp.ofLp u.val = WithLp.ofLp c := by
  by_cases hc : c = 0
  · exact ⟨coordinatePoint 0, by simp [hc]⟩
  · exact ⟨residualUnit ⟨c,hc⟩, scaled_residualUnit ⟨c,hc⟩⟩

/-- At a fixed public state, generate the query answer and the next frame
from the uniform direction alone. Reinserting any smaller residual gives
the identical ambient oracle and returns that answer, for either query sense. -/
theorem split_query {n : ℕ} (F : BlockFrame N (n+2)) (v : Vec N) (back : Bool)
    (Q : S (n+2) → O (n+2))
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val) :
    ∃ u : S (n+2), ∃ y : S (n+2) → Vec N, Measurable y ∧
      ∃ next : S (n+2) → BlockFrame N (n+1), ∀ (z : S (n+2)) (V : O (n+1)),
        let W := if back then (assemble Q u z V⁻¹)⁻¹ else assemble Q u z V
        F.realize W = (next z).realize V ∧
          (if back then act (F.realize W)⁻¹ v else act (F.realize W) v) = y z := by
  rcases F with ⟨r, hr, D, R⟩
  subst N
  let input := queryFrame back D R
  let output := queryFrame back R D
  let a := exposedCoords (n+2) r (act input⁻¹ v)
  let c := queryComplement (m := n+2) (r := r) input v
  obtain ⟨u, hu⟩ := exists_direction c
  let y := encodeResponse output a ‖c‖
  have hv : act input (splitVec r a (‖c‖ • WithLp.ofLp u.val)) = v := by
    rw [hu]
    exact query_from_coordinates input v
  have hy : Measurable y :=
    measurable_encodeResponse measurable_const measurable_const measurable_const measurable_id
  have hQ (z : S (n+2)) : rotate (Q z) (coordinatePoint 0) = z :=
    (first_column_iff_rotate_coordinate 0 _ z).mp (hfirst z)
  have he : (n+1)+(r+1) = (n+2)+r := by omega
  have hblock (V : O (n+1)) : castOrthogonal he (prefixEmbed (n+1) (r+1) V) =
      prefixEmbed (n+2) r (residualEmbed (n+1) V) :=
    castOrthogonal_of_heq he (prefixEmbed_next r V).symm
  refine ⟨u, y, hy, ?_⟩
  cases back
  · refine ⟨fun z => ⟨r+1, he, extendFrame D (Q u), extendFrame R (Q z)⟩, ?_⟩
    intro z V
    constructor
    · change framed D R (assemble Q u z V) =
        extendFrame R (Q z) * castOrthogonal he (prefixEmbed (n+1) (r+1) V) * (extendFrame D (Q u))⁻¹
      rw [hblock]
      exact forward_frame_update D R Q u z V
    · change act (framed D R (assemble Q u z V)) v = encodeResponse R a ‖c‖ z
      have ho := (normalized_responses D R (assemble Q u z V) a ‖c‖ u).1
      rw [assemble_rotate hQ] at ho
      exact (congrArg (act (framed D R (assemble Q u z V))) hv.symm).trans ho
  · refine ⟨fun z => ⟨r+1, he, extendFrame D (Q z), extendFrame R (Q u)⟩, ?_⟩
    intro z V
    constructor
    · change framed D R (assemble Q u z V⁻¹)⁻¹ =
        extendFrame R (Q u) * castOrthogonal he (prefixEmbed (n+1) (r+1) V) * (extendFrame D (Q z))⁻¹
      rw [hblock]
      simpa only [inv_inv, framed] using inverse_frame_update D R Q u z V⁻¹
    · change act (framed D R (assemble Q u z V⁻¹)⁻¹)⁻¹ v = encodeResponse D a ‖c‖ z
      have ho := (normalized_responses D R (assemble Q u z V⁻¹)⁻¹ a ‖c‖ u).2
      rw [inv_inv, assemble_rotate hQ] at ho
      exact (congrArg (act (framed D R (assemble Q u z V⁻¹)⁻¹)⁻¹) hv.symm).trans ho

#print axioms split_query

end BlockFrame
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
