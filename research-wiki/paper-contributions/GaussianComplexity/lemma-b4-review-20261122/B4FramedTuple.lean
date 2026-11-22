import B4Frames
import B4Resample

/-!
Reconstruct every ambient matrix under the one-block resampling. At a fixed
old history the spherical observation determines the new frames; the equality
of the two tuples holds for every value of every smaller residual matrix.
-/

open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

def transportFrame {N a b : ℕ} (e : a = b) (F : BlockFrame N a) : BlockFrame N b := e ▸ F

private theorem realize_transport {N a b : ℕ} (e : a = b) (F : BlockFrame N a) (W : O b) :
    (transportFrame e F).realize W = F.realize (castOrthogonal e.symm W) := by
  subst b; rfl

private theorem realize_transport_both {N a b : ℕ} (e : a = b) (F : BlockFrame N a) (W : O a) :
    (transportFrame e F).realize (castOrthogonal e W) = F.realize W := by
  subst b; rfl

variable {k N : ℕ} {d : Fin (k+1) → ℕ}

noncomputable def ambientTuple (F : ∀ j, BlockFrame N (d j)) (w : ∀ j, O (d j)) :
    Fin (k+1) → O N := fun j => (F j).realize (w j)

theorem measurable_ambientTuple (F : ∀ j, BlockFrame N (d j)) : Measurable (ambientTuple F) :=
  measurable_pi_lambda _ fun j => (F j).measurable_realize.comp (measurable_pi_apply j)

theorem split_ambient_tuple (F : ∀ j, BlockFrame N (d j)) (i : Fin (k+1)) (n : ℕ)
    (hi : d i = n+2) (v : Vec N) (back : Bool)
    (Q : S (n+2) → O (n+2))
    (hc : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val) :
    ∃ u : S (n+2), ∃ y : S (n+2) → Vec N, Measurable y ∧
      ∃ next : S (n+2) → ∀ j, BlockFrame N (resampleDim d i n j),
      ∀ z (V : ∀ j, O (resampleDim d i n j)),
        let W := ambientTuple F (rebuildHaarTuple d i n hi Q back u z V)
        W = ambientTuple (next z) V ∧
          (if back then act (W i)⁻¹ v else act (W i) v) = y z := by
  let A := transportFrame hi (F i)
  obtain ⟨u,y,hy,B,hB⟩ := A.split_query v back Q hc
  let d' := resampleDim d i n
  have ei : d' i = n+1 := Function.update_self _ _ _
  let next (z : S (n+2)) (j : Fin (k+1)) : BlockFrame N (d' j) :=
    if hj : j = i then transportFrame ((congrArg d' hj).trans ei).symm (B z)
    else transportFrame (Function.update_of_ne hj (n+1) d).symm (F j)
  refine ⟨u, y, hy, next, ?_⟩
  intro z V
  let w := rebuildHaarTuple d i n hi Q back u z V
  let small := castOrthogonal ei (V i)
  have hselected : (F i).realize (w i) = A.realize (rebuildSelected Q back u z small) := by
    rw [← rebuildHaarTuple_selected d i n hi Q back u z V]
    exact (realize_transport_both hi (F i) (w i)).symm
  obtain ⟨hrepr, hans⟩ := hB z small
  change A.realize (rebuildSelected Q back u z small) = (B z).realize small at hrepr
  constructor
  · funext j
    by_cases hj : j = i
    · subst j
      change (F i).realize (w i) = (next z i).realize (V i)
      rw [hselected, hrepr]
      simp only [next, dif_pos rfl, realize_transport]
      rfl
    · change (F j).realize (w j) = (next z j).realize (V j)
      simp only [next, dif_neg hj, realize_transport]
      rw [show w j = _ from rebuildHaarTuple_other d i n hi Q back u z V j hj]
  · change (if back then act ((F i).realize (w i))⁻¹ v else act ((F i).realize (w i)) v) = _
    rw [hselected]
    exact hans

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
