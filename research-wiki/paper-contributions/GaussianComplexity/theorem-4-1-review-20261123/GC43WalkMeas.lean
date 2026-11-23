import GC43WalkStarts
import GC43FrameMeasurable
import GC43ConsLaw

open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
noncomputable section

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
variable {N : ℕ} {State H : Type*} [MeasurableSpace State] [MeasurableSpace H]

theorem measurable_ambientGaussian {m : ℕ} {F : H → BlockFrame N m}
    {x : H → E N} {z : H → S m} (hD : Measurable fun h => (F h).domain)
    (hx : Measurable x) (hz : Measurable z) :
    Measurable fun h => ambientGaussian (F h) (x h) (z h) := by
  apply measurable_frameFamily F (fun h f => ambientGaussian f (x h) (z h))
  intro r e
  subst N
  have hv := (PiLp.continuous_ofLp 2 (fun _ : Fin (m+r) => ℝ)).measurable.comp hx
  exact (PiLp.continuous_toLp 2 (fun _ : Fin (m+r) => ℝ)).measurable.comp
    (measurable_encodeResponse hD ((continuous_exposedCoords m r).measurable.comp hv)
      (((PiLp.continuous_toLp 2 (fun _ : Fin m => ℝ)).measurable.comp
        ((continuous_residualCoords m r).measurable.comp hv)).norm) hz)

theorem measurable_perStepStart {m : ℕ} [NeZero m] {F : H → BlockFrame N m}
    (b : Bool) {x : H → E N} {z : H → S m} {v : H → Vec N}
    (hD : Measurable fun h => (F h).domain) (hR : Measurable fun h => (F h).range)
    (hv : Measurable v) (hx : Measurable x) (hz : Measurable z) :
    Measurable fun h => perStepStart (F h) b (v h) (x h) (z h) := by
  classical
  cases b
  · simpa [perStepStart] using hx
  · simp only [perStepStart,true_and]
    exact Measurable.ite
      ((measurableSet_singleton (0 : E m)).compl.preimage
        (measurable_frameComplement hD hR measurable_const hv))
      (measurable_ambientGaussian hD hx hz) hx

theorem measurable_cons_family {k : ℕ} {f : H → E N} {g : H → Fin k → E N}
    (hf : Measurable f) (hg : Measurable g) :
    Measurable (fun h => Fin.cons (α := fun _ : Fin (k+1) => E N) (f h) (g h)) :=
  (consLaw (n := k) (stdGaussian (E N))).measurable.comp (hf.prodMk hg)

theorem measurable_frameObservation_fixed {m : ℕ} [NeZero m] {F : H → BlockFrame N m}
    (b : Bool) {v : H → Vec N} {W : H → O m} (hD : Measurable fun h => (F h).domain)
    (hR : Measurable fun h => (F h).range) (hv : Measurable v)
    (hW : Measurable W) : Measurable (fun h => frameObservation (F h) b (v h) (W h)) := by
  have hu : Measurable fun h => frameUnit (F h) b (v h) :=
    measurable_frameUnit (F := F) (b := fun _ => b) (v := v) hD hR measurable_const hv
  have hm : Measurable (fun h => if b then (W h)⁻¹ else W h) := by
    cases b <;> first | exact hW | exact hW.inv
  let G (h : H) : O m × S m := (if b then (W h)⁻¹ else W h, frameUnit (F h) b (v h))
  have hG : Measurable G := hm.prodMk hu
  let L (p : O m × S m) : S m := rotate p.1 p.2
  have hL : Measurable L := (continuous_rotate (n := m)).measurable
  change Measurable (L ∘ G)
  exact hL.comp hG

theorem measurable_reveal_fixed {n : ℕ} {F : H → BlockFrame N (n+2)}
    (b : Bool) {v : H → Vec N} {W : H → O (n+2)} (hD : Measurable fun h => (F h).domain)
    (hR : Measurable fun h => (F h).range) (hv : Measurable v) (hW : Measurable W) :
    Measurable (fun h => reveal (F h) b (v h) (W h)) := by
  let G (h : H) : S (n+2) × O (n+2) := (frameUnit (F h) b (v h), W h)
  have hu : Measurable fun h => frameUnit (F h) b (v h) :=
    measurable_frameUnit (F := F) (b := fun _ => b) (v := v) hD hR measurable_const hv
  have hG : Measurable G := hu.prodMk hW
  let L (p : S (n+2) × O (n+2)) := selectedHaarStep (sectionQ n) (sectionQ_col n) b p.1 p.2
  have hL : Measurable L := measurable_selectedHaarStep _ (sectionQ_meas n) (sectionQ_col n) b
  change Measurable (L ∘ G)
  exact hL.comp hG

set_option maxHeartbeats 900000 in
theorem measurable_startArray (P : Program N State) (clock fuel : ℕ) {m : ℕ}
    (room : fuel ≤ m) {F : H → BlockFrame N m} {s : H → State} {W : H → O m}
    {z : H → Fin fuel → E N} (hD : Measurable fun h => (F h).domain)
    (hR : Measurable fun h => (F h).range) (hs : Measurable s) (hW : Measurable W)
    (hz : Measurable z) :
    Measurable (fun h => startArray P clock fuel (F h) (s h) (W h) (z h)) := by
  classical
  induction fuel generalizing clock m s with
  | zero => exact measurable_pi_lambda _ (fun i => Fin.elim0 i)
  | succ k ih =>
    have hz0 : Measurable (fun h => z h 0) := (measurable_pi_apply _).comp hz
    have hzt : Measurable (fun h => Fin.tail (z h)) :=
      measurable_pi_lambda _ (fun i => (measurable_pi_apply i.succ).comp hz)
    let b := P.back clock
    let v := fun h => P.vector clock (s h)
    have hv : Measurable v := (P.measurable_vector clock).comp hs
    cases m with
    | zero => omega
    | succ m =>
      cases m with
      | zero =>
        have hobs : Measurable (fun h => frameObservation (F h) b (v h) (W h)) :=
          measurable_frameObservation_fixed (F := F) b (W := W) hD hR hv hW
        have hy := measurable_frameResponse (F := F) hD hR (measurable_const (a := b)) hv hobs
        simp_rw [startArray_one]
        exact measurable_cons_family (measurable_perStepStart b hD hR hv hz0 hobs)
          (ih (clock+1) (by omega) hD hR ((P.measurable_update clock).comp (hs.prodMk hy)) hW hzt)
      | succ n =>
        let read := fun h => reveal (F h) b (v h) (W h)
        have hm : Measurable read := measurable_reveal_fixed (F := F) b (v := v) (W := W) hD hR hv hW
        let freeze := fun h => frameResponse (F h) b (v h) (coordinatePoint 0)
        have hf : Measurable freeze := measurable_frameResponse hD hR (measurable_const (a := b)) hv measurable_const
        let next := fun h => frameAfter (F h) (sectionQ n) b (v h) (read h).1
        have hp := measurable_frameAfter (F := F) (sectionQ n) (sectionQ_meas n) hD hR
          (measurable_const (a := b)) hv hm.fst
        have hy := measurable_frameResponse (F := F) hD hR (measurable_const (a := b)) hv hm.fst
        have htail := ih (clock+1) (m := n+1) (by omega) hp.1 hp.2
          ((P.measurable_update clock).comp (hs.prodMk hy)) hm.snd hzt
        have hold := ih (clock+1) (m := n+2) (by omega) hD hR
          ((P.measurable_update clock).comp (hs.prodMk hf)) hW hzt
        let bad := {h | frameComplement (F h) b (v h) = 0}
        have hb : MeasurableSet bad := (measurableSet_singleton (0 : E (n+2))).preimage
          (measurable_frameComplement hD hR (measurable_const (a := b)) hv)
        let dec : DecidablePred (fun h => h ∈ bad) := Classical.decPred _
        have hboth := @Measurable.ite _ _ _ _ _ _ (fun h => h ∈ bad) dec hb (measurable_cons_family hz0 hold)
          (measurable_cons_family (measurable_perStepStart b hD hR hv hz0 hm.fst) htail)
        convert hboth using 1
        funext h
        by_cases hbad : h ∈ bad
        · rw [if_pos hbad]
          exact startArray_determined P clock k (F h) (s h) (W h) _ hbad
        · rw [if_neg hbad]
          exact startArray_informative P clock k (F h) (s h) (W h) _ hbad

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
