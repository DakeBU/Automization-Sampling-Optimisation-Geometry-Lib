import B3TaggedInduction
import HaarOrientedSection

open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarOrientedSection
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

namespace TaggedFiniteConsumer

abbrev H (t : ℕ) := QueryHistory Unit (fun _ => S 3) t
abbrev Chart (t : ℕ) := ResidualChart (H t) (S 3) 2
abbrev Policy := TaggedQueryPolicy Unit (fun _ => S 3) Bool 2
private noncomputable def Q := (exists_measurable_oriented_section 1).choose
private theorem hQ : Measurable Q := (exists_measurable_oriented_section 1).choose_spec.1
private theorem hdet (z : S 3) : (Q z).val.det = 1 :=
  ((exists_measurable_oriented_section 1).choose_spec.2 z).1
private theorem hfirst (z : S 3) :
    (Q z).val *ᵥ Pi.single (0 : Fin 3) 1 = WithLp.ofLp z.val :=
  ((exists_measurable_oriented_section 1).choose_spec.2 z).2

noncomputable def hemisphere (z : S 3) : Bool :=
  if 0 < WithLp.ofLp z.val 0 then true else false

private theorem measurable_hemisphere : Measurable hemisphere := by
  have hz : Measurable (fun z : S 3 => WithLp.ofLp z.val 0) :=
    (measurable_pi_apply (0 : Fin 3)).comp ((PiLp.continuous_ofLp 2 (fun _ : Fin 3 => ℝ)).measurable.comp
      measurable_subtype_coe)
  exact Measurable.ite (measurableSet_lt measurable_const hz) measurable_const measurable_const

private def firstAnswer : (t : ℕ) → H (t+1) → S 3
  | 0, h => h.2
  | t+1, h => firstAnswer t h.1

private theorem measurable_firstAnswer : (t : ℕ) → Measurable (firstAnswer t)
  | 0 => measurable_snd
  | t+1 => (measurable_firstAnswer t).comp measurable_fst

private noncomputable def block0 : Chart 0 :=
  informativeChart (k := 1) ![3, 3] (by decide) 0 1 (by decide) Q hQ hfirst hdet
    (fun _ => false) measurable_const (fun _ => coordinatePoint 0) measurable_const
    (fun _ z => z) measurable_snd

private noncomputable def block1 : Chart 1 :=
  informativeChart (k := 1) ![2, 3] (by decide) 1 1 (by decide) Q hQ hfirst hdet
    (fun _ => true) measurable_const (fun _ => coordinatePoint 0) measurable_const
    (fun _ z => z) measurable_snd

private noncomputable def idle (t : ℕ) (b : Bool) : Chart t :=
  if b then determinedChart ![2, 2] (by decide) (fun _ => coordinatePoint 0) measurable_const
  else determinedChart ![2, 3] (by decide) (fun _ => coordinatePoint 0) measurable_const

noncomputable def policy : Policy where
  charts
    | 0, _ => block0
    | 1, b => if b then block1 else idle 1 false
    | t+2, b => idle (t+2) b
  pick
    | 0, _ => false
    | t+1, h => hemisphere (firstAnswer t h)
  measurable_pick
    | 0 => measurable_const
    | t+1 => measurable_hemisphere.comp (measurable_firstAnswer t)

theorem fits : policy.Fits (Measure.dirac ()) ![3, 3] := by
  constructor
  · exact ae_of_all _ fun _ => rfl
  · intro t
    apply ae_of_all
    intro h
    cases t with
    | zero =>
      change (if hemisphere h.2 then block1 else idle 1 false).before = block0.after
      cases hemisphere h.2 <;> decide
    | succ t =>
      cases t with
      | zero =>
        change (idle 2 (hemisphere h.1.2)).before = (if hemisphere h.1.2 then block1 else idle 1 false).after
        cases hemisphere h.1.2 <;> decide
      | succ t =>
        change (idle (t+3) (hemisphere (firstAnswer (t+1) h.1))).before =
          (idle (t+2) (hemisphere (firstAnswer (t+1) h.1))).after
        cases hemisphere (firstAnswer (t+1) h.1) <;> rfl

/-- The first full sphere response decides if a second block is queried by its
transpose or receives padding. The finite transcript laws agree for all times. -/
theorem finite_transcript (t : ℕ) :
    ((Measure.dirac ()).prod (taggedHaar ![3, 3] (-1))).map (fun w => (policy.evolution.run t w).1) =
      ((Measure.dirac ()).prod (taggedHaar ![3, 3] 1)).map (fun w => (policy.evolution.run t w).1) :=
  policy.signs_same_history _ _ (by decide) fits t

#print axioms finite_transcript
end TaggedFiniteConsumer
