import GC43WalkPath

open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
noncomputable section
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

variable {N : ℕ} {State : Type*} [MeasurableSpace State]

private theorem consPath {k m m' : ℕ} (P : Program N State) (clock : ℕ) (A : O N)
    (s : State) (F : BlockFrame N m) (G : BlockFrame N m') (y : Vec N) (g : E N)
    (R : Fin k → Report N State)
    (hy : y = if P.back clock then act A⁻¹ (P.vector clock s) else act A (P.vector clock s))
    (hg : P.back clock = true → y ∈ exposedSpace F.domain F.rank ⊔ ℝ ∙ g.ofLp)
    (hG : exposedSpace G.domain G.rank ≤ exposedSpace F.domain F.rank ⊔
      ℝ ∙ (if P.back clock then y else P.vector clock s))
    (hR : WalkPath P (clock+1) A (P.update clock s y) G.domain G.rank R) :
    WalkPath P clock A s F.domain F.rank (Fin.cons (emit F G s y g) R) := by
  have htime (i : Fin k) : clock+i.succ.val = (clock+1)+i.val := by simp only [Fin.val_succ]; omega
  constructor
  · intro i hi
    obtain rfl : i = 0 := Fin.ext hi
    simp [emit]
  · intro i j hij
    cases i using Fin.cases with
    | zero =>
      cases j using Fin.cases with
      | zero => simp only [Fin.val_zero] at hij; omega
      | succ j => simpa [emit] using hR.first j (by simp only [Fin.val_zero,Fin.val_succ] at hij; omega)
    | succ i =>
      cases j using Fin.cases with
      | zero => simp only [Fin.val_zero, Fin.val_succ] at hij; omega
      | succ j => simpa only [Fin.cons_succ, htime] using hR.adjacent i j (by simp only [Fin.val_succ] at hij; omega)
  · intro i
    cases i using Fin.cases with
    | zero => simpa [emit] using hy
    | succ i => simpa only [Fin.cons_succ,htime] using hR.answer i
  · intro i hi
    cases i using Fin.cases with
    | zero => simpa [emit] using hg (by simpa using hi)
    | succ i => exact hR.start_mem i (by rwa [← htime])
  · intro i
    cases i using Fin.cases with
    | zero => simpa [emit] using hG
    | succ i => simpa only [Fin.cons_succ,htime] using hR.growth i

/-- Every regular-noise run records its actual ambient queries and answers and
satisfies the one-step exposed-space inclusions throughout the run. -/
theorem walk_path (P : Program N State) (clock fuel : ℕ) {m : ℕ} (F : BlockFrame N m)
    (s : State) (W : O m) (noise : Fin fuel → E N) (hf : fuel ≤ m)
    (hr : ∀ i, Regular (noise i)) :
    WalkPath P clock (F.realize W) s F.domain F.rank (walk P clock fuel F s W noise) := by
  induction fuel generalizing clock m s with
  | zero => constructor <;> exact fun i => Fin.elim0 i
  | succ k ih =>
    cases m with
    | zero => omega
    | succ m =>
      cases m with
      | zero =>
        rw [walk]
        apply consPath
        · exact (frameAnswer_eq F _ _ W).symm
        · intro hb
          simp only [hb]
          exact frameStart_mem F _ _ (hr 0) _
        · exact le_sup_left
        · exact ih _ F _ W _ (by omega) (fun i => hr i.succ)
      | succ n =>
        classical
        let b := P.back clock
        let v := P.vector clock s
        let u := frameUnit F b v
        let p := selectedHaarStep (sectionQ n) (sectionQ_col n) b u W
        let G := frameAfter F (sectionQ n) b v p.1
        let y := frameResponse F b v p.1
        have hp : p.1 = frameObservation F b v W := by cases h : b <;> simp [p,selectedHaarStep,frameObservation,u,h]
        have hy : y = if b then act (F.realize W)⁻¹ v else act (F.realize W) v := by
          exact (congrArg (frameResponse F b v) hp).trans (frameAnswer_eq F b v W).symm
        have herr := frame_reconstruct F (sectionQ n) (sectionQ_col n) b v W
        change F.realize W = G.realize p.2 at herr
        rw [walk]
        split_ifs with hc
        · apply consPath
          · exact hy
          · intro hb
            change frameComplement F b v = 0 at hc
            change b = true at hb
            have hper : perStepStart F b v (noise 0) p.1 = noise 0 := by simp [perStepStart, hc]
            change frameResponse F b v p.1 ∈ exposedSpace F.domain F.rank ⊔ ℝ ∙ (noise 0).ofLp
            rw [← hper, hb]
            exact frameStart_mem F v _ (hr 0) _
          · exact le_sup_left
          · exact ih _ F _ W _ (by omega) (fun i => hr i.succ)
        · apply consPath
          · exact hy
          · intro hb
            change b = true at hb
            change y ∈ exposedSpace F.domain F.rank ⊔ ℝ ∙ (perStepStart F b v (noise 0) p.1).ofLp
            dsimp only [y]
            rw [hb]
            exact frameStart_mem F v _ (hr 0) _
          · exact frameAfter_exposed_le F _ (sectionQ_col n) b v p.1 hc
          · rw [herr]
            exact ih _ G _ p.2 _ (by omega) (fun i => hr i.succ)

#print axioms walk_path
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
