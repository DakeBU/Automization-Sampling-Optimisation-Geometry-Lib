import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle
import Mathlib.MeasureTheory.MeasurableSpace.Embedding
import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# Measurable adaptive oracle simulation

Author-derived probability interface for the exact oracle equivalence in
Zhou--Suzuki arXiv:2610.20492v1 Section2 Equation1. We reuse the canonical
finite-fuel interpreter without padding actual query counts. A missing output
is exhaustion, not a successful sample. This theorem does not assert source
algorithm representation or a class-uniform query-complexity bound.
-/
open MeasureTheory
open AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle
set_option autoImplicit false
universe uS uQ uA uB uX uΩ

namespace AutoSamplingTheory.TechnicalLemmas.Probability.AdaptiveOracleSimulation

private theorem run_simulation_and_cap
    {S : Type uS} {Q : Type uQ} {A : Type uA} {B : Type uB} {X : Type uX}
    (next : S → Sum X Q) (update : S → Q → B → S)
    (oracle : Q → A) (target : Q → B) (decode : Q → A → B)
    (hdecode : ∀ q, decode q (oracle q) = target q) (fuel : ℕ) :
    ∀ s, run next (fun s q a => update s q (decode q a)) oracle fuel s =
      run next update target fuel s ∧
      (run next (fun s q a => update s q (decode q a)) oracle fuel s).2 ≤ fuel := by
  induction fuel with
  | zero =>
      intro s
      cases h : next s <;> simp [run, h]
  | succ n ih =>
      intro s
      cases h : next s with
      | inl x => simp [run, h]
      | inr q =>
          have step (upd : S → Q → B → S) (O : Q → B) :
              run next upd O (n+1) s =
                let tail := run next upd O n (upd s q (O q))
                (tail.1, tail.2+1) := by rw [run, h]
          have stepA (upd : S → Q → A → S) (O : Q → A) :
              run next upd O (n+1) s =
                let tail := run next upd O n (upd s q (O q))
                (tail.1, tail.2+1) := by rw [run, h]
          have hr := ih (update s q (target q))
          constructor
          · simpa only [stepA, step, hdecode] using
              congrArg (fun r : (S × Option X) × ℕ => (r.1, r.2+1)) hr.1
          · simpa only [stepA, hdecode] using Nat.succ_le_succ hr.2

private theorem measurable_run
    {S : Type uS} {Q : Type uQ} {A : Type uA} {X : Type uX}
    [MeasurableSpace S] [MeasurableSpace Q] [MeasurableSpace A]
    [MeasurableSpace X] [MeasurableSpace (Option X)]
    (next : S → Sum X Q) (update : S → Q → A → S) (oracle : Q → A)
    (hnext : Measurable next)
    (hupdate : Measurable (fun p : S × Q × A => update p.1 p.2.1 p.2.2))
    (horacle : Measurable oracle) (hsome : Measurable (@Option.some X))
    (fuel : ℕ) : Measurable (run next update oracle fuel) := by
  have hl : Measurable (fun p : S × X => ((p.1, some p.2), (0 : ℕ))) :=
    (measurable_fst.prodMk (hsome.comp measurable_snd)).prodMk measurable_const
  have hdist : Measurable (fun s : S =>
      (MeasurableEquiv.prodSumDistrib S X Q) (s, next s)) :=
    (MeasurableEquiv.prodSumDistrib S X Q).measurable.comp
      (measurable_id.prodMk hnext)
  induction fuel with
  | zero =>
      have hr : Measurable (fun p : S × Q => ((p.1, (none : Option X)), (0 : ℕ))) :=
        (measurable_fst.prodMk measurable_const).prodMk measurable_const
      convert (hl.sumElim hr).comp hdist using 1
      funext s
      cases h : next s <;> rw [run, h] <;>
        simp only [Function.comp_apply, h] <;> rfl
  | succ n ih =>
      have hstep : Measurable (fun p : S × Q => update p.1 p.2 (oracle p.2)) :=
        hupdate.comp (measurable_fst.prodMk
          (measurable_snd.prodMk (horacle.comp measurable_snd)))
      have htail := ih.comp hstep
      have hadd : Measurable (fun n : ℕ => n+1) := measurable_of_countable _
      have hr : Measurable (fun p : S × Q =>
          let tail := run next update oracle n (update p.1 p.2 (oracle p.2))
          (tail.1, tail.2+1)) :=
        (measurable_fst.comp htail).prodMk (hadd.comp (measurable_snd.comp htail))
      convert (hl.sumElim hr).comp hdist using 1
      funext s
      cases h : next s <;> rw [run, h] <;>
        simp only [Function.comp_apply, h] <;> rfl

/-- Exact reply simulation preserves the measurable seeded joint execution
law and the actual, pointwise bounded query cost and its ordinary expectation. -/
theorem measurable_simulation_joint_law_and_cost :
  ∀ {S : Type uS} {Q : Type uQ} {A : Type uA} {B : Type uB}
      {X : Type uX} {Ω : Type uΩ}
      [MeasurableSpace S] [MeasurableSpace Q] [MeasurableSpace A]
      [MeasurableSpace B] [MeasurableSpace X] [MeasurableSpace Ω],
      letI : MeasurableSpace (Option X) := MeasurableSpace.comap
        (fun x : Option X => x.elim (Sum.inl () : Unit ⊕ X) Sum.inr) inferInstance
      ∀ (μ : Measure Ω) [IsProbabilityMeasure μ]
      (next : S → Sum X Q) (update : S → Q → B → S)
      (oracle : Q → A) (target : Q → B) (decode : Q → A → B)
      (initial : Ω → S),
      Measurable next →
      Measurable (fun p : S × Q × B => update p.1 p.2.1 p.2.2) →
      Measurable oracle →
      Measurable (fun p : Q × A => decode p.1 p.2) →
      Measurable initial →
      (∀ q, decode q (oracle q) = target q) →
      ∀ fuel : ℕ,
        let baseRun : Ω → (S × Option X) × ℕ := fun ω =>
          run next (fun s q a => update s q (decode q a)) oracle fuel (initial ω)
        let targetRun : Ω → (S × Option X) × ℕ := fun ω =>
          run next update target fuel (initial ω)
        Measurable baseRun ∧ Measurable targetRun ∧
        (∀ ω, baseRun ω = targetRun ω ∧ (baseRun ω).2 ≤ fuel) ∧
        μ.map baseRun = μ.map targetRun ∧
        IsProbabilityMeasure (μ.map baseRun) ∧
        Integrable (fun ω => ((baseRun ω).2 : ℝ)) μ ∧
        (∫ ω, ((baseRun ω).2 : ℝ) ∂μ) = (∫ ω, ((targetRun ω).2 : ℝ) ∂μ) ∧
        (∫ ω, ((baseRun ω).2 : ℝ) ∂μ) ≤ (fuel : ℝ) := by
  intro S Q A B X Ω mS mQ mA mB mX mΩ
  let : MeasurableSpace (Option X) := MeasurableSpace.comap
    (fun x : Option X => x.elim (Sum.inl () : Unit ⊕ X) Sum.inr) inferInstance
  dsimp only
  intro μ hμ next update oracle target decode initial hnext hupdate horacle hdecodeMeas
    hinitial hdecode fuel
  have hsome : Measurable (@Option.some X) := by
    apply Measurable.of_comap_le
    change MeasurableSpace.comap Option.some
      (MeasurableSpace.comap
        (fun x : Option X => x.elim (Sum.inl () : Unit ⊕ X) Sum.inr) inferInstance) ≤ _
    rw [MeasurableSpace.comap_comp]
    exact (measurable_inr : Measurable (Sum.inr : X → Unit ⊕ X)).comap_le
  let baseRun : Ω → (S × Option X) × ℕ := fun ω =>
    run next (fun s q a => update s q (decode q a)) oracle fuel (initial ω)
  let targetRun : Ω → (S × Option X) × ℕ := fun ω =>
    run next update target fuel (initial ω)
  have hcorrected : Measurable (fun p : S × Q × A =>
      update p.1 p.2.1 (decode p.2.1 p.2.2)) :=
    hupdate.comp (measurable_fst.prodMk
      (measurable_snd.fst.prodMk (hdecodeMeas.comp measurable_snd)))
  have hb : Measurable baseRun :=
    (measurable_run next (fun s q a => update s q (decode q a)) oracle
      hnext hcorrected horacle hsome fuel).comp hinitial
  have he (ω : Ω) : baseRun ω = targetRun ω ∧ (baseRun ω).2 ≤ fuel :=
    run_simulation_and_cap next update oracle target decode hdecode fuel (initial ω)
  have heq : baseRun = targetRun := funext fun ω => (he ω).1
  have ht : Measurable targetRun := by rw [← heq]; exact hb
  have hlaw : μ.map baseRun = μ.map targetRun := congrArg (fun f => μ.map f) heq
  have hprob : IsProbabilityMeasure (μ.map baseRun) :=
    Measure.isProbabilityMeasure_map hb.aemeasurable
  have hcount : Measurable (fun ω => ((baseRun ω).2 : ℝ)) :=
    (measurable_of_countable (fun n : ℕ => (n : ℝ))).comp (measurable_snd.comp hb)
  have hbound (ω : Ω) : ((baseRun ω).2 : ℝ) ≤ (fuel : ℝ) :=
    Nat.cast_le.mpr (he ω).2
  have hint : Integrable (fun ω => ((baseRun ω).2 : ℝ)) μ :=
    (integrable_const (fuel : ℝ)).mono' hcount.aestronglyMeasurable
      (ae_of_all _ fun ω => by
        rw [Real.norm_eq_abs, abs_of_nonneg (Nat.cast_nonneg _)]
        exact hbound ω)
  have hcost : (∫ ω, ((baseRun ω).2 : ℝ) ∂μ) =
      (∫ ω, ((targetRun ω).2 : ℝ) ∂μ) :=
    integral_congr_ae (ae_of_all _ fun ω =>
      congrArg (fun r : (S × Option X) × ℕ => (r.2 : ℝ)) (he ω).1)
  have hmean : (∫ ω, ((baseRun ω).2 : ℝ) ∂μ) ≤ (fuel : ℝ) := by
    simpa using integral_mono hint (integrable_const (fuel : ℝ)) hbound
  exact ⟨hb, ht, he, hlaw, hprob, hint, hcost, hmean⟩

end AutoSamplingTheory.TechnicalLemmas.Probability.AdaptiveOracleSimulation
