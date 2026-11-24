import GC3AmbientKernel
import GC3TraceFrames
import B4FramedTuple

/-! A visible informative answer determines both new ambient frames of the chosen block. -/
noncomputable section
open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
variable {N k n : ℕ}

theorem readFrame_cast (F : PublicFrame N) {a c : ℕ} (e : a=c) (w : O a) :
    readFrame F c (castOrthogonal e w) = readFrame F a w := by subst c; rfl

theorem tag_transport (F : PublicFrame N) {m : ℕ} (e : F.1=m) :
    (⟨m,transportFrame e F.2⟩ : PublicFrame N) = F := by
  rcases F with ⟨d,F⟩; dsimp only at e; subst m; rfl

def afterFrames (F : Frames (k+1) N) (i : Fin (k+1)) (G : BlockFrame N (n+2))
    (back : Bool) (v : Vec N) (z : S (n+2)) : Frames (k+1) N :=
  Function.update F i ⟨n+1, frameAfter G (sectionQ n) back v z⟩

theorem profile_afterFrames (F : Frames (k+1) N) (i : Fin (k+1)) (G : BlockFrame N (n+2))
    (back : Bool) (v : Vec N) (z : S (n+2)) :
    profile (afterFrames F i G back v z) = resampleDim (profile F) i n := by
  ext j
  by_cases h : j=i
  · subst j; simp [profile,afterFrames,resampleDim]
  · simp [profile,afterFrames,resampleDim,Function.update_of_ne h]

theorem updateRecord_informative_eq (F : Frames (k+1) N) (i : Fin (k+1))
    (G : BlockFrame N (n+2)) (he : (⟨n+2,G⟩ : PublicFrame N) = F i)
    (back : Bool) (v : Vec N) (hc : frameComplement G back v ≠ 0) (z : S (n+2)) :
    PublicFrame.updateRecord F (some ((i,v,back), frameResponse G back v z)) =
      afterFrames F i G back v z := by
  simp only [PublicFrame.updateRecord,afterFrames]
  rw [← he,PublicFrame.recordStep_informative _ _ _ _ hc,PublicFrame.observed_response _ _ _ _ hc]

theorem updateRecord_determined_eq (F : Frames (k+1) N) (i : Fin (k+1))
    (G : BlockFrame N (n+2)) (he : (⟨n+2,G⟩ : PublicFrame N) = F i)
    (back : Bool) (v : Vec N) (hc : frameComplement G back v = 0) (y : Vec N) :
    PublicFrame.updateRecord F (some ((i,v,back), y)) = F := by
  simp only [PublicFrame.updateRecord]
  rw [← he, PublicFrame.recordStep_zero _ _ _ _ hc,he,Function.update_eq_self]

theorem read_selected (F : Frames (k+1) N) (i : Fin (k+1))
    (hi : profile F i = n+2) (w : ResidualTuple (profile F)) :
    decodeAt (profile F) F w i =
      (transportFrame hi (F i).2).realize (castOrthogonal hi (w i)) := by
  let G := transportFrame hi (F i).2
  change readFrame (F i) (profile F i) (w i) = _
  rw [← readFrame_cast (F i) hi]
  exact (congrArg (fun f : PublicFrame N => readFrame f (n+2) (castOrthogonal hi (w i)))
    (tag_transport (F i) hi).symm).trans (readFrame_tag _ _)

theorem query_answer (W : Ambient (k+1) N) (i : Fin (k+1)) (v : Vec N) (b : Bool) :
    oracleAnswer W (i,v,b) = (if b then act (W i)⁻¹ v else act (W i) v) := by
  cases b <;> rfl

theorem regenerated_block (G : BlockFrame N (n+2)) (back : Bool) (v : Vec N)
    (z : S (n+2)) (V : O (n+1)) :
    let A := rebuildSelected (sectionQ n) back (frameUnit G back v) z V
    G.realize A = (frameAfter G (sectionQ n) back v z).realize V ∧
    (if back then act (G.realize A)⁻¹ v else act (G.realize A) v) = frameResponse G back v z := by
  let u := frameUnit G back v
  let A := rebuildSelected (sectionQ n) back u z V
  have h := update_rebuildSelected (sectionQ n) (sectionQ_col n) back u z V
  have hz : frameObservation G back v A = z := by
    cases back <;> exact congrArg Prod.fst h
  have hv := frame_reconstruct G (sectionQ n) (sectionQ_col n) back v A
  change G.realize A = (frameAfter G (sectionQ n) back v _).realize _ at hv
  rw [show selectedHaarStep (sectionQ n) (sectionQ_col n) back (frameUnit G back v) A = (z,V) from h] at hv
  exact ⟨hv, (frameAnswer_eq G back v A).trans (congrArg _ hz)⟩

theorem regenerated_tuple (F : Frames (k+1) N) (i : Fin (k+1)) (hi : profile F i = n+2)
    (back : Bool) (v : Vec N) (z : S (n+2)) (V : ResidualTuple (resampleDim (profile F) i n)) :
    let G := transportFrame hi (F i).2
    let W := decodeAt (profile F) F (rebuildHaarTuple (profile F) i n hi (sectionQ n) back
      (frameUnit G back v) z V)
    W = decodeAt (resampleDim (profile F) i n) (afterFrames F i G back v z) V ∧
      oracleAnswer W (i,v,back) = frameResponse G back v z := by
  let G := transportFrame hi (F i).2
  let u := frameUnit G back v
  let w := rebuildHaarTuple (profile F) i n hi (sectionQ n) back u z V
  let e := Function.update_self i (n+1) (profile F)
  have hs : decodeAt (profile F) F w i = G.realize
      (rebuildSelected (sectionQ n) back u z (castOrthogonal e (V i))) := by
    exact (read_selected F i hi w).trans (congrArg G.realize
      (rebuildHaarTuple_selected (profile F) i n hi (sectionQ n) back u z V))
  have h := regenerated_block G back v z (castOrthogonal e (V i))
  constructor
  · funext j
    by_cases hj : j=i
    · subst j
      rw [hs,h.1]
      change _ = readFrame ((afterFrames F i G back v z) i) _ _
      rw [← readFrame_cast _ e]
      let f := frameAfter G (sectionQ n) back v z
      change f.realize _ = readFrame (Function.update F i ⟨n+1,f⟩ i) (n+1) _
      exact (readFrame_tag f _).symm.trans (congrArg
        (fun A : PublicFrame N => readFrame A (n+1) (castOrthogonal e (V i)))
        (Function.update_self i ⟨n+1,f⟩ F).symm)
    · change readFrame (F j) _ (w j) = readFrame ((afterFrames F i G back v z) j) _ (V j)
      dsimp only [w]
      rw [rebuildHaarTuple_other _ _ _ _ _ _ _ _ _ _ hj, readFrame_cast]
      unfold afterFrames
      exact congrArg (fun f : PublicFrame N => readFrame f _ (V j))
        (Function.update_of_ne hj (⟨n+1,frameAfter G (sectionQ n) back v z⟩ : PublicFrame N) F).symm
  · rw [query_answer,hs]
    exact h.2

end AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
