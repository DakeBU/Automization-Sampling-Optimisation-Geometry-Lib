import B3HaarProduct
import B3HistoryUpdate
import ParameterizedPushforward

/-!
# History-dependent choice of block and residual dimensions in Lemma B.3

Each fixed-profile query updates the tuple in its own matrix dimensions.
A history-measurable choice from a countable family of such queries acts
on one common space by tagging tuples with their dimensions. This supplies
the one-step posterior when the choice, old profile and new profile vary.
The algorithm's recursive construction of the frames and query counts is
a separate obligation.
-/

open Matrix MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.TechnicalLemmas.Probability.ParameterizedPushforward

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

abbrev ResidualTuple {k : ℕ} (d : Fin k → ℕ) := ∀ j, O (d j)
abbrev TaggedTuple (k : ℕ) := Σ d : Fin k → ℕ, ResidualTuple d

private theorem measurable_tag {k : ℕ} (d : Fin k → ℕ) :
    Measurable (Sigma.mk (β := ResidualTuple) d) := by
  intro s hs
  exact MeasurableSpace.measurableSet_iInf.mp hs d

/-- Read a tuple of the requested dimensions. The identity matrices define the
off-profile value, where a law supported on the requested profile has zero mass. -/
noncomputable def readTagged {k : ℕ} (d : Fin k → ℕ) (w : TaggedTuple k) : ResidualTuple d := by
  classical
  exact if h : w.1 = d then h ▸ w.2 else fun _ => 1

@[simp] theorem readTagged_mk {k : ℕ} (d : Fin k → ℕ) (w : ResidualTuple d) :
    readTagged d ⟨d,w⟩ = w := by simp [readTagged]

private theorem measurable_readTagged {k : ℕ} (d : Fin k → ℕ) : Measurable (readTagged d) := by
  classical
  intro s hs
  apply MeasurableSpace.measurableSet_iInf.mpr
  intro d'
  change MeasurableSet ((fun w : ResidualTuple d' => readTagged d ⟨d',w⟩) ⁻¹' s)
  by_cases h : d' = d
  · subst d'
    simpa using hs
  · have hconst : (fun w : ResidualTuple d' => readTagged d ⟨d',w⟩) = fun _ => fun _ => 1 := by
      funext w; simp [readTagged, h]
    rw [hconst]
    exact measurable_const hs

noncomputable def tupleHaar {k : ℕ} (d : Fin k → ℕ) (b : ℝ) : Measure (ResidualTuple d) :=
  Measure.pi fun j => componentHaar (d j) b

private theorem probability_tupleHaar {k : ℕ} {d : Fin k → ℕ} (hd : ∀ j, 0 < d j)
    {b : ℝ} (hb : b = -1 ∨ b = 1) : IsProbabilityMeasure (tupleHaar d b) := by
  let : ∀ j, IsProbabilityMeasure (componentHaar (d j) b) := fun j =>
    isProbabilityMeasure_componentHaar (hd j) hb
  unfold tupleHaar
  infer_instance

noncomputable def taggedHaar {k : ℕ} (d : Fin k → ℕ) (b : ℝ) : Measure (TaggedTuple k) :=
  (tupleHaar d b).map (Sigma.mk d)

theorem probability_taggedHaar {k : ℕ} {d : Fin k → ℕ} (hd : ∀ j, 0 < d j)
    {b : ℝ} (hb : b = -1 ∨ b = 1) : IsProbabilityMeasure (taggedHaar d b) := by
  let := probability_tupleHaar hd hb
  exact Measure.isProbabilityMeasure_map (measurable_tag d).aemeasurable

/-- Data for one type of query at fixed old and new dimensions. Its branch map
and answer kernel are chosen before the determinant sign. -/
structure ResidualChart (H Y : Type*) [MeasurableSpace H] [MeasurableSpace Y] (k : ℕ) where
  before : Fin k → ℕ
  after : Fin k → ℕ
  before_pos : ∀ j, 0 < before j
  after_pos : ∀ j, 0 < after j
  update : H → ResidualTuple before → Y × ResidualTuple after
  measurable_update : Measurable (Function.uncurry update)
  answer : Kernel H Y
  markov_answer : IsMarkovKernel answer
  law : ∀ b : ℝ, b = -1 ∨ b = 1 → ∀ h : H,
    (tupleHaar before b).map (update h) = (answer h).prod (tupleHaar after b)

variable {H Y : Type*} [MeasurableSpace H] [MeasurableSpace Y] {k : ℕ}

/-- A history-determined answer, including a terminal symbol, leaves the entire
tuple and its dimensions unchanged. -/
noncomputable def determinedChart (d : Fin k → ℕ) (hd : ∀ j, 0 < d j)
    (answer : H → Y) (hans : Measurable answer) : ResidualChart H Y k where
  before := d
  after := d
  before_pos := hd
  after_pos := hd
  update h w := (answer h, w)
  measurable_update := (hans.comp measurable_fst).prodMk measurable_snd
  answer := Kernel.deterministic answer hans
  markov_answer := inferInstance
  law b hb h := by
    let := probability_tupleHaar hd hb
    rw [Kernel.deterministic_apply, Measure.dirac_prod]

/-- Construct the informative branch from the actual observed direction and
extracted smaller matrix. The other block labels keep their original matrices. -/
noncomputable def informativeChart (d : Fin (k+1) → ℕ) (hd : ∀ j, 0 < d j)
    (i : Fin (k+1)) (n : ℕ) (hi : d i = n+2)
    (Q : S (n+2) → O (n+2)) (hQ : Measurable Q)
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (hdet : ∀ z, (Q z).val.det = 1)
    (back : H → Bool) (hback : Measurable back)
    (u : H → S (n+2)) (hu : Measurable u)
    (encode : H → S (n+2) → Y) (he : Measurable (Function.uncurry encode)) :
    ResidualChart H Y (k+1) := by
  let := isProbabilityMeasure_sphereProbability (n+2)
  let read (h : H) := updateHaarTuple d i n hi Q hfirst (back h) (u h)
  have hm : Measurable (Function.uncurry read) :=
    (measurable_from_prod_countable_right
      (f := fun p : Bool × S (n+2) × ResidualTuple d =>
        updateHaarTuple d i n hi Q hfirst p.1 p.2.1 p.2.2)
      (fun t => measurable_updateHaarTuple d i n hi Q hQ hfirst t)).comp
        ((hback.comp measurable_fst).prodMk ((hu.comp measurable_fst).prodMk measurable_snd))
  have hpos (j) : 0 < Function.update d i (n+1) j := by
    by_cases h : j = i
    · subst j; simp
    · simpa only [Function.update_of_ne h] using hd j
  refine ⟨d, Function.update d i (n+1), hd, hpos,
    fun h w => (encode h (read h w).1, (read h w).2),
    (he.comp (measurable_fst.prodMk hm.fst)).prodMk hm.snd,
    kernel (sphereProbability (n+2)) encode, isMarkovKernel_kernel _ _ he, ?_⟩
  intro b hb h
  let := probability_tupleHaar hpos hb
  let σ := sphereProbability (n+2)
  have hp : MeasurePreserving (encode h) σ (σ.map (encode h)) := ⟨he.of_uncurry_left, rfl⟩
  have hread := query_selected_haar_product d i n hi b hb Q hQ hfirst hdet (back h) (u h)
  change (tupleHaar d b).map (Prod.map (encode h) id ∘ read h) = _
  rw [kernel_apply _ _ he]
  exact ((hp.prod (MeasurePreserving.id (tupleHaar (Function.update d i (n+1)) b))).comp hread).map_eq

noncomputable def ResidualChart.taggedUpdate (c : ResidualChart H Y k)
    (h : H) (w : TaggedTuple k) : Y × TaggedTuple k :=
  Prod.map id (Sigma.mk c.after) (c.update h (readTagged c.before w))

theorem ResidualChart.measurable_taggedUpdate (c : ResidualChart H Y k) :
    Measurable (Function.uncurry c.taggedUpdate) :=
  (measurable_id.prodMap (measurable_tag c.after)).comp
    (c.measurable_update.comp (measurable_fst.prodMk ((measurable_readTagged c.before).comp measurable_snd)))

theorem ResidualChart.tagged_law (c : ResidualChart H Y k) {b : ℝ}
    (hb : b = -1 ∨ b = 1) (h : H) :
    (taggedHaar c.before b).map (c.taggedUpdate h) = (c.answer h).prod (taggedHaar c.after b) := by
  let := probability_tupleHaar c.after_pos hb
  let := c.markov_answer
  rw [taggedHaar, Measure.map_map c.measurable_taggedUpdate.of_uncurry_left (measurable_tag _)]
  have heq : c.taggedUpdate h ∘ Sigma.mk c.before = Prod.map id (Sigma.mk c.after) ∘ c.update h := by
    funext w
    simp only [Function.comp_apply, ResidualChart.taggedUpdate, readTagged_mk]
  rw [heq, ← Measure.map_map (measurable_id.prodMap (measurable_tag _))
    c.measurable_update.of_uncurry_left, c.law b hb h, taggedHaar,
    ← Measure.map_prod_map _ _ measurable_id (measurable_tag _), Measure.map_id]

variable {I : Type*} [MeasurableSpace I] [Countable I] [MeasurableSingletonClass I]

/-- Select a different kernel at each history from a countable family. -/
noncomputable def selectHistoryKernel {X : Type*} [MeasurableSpace X]
    (pick : H → I) (hp : Measurable pick) (K : I → Kernel H X) : Kernel H X where
  toFun h := K (pick h) h
  measurable' :=
    (measurable_from_prod_countable_right (f := fun p : I × H => K p.1 p.2)
      (fun i => (K i).measurable)).comp (hp.prodMk measurable_id)

theorem markov_selectHistoryKernel {X : Type*} [MeasurableSpace X]
    (pick : H → I) (hp : Measurable pick) (K : I → Kernel H X)
    (hK : ∀ i, IsMarkovKernel (K i)) : IsMarkovKernel (selectHistoryKernel pick hp K) :=
  ⟨fun h => (hK (pick h)).isProbabilityMeasure h⟩

/-- On adjoining the recorded response, the posterior is exactly the tagged
product law at the new dimensions from the history-selected chart. -/
theorem history_selected_chart_posterior (ρ : Measure H) [SFinite ρ]
    (charts : I → ResidualChart H Y k) (pick : H → I) (hp : Measurable pick)
    (b : ℝ) (hb : b = -1 ∨ b = 1) :
    let old := selectHistoryKernel pick hp fun i => Kernel.const H (taggedHaar (charts i).before b)
    let new := selectHistoryKernel pick hp fun i => Kernel.const H (taggedHaar (charts i).after b)
    let ans := selectHistoryKernel pick hp fun i => (charts i).answer
    let update := fun h => (charts (pick h)).taggedUpdate h
    (ρ ⊗ₘ old).map (fun p : H × TaggedTuple k =>
        ((p.1, (update p.1 p.2).1), (update p.1 p.2).2)) =
      (ρ ⊗ₘ ans) ⊗ₘ Kernel.prodMkRight Y new := by
  intro old new ans update
  let : IsMarkovKernel old := markov_selectHistoryKernel _ _ _ fun i => by
    let := probability_taggedHaar (charts i).before_pos hb
    infer_instance
  let : IsMarkovKernel new := markov_selectHistoryKernel _ _ _ fun i => by
    let := probability_taggedHaar (charts i).after_pos hb
    infer_instance
  let : IsMarkovKernel ans := markov_selectHistoryKernel _ _ _ fun i => (charts i).markov_answer
  apply extend_history_posterior ρ old ans new update
  · exact (measurable_from_prod_countable_right
      (f := fun p : I × (H × TaggedTuple k) => (charts p.1).taggedUpdate p.2.1 p.2.2)
      (fun i => (charts i).measurable_taggedUpdate)).comp
        ((hp.comp measurable_fst).prodMk measurable_id)
  · exact ae_of_all _ fun h => (charts (pick h)).tagged_law hb h

#print axioms informativeChart
#print axioms history_selected_chart_posterior

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
