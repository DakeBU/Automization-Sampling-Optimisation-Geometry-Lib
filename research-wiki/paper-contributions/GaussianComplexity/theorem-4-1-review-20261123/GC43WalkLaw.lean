import GC43WalkMeas
import GC43Fubini

noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

variable {N : ℕ} {State : Type*} [MeasurableSpace State]

theorem perStepStart_law {m : ℕ} [NeZero m] (F : BlockFrame N m) (b : Bool) (v : Vec N) :
    MeasurePreserving (fun p : E N × S m => perStepStart F b v p.1 p.2)
      ((stdGaussian (E N)).prod (sphereProbability m)) (stdGaussian (E N)) := by
  classical
  have hm := measurable_perStepStart (F := fun _ : E N × S m => F) b measurable_const
    measurable_const (measurable_const (a := v)) measurable_fst measurable_snd
  refine ⟨hm,?_⟩
  by_cases h : b = true ∧ frameComplement F b v ≠ 0
  · simp only [perStepStart, if_pos h]
    change ((stdGaussian (E N)).prod (sphereProbability m)).map (Function.uncurry (ambientGaussian F)) = _
    exact ambientGaussian_law F
  · let := isProbabilityMeasure_sphereProbability m
    simp only [perStepStart, if_neg h, Measure.map_fst_prod, measure_univ, one_smul]

set_option maxHeartbeats 1400000 in
theorem walk_starts_law (P : Program N State) (clock fuel : ℕ) {m : ℕ} (room : fuel ≤ m)
    (F : BlockFrame N m) (s : State) :
    MeasurePreserving
      (fun p : O m × (Fin fuel → E N) => startArray P clock fuel F s p.1 p.2)
      ((orthogonalHaar m).prod (Measure.pi (fun _ : Fin fuel => stdGaussian (E N))))
      (Measure.pi (fun _ : Fin fuel => stdGaussian (E N))) := by
  classical
  let γ := stdGaussian (E N)
  let Z := fun k : ℕ => Measure.pi (fun _ : Fin k => γ)
  induction fuel generalizing m clock s with
  | zero =>
    let := (orthogonalHaar_spec m).1
    have h : MeasurePreserving (Prod.snd : O m × (Fin 0 → E N) → _)
        ((orthogonalHaar m).prod (Z 0)) (Z 0) := measurePreserving_snd
    have he : (fun p : O m × (Fin 0 → E N) => startArray P clock 0 F s p.1 p.2) = Prod.snd := by
      funext p i; exact Fin.elim0 i
    rw [he]
    exact h
  | succ k ih =>
    let v := P.vector clock s
    let b := P.back clock
    cases m with
    | zero => omega
    | succ m =>
      cases m with
      | zero =>
        obtain rfl : k = 0 := by omega
        let := (orthogonalHaar_spec 1).1
        let := isProbabilityMeasure_sphereProbability 1
        have hread := full_haar_observation F b v
        have hz := measurePreserving_eval (fun _ : Fin 1 => γ) (0 : Fin 1)
        have h := (perStepStart_law F b v).comp
          ((Measure.measurePreserving_swap (μ := sphereProbability 1) (ν := γ)).comp (hread.prod hz))
        have hout := (measurePreserving_piUnique (fun _ : Fin 1 => γ)).symm.comp h
        convert hout using 1
        funext p i
        have hi : i = 0 := Fin.ext (by have := i.isLt; omega)
        subst i
        rw [startArray_one, Fin.cons_zero]
        rfl
      | succ n =>
        let η := orthogonalHaar (n+2)
        let := (orthogonalHaar_spec (n+2)).1
        let := (orthogonalHaar_spec (n+1)).1
        let := isProbabilityMeasure_sphereProbability (n+2)
        by_cases hc : frameComplement F b v = 0
        · let next := P.update clock s (frameResponse F b v (coordinatePoint 0))
          let t := fun p : E N × (O (n+2) × (Fin k → E N)) =>
            startArray P (clock+1) k F next p.2.1 p.2.2
          have ht : Measurable t := measurable_startArray P (clock+1) k (by omega)
            (F := fun _ => F) measurable_const measurable_const measurable_const
            (measurable_fst.comp measurable_snd) (measurable_snd.comp measurable_snd)
          have hcond (x : E N) : (η.prod (Z k)).map (fun p => t (x,p)) = Z k :=
            (ih (clock := clock+1) (m := n+2) (by omega) F next).map_eq
          have htail := consLaw_of_constant_fibers γ (η.prod (Z k)) γ id t
            (MeasurePreserving.id γ) ht (.of_forall hcond)
          have h := htail.comp (split_noise (k := k) η γ)
          convert h using 1
          funext p
          exact startArray_determined P clock k F s p.1 p.2 hc
        · let σ := sphereProbability (n+2)
          let ν := orthogonalHaar (n+1)
          let u := frameUnit F b v
          let read := reveal F b v
          have hread : MeasurePreserving read η (σ.prod ν) :=
            ⟨Measurable.of_uncurry_left (f := selectedHaarStep (sectionQ n) (sectionQ_col n) b)
                (measurable_selectedHaarStep (sectionQ n) (sectionQ_meas n) (sectionQ_col n) b) (x := u),
              full_haar_step_law (sectionQ n) (sectionQ_meas n) (sectionQ_col n) (sectionQ_det n) b u⟩
          let T := (E N × S (n+2)) × (O (n+1) × (Fin k → E N))
          let next := fun z => frameAfter F (sectionQ n) b v z
          let st := fun z => P.update clock s (frameResponse F b v z)
          let tail := fun p : T => startArray P (clock+1) k (next p.1.2) (st p.1.2) p.2.1 p.2.2
          have hz : Measurable (fun p : T => p.1.2) := measurable_snd.comp measurable_fst
          have hF := measurable_frameAfter (F := fun _ : T => F) (sectionQ n) (sectionQ_meas n)
            measurable_const measurable_const (measurable_const (a := b)) (measurable_const (a := v)) hz
          have hy := measurable_frameResponse (F := fun _ : T => F) measurable_const measurable_const
            (measurable_const (a := b)) (measurable_const (a := v)) hz
          have ht : Measurable tail := measurable_startArray P (clock+1) k (by omega)
            hF.1 hF.2 ((P.measurable_update clock).comp (measurable_const.prodMk hy))
            (measurable_fst.comp measurable_snd) (measurable_snd.comp measurable_snd)
          have hcond (a : E N × S (n+2)) :
              (ν.prod (Z k)).map (fun p => tail (a,p)) = Z k :=
            (ih (clock := clock+1) (m := n+1) (by omega) (next a.2) (st a.2)).map_eq
          have htail := consLaw_of_constant_fibers (γ.prod σ) (ν.prod (Z k)) γ
            (fun p => perStepStart F b v p.1 p.2) tail (perStepStart_law F b v) ht (.of_forall hcond)
          have h := htail.comp (split_informative (k := k) η γ σ ν read hread)
          convert h using 1
          funext p
          exact startArray_informative P clock k F s p.1 p.2 hc

#print axioms walk_starts_law
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
