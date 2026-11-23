import GC43Flow

noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

variable {N : ℕ} {State : Type*} [MeasurableSpace State]

def startArray (P : Program N State) (clock fuel : ℕ) {m : ℕ} (F : BlockFrame N m)
    (s : State) (W : O m) (z : Fin fuel → E N) : Fin fuel → E N :=
  fun i => (walk P clock fuel F s W z i).start

def reveal {N n : ℕ} (F : BlockFrame N (n+2)) (back : Bool) (v : Vec N) (W : O (n+2)) :=
  selectedHaarStep (sectionQ n) (sectionQ_col n) back (frameUnit F back v) W

theorem startArray_one (P : Program N State) (clock k : ℕ) (F : BlockFrame N 1)
    (s : State) (W : O 1) (noise : Fin (k+1) → E N) :
    let v := P.vector clock s
    let b := P.back clock
    let z := frameObservation F b v W
    let y := frameResponse F b v z
    startArray P clock (k+1) F s W noise = Fin.cons (perStepStart F b v (noise 0) z)
      (startArray P (clock+1) k F (P.update clock s y) W (Fin.tail noise)) := by
  dsimp only
  funext i
  cases i using Fin.cases <;> simp only [startArray,walk,Fin.cons_zero,Fin.cons_succ,emit]

theorem startArray_determined (P : Program N State) (clock k : ℕ) {n : ℕ} (F : BlockFrame N (n+2))
    (s : State) (W : O (n+2)) (noise : Fin (k+1) → E N)
    (hc : frameComplement F (P.back clock) (P.vector clock s) = 0) :
    let v := P.vector clock s
    let b := P.back clock
    let y := frameResponse F b v (coordinatePoint 0)
    startArray P clock (k+1) F s W noise = Fin.cons (noise 0)
      (startArray P (clock+1) k F (P.update clock s y) W (Fin.tail noise)) := by
  dsimp only
  have hy := frameResponse_zero F _ _ hc (reveal F (P.back clock) (P.vector clock s) W).1 (coordinatePoint 0)
  funext i
  cases i using Fin.cases <;> simp only [startArray,walk,if_pos hc,Fin.cons_zero,Fin.cons_succ,emit]
  rw [show frameResponse F (P.back clock) (P.vector clock s)
      ((selectedHaarStep (sectionQ n) (sectionQ_col n) (P.back clock)
        (frameUnit F (P.back clock) (P.vector clock s)) W).1) = _ from hy]

theorem startArray_informative (P : Program N State) (clock k : ℕ) {n : ℕ} (F : BlockFrame N (n+2))
    (s : State) (W : O (n+2)) (noise : Fin (k+1) → E N)
    (hc : frameComplement F (P.back clock) (P.vector clock s) ≠ 0) :
    let v := P.vector clock s
    let b := P.back clock
    let p := reveal F b v W
    let y := frameResponse F b v p.1
    let F' := frameAfter F (sectionQ n) b v p.1
    startArray P clock (k+1) F s W noise = Fin.cons (perStepStart F b v (noise 0) p.1)
      (startArray P (clock+1) k F' (P.update clock s y) p.2 (Fin.tail noise)) := by
  dsimp only
  funext i
  cases i using Fin.cases <;> simp only [startArray,walk,if_neg hc,Fin.cons_zero,Fin.cons_succ,emit,reveal]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
