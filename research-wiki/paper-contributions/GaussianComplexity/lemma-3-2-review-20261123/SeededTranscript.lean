import B4Transcript

/-!
# The random seed and the primitive transcript

In the proof of Zhou–Suzuki Lemma 3.2 the entire random seed is independent
of the hidden matrices. Condition on this seed, apply Lemma B.4, and integrate
to compare the joint law of the seed and the complete padded transcript.
-/

open MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open scoped AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

/-- If the conditional laws at fixed seeds agree, mixing the independent seed
and keeping it in the record gives the same joint law. -/
theorem seed_and_output_law_of_fiber_law {S V X : Type*}
    [MeasurableSpace S] [MeasurableSpace V] [MeasurableSpace X]
    (ρ : Measure S) (μ₁ μ₂ : Measure V) [SFinite μ₁] [SFinite μ₂]
    (f : S × V → X) (hf : Measurable f)
    (h : ∀ᵐ s ∂ρ, μ₁.map (fun v => f (s,v)) = μ₂.map (fun v => f (s,v))) :
    (ρ.prod μ₁).map (fun p => (p.1, f p)) = (ρ.prod μ₂).map (fun p => (p.1, f p)) := by
  have hm := measurable_fst.prodMk hf
  ext A hA
  rw [Measure.map_apply hm hA, Measure.map_apply hm hA,
    Measure.prod_apply (hm hA), Measure.prod_apply (hm hA)]
  apply lintegral_congr_ae
  filter_upwards [h] with s hs
  have hslice : MeasurableSet (Prod.mk s ⁻¹' A) := measurable_prodMk_left hA
  have hfs : Measurable (fun v : V => f (s,v)) := hf.comp measurable_prodMk_left
  have heq := congrArg (fun ν : Measure X => ν (Prod.mk s ⁻¹' A)) hs
  change μ₁.map (fun v => f (s,v)) (Prod.mk s ⁻¹' A) =
    μ₂.map (fun v => f (s,v)) (Prod.mk s ⁻¹' A) at heq
  rw [Measure.map_apply hfs hslice, Measure.map_apply hfs hslice] at heq
  exact heq

private abbrev Inputs (S : Type*) (k N : ℕ) := S × Trace k N × (Fin k → O N)

/-- Joint measurability in random seed, starting history and original matrices. -/
theorem measurable_seeded_rawRun {S : Type*} [MeasurableSpace S] {k N : ℕ}
    (select : S → Trace k N → Option (Query k N)) (hs : Measurable (Function.uncurry select))
    (fuel : ℕ) :
    Measurable (fun p : S × Trace k N × (Fin k → O N) => rawRun (select p.1) fuel p.2.1 p.2.2) := by
  induction fuel with
  | zero => exact measurable_const
  | succ t ih =>
    let D := Inputs S k N × Query k N
    let seed : D → S := fun d => d.1.1
    let past : D → Trace k N := fun d => d.1.2.1
    let W : D → Fin k → O N := fun d => d.1.2.2
    let recd : D → Record k N := fun d => some (d.2, oracleAnswer (W d) d.2)
    have hseed : Measurable seed := measurable_fst.comp measurable_fst
    have hpast : Measurable past := measurable_fst.comp (measurable_snd.comp measurable_fst)
    have hW : Measurable W := measurable_snd.comp (measurable_snd.comp measurable_fst)
    have hr : Measurable recd := measurable_some.comp
      (measurable_snd.prodMk (measurable_oracleAnswer.comp (hW.prodMk measurable_snd)))
    let present (p : Inputs S k N) (q : Query k N) :=
      let r := recd (p,q)
      r :: rawRun (select p.1) t (p.2.1 ++ [r]) p.2.2
    have hmore := ih.comp (hseed.prodMk ((measurable_append_singleton hpast hr).prodMk hW))
    have hsome : Measurable (Function.uncurry present) := measurable_list_cons hr hmore
    convert measurable_option_cases (fun p : Inputs S k N => select p.1 p.2.1)
      (hs.comp (measurable_fst.prodMk (measurable_fst.comp measurable_snd)))
      (fun _ => List.replicate (t+1) none) measurable_const present hsome using 1
    funext p
    cases h : select p.1 p.2.1 <;> simp only [rawRun, h, present, recd, W]

/-- The padded chronological primitive transcript from the empty history. -/
noncomputable def seededTranscript {S : Type*} {k N : ℕ}
    (select : S → Trace k N → Option (Query k N)) (fuel : ℕ)
    (p : S × (Fin k → O N)) : Trace k N := rawRun (select p.1) fuel [] p.2

theorem measurable_seededTranscript {S : Type*} [MeasurableSpace S] {k N : ℕ}
    (select : S → Trace k N → Option (Query k N)) (hs : Measurable (Function.uncurry select))
    (fuel : ℕ) : Measurable (seededTranscript select fuel) :=
  (measurable_seeded_rawRun select hs fuel).comp
    (measurable_fst.prodMk (measurable_const.prodMk measurable_snd))

private theorem probability_prior {k N : ℕ} (b : ℝ) (hN : 0 < N) (hb : b = -1 ∨ b = 1) :
    IsProbabilityMeasure (Measure.pi fun _ : Fin k => componentHaar N b) := by
  let : IsProbabilityMeasure (componentHaar N b) := isProbabilityMeasure_componentHaar hN hb
  infer_instance

/-- The two signs have the same joint law of the independent random seed and the
entire original primitive transcript. The budget need only hold on actual draws. -/
theorem seeded_transcript_indistinguishability {S : Type*} [MeasurableSpace S] {k N T : ℕ}
    (hN : 2*T < N) (ρ : Measure S) (select : S → Trace k N → Option (Query k N))
    (hs : Measurable (Function.uncurry select))
    (cap : ∀ b : ℝ, b = -1 ∨ b = 1 →
      ∀ᵐ p ∂ρ.prod (Measure.pi fun _ : Fin k => componentHaar N b),
        ∀ j, blockCount j (seededTranscript select (2*T*k) p) ≤ 2*T) :
    let record := fun p => (p.1, seededTranscript select (2*T*k) p)
    (ρ.prod (Measure.pi fun _ : Fin k => componentHaar N 1)).map record =
      (ρ.prod (Measure.pi fun _ : Fin k => componentHaar N (-1))).map record := by
  have pos : 0 < N := by omega
  let := probability_prior (k := k) 1 pos (Or.inr rfl)
  let := probability_prior (k := k) (-1) pos (Or.inl rfl)
  apply seed_and_output_law_of_fiber_law ρ _ _ _ (measurable_seededTranscript select hs _)
  filter_upwards [Measure.ae_ae_of_ae_prod (cap 1 (Or.inr rfl)),
    Measure.ae_ae_of_ae_prod (cap (-1) (Or.inl rfl))] with s hp hn
  exact padded_transcript_indistinguishability hN (select s)
    (hs.comp measurable_prodMk_left) (fun b hb => hb.elim (fun e => e ▸ hn) (fun e => e ▸ hp))

/-- A common Borel readout of the seed and transcript has equal output laws. -/
theorem seeded_readout_indistinguishability {S X : Type*} [MeasurableSpace S]
    [MeasurableSpace X] {k N T : ℕ} (hN : 2*T < N) (ρ : Measure S)
    (select : S → Trace k N → Option (Query k N)) (hs : Measurable (Function.uncurry select))
    (cap : ∀ b : ℝ, b = -1 ∨ b = 1 →
      ∀ᵐ p ∂ρ.prod (Measure.pi fun _ : Fin k => componentHaar N b),
        ∀ j, blockCount j (seededTranscript select (2*T*k) p) ≤ 2*T)
    (out : S × Trace k N → X) (hout : Measurable out) :
    let draw := fun p => out (p.1, seededTranscript select (2*T*k) p)
    (ρ.prod (Measure.pi fun _ : Fin k => componentHaar N 1)).map draw =
      (ρ.prod (Measure.pi fun _ : Fin k => componentHaar N (-1))).map draw := by
  have hm := measurable_fst.prodMk (measurable_seededTranscript select hs (2*T*k))
  have h := congrArg (Measure.map out) (seeded_transcript_indistinguishability hN ρ select hs cap)
  dsimp only
  simpa only [Measure.map_map hout hm, Function.comp_def] using h

#print axioms seeded_readout_indistinguishability

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
