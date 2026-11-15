import AutoSamplingTheory.TechnicalLemmas.Probability.AdaptiveOracleSimulation
import Tests.GaussianComplexityAdaptiveFirstOrderSimulation
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

open MeasureTheory
open AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle
open AutoSamplingTheory.TechnicalLemmas.Probability.AdaptiveOracleSimulation

namespace R18BoundaryChecks

local instance : MeasurableSpace (Option ℝ) := MeasurableSpace.comap
  (fun x : Option ℝ => x.elim (Sum.inl () : Unit ⊕ ℝ) Sum.inr) inferInstance

private noncomputable def next (s : ℝ) : ℝ ⊕ ℝ :=
  if s ≤ 0 then .inr (-s) else .inl s

private def update (_ _ a : ℝ) : ℝ := a
private def oracle (q : ℝ) := 2*q
private def target (q : ℝ) := 3*q
private def decode (q a : ℝ) := a+q

-- The actual reply affects the state and terminal output. Both joint laws,
-- rather than only an arithmetic counter, are obtained from the new producer.
example :
    let b := fun ω : ℝ => run next (fun s q a => update s q (decode q a)) oracle 7 (-ω)
    let t := fun ω : ℝ => run next update target 7 (-ω)
    (Measure.dirac (2 : ℝ)).map b = (Measure.dirac (2 : ℝ)).map t := by
  have hn : Measurable next := by
    exact Measurable.ite (measurableSet_le measurable_id measurable_const)
      (measurable_inr.comp measurable_neg) measurable_inl
  have hu : Measurable (fun p : ℝ × ℝ × ℝ => update p.1 p.2.1 p.2.2) :=
    measurable_snd.snd
  have ho : Measurable oracle := by unfold oracle; fun_prop
  have hd : Measurable (fun p : ℝ × ℝ => decode p.1 p.2) := by unfold decode; fun_prop
  have hi : Measurable (fun ω : ℝ => -ω) := measurable_neg
  have he (q : ℝ) : decode q (oracle q) = target q := by
    dsimp [decode, oracle, target]
    ring
  have h := measurable_simulation_joint_law_and_cost (Measure.dirac (2 : ℝ))
    next update oracle target decode (fun ω => -ω) hn hu ho hd hi he 7
  exact h.2.2.2.1

-- Zero fuel with an outstanding request is exhaustion, not a fake output.
example : run next (fun s q a => update s q (decode q a)) oracle 0 (-2) =
    (((-2 : ℝ), none), 0) := by
  norm_num [run, next]

-- Seven available calls, but this real execution stops after exactly one.
example : run next (fun s q a => update s q (decode q a)) oracle 7 (-2) =
    (((6 : ℝ), some 6), 1) := by
  norm_num [run, next, update, oracle, decode]

-- A readout available initially consumes no oracle call even at positive fuel.
example : run next (fun s q a => update s q (decode q a)) oracle 7 2 =
    (((2 : ℝ), some 2), 0) := by
  norm_num [run, next]

-- Ordinary seed-averaged cost records the actual stop, not the fuel ceiling.
example : (∫ ω : ℝ,
    ((run next (fun s q a => update s q (decode q a)) oracle 7 (-ω)).2 : ℝ)
      ∂Measure.dirac (2 : ℝ)) = 1 := by
  rw [integral_dirac]
  norm_num [run, next, update, oracle, decode]

end R18BoundaryChecks
