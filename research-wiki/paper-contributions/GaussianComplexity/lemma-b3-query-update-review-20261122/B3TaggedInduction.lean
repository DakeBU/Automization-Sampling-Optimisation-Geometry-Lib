import B3TaggedUpdate
import B3HistoryInduction

/-!
# Finite histories of a sequence of residual updates

In the chart representation of the B.3 induction, every history selects the
next query. The old profile must agree almost everywhere with the initial
profile, or with the profile left by the preceding update. The resulting
posterior at every finite time is the tagged product Haar law. The common
response kernels give equal history laws for the two determinant signs.
-/

open MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

universe u v
variable {H : Type u} {Y : ℕ → Type u} [MeasurableSpace H] [∀ t, MeasurableSpace (Y t)]
variable {I : Type v} [MeasurableSpace I] [Countable I] [MeasurableSingletonClass I] {k : ℕ}

/-- The index may encode the current profile, queried block, and whether the
response is informative, determined, or padding. -/
structure TaggedQueryPolicy (H : Type u) (Y : ℕ → Type u) [MeasurableSpace H]
    [∀ t, MeasurableSpace (Y t)] (I : Type v) [MeasurableSpace I] (k : ℕ) where
  charts : ∀ t, I → ResidualChart (QueryHistory H Y t) (Y t) k
  pick : ∀ t, QueryHistory H Y t → I
  measurable_pick : ∀ t, Measurable (pick t)

namespace TaggedQueryPolicy
variable (P : TaggedQueryPolicy H Y I k)

def branch (t : ℕ) (h : QueryHistory H Y t) := P.charts t (P.pick t h)

noncomputable def answers (t : ℕ) : Kernel (QueryHistory H Y t) (Y t) :=
  selectHistoryKernel (P.pick t) (P.measurable_pick t) fun i => (P.charts t i).answer

instance answers_markov (t : ℕ) : IsMarkovKernel (P.answers t) :=
  markov_selectHistoryKernel _ _ _ fun i => (P.charts t i).markov_answer

/-- The deterministic run starts from the original tagged matrix draw. -/
noncomputable def evolution :
    QueryEvolution (H × TaggedTuple k) H Y (fun _ => TaggedTuple k) where
  initial := id
  initial_measurable := measurable_id
  step t h := (P.branch t h).taggedUpdate h
  step_measurable t :=
    (measurable_from_prod_countable_right
      (f := fun p : I × (QueryHistory H Y t × TaggedTuple k) =>
        (P.charts t p.1).taggedUpdate p.2.1 p.2.2)
      (fun i => (P.charts t i).measurable_taggedUpdate)).comp
        (((P.measurable_pick t).comp measurable_fst).prodMk measurable_id)

noncomputable def beforeKernel (b : ℝ) (t : ℕ) : Kernel (QueryHistory H Y t) (TaggedTuple k) :=
  selectHistoryKernel (P.pick t) (P.measurable_pick t) fun i =>
    Kernel.const _ (taggedHaar (P.charts t i).before b)

private noncomputable def afterKernel (b : ℝ) (t : ℕ) : Kernel (QueryHistory H Y t) (TaggedTuple k) :=
  selectHistoryKernel (P.pick t) (P.measurable_pick t) fun i =>
    Kernel.const _ (taggedHaar (P.charts t i).after b)

private theorem markov_before {b : ℝ} (hb : b = -1 ∨ b = 1) (t : ℕ) :
    IsMarkovKernel (P.beforeKernel b t) :=
  markov_selectHistoryKernel _ _ _ fun i => by
    let := probability_taggedHaar (P.charts t i).before_pos hb
    infer_instance

private theorem markov_after {b : ℝ} (hb : b = -1 ∨ b = 1) (t : ℕ) :
    IsMarkovKernel (P.afterKernel b t) :=
  markov_selectHistoryKernel _ _ _ fun i => by
    let := probability_taggedHaar (P.charts t i).after_pos hb
    infer_instance

/-- Dimensions fit the old history at initialization and at successive steps.
Both requirements only concern histories of full measure. -/
structure Fits (ρ : Measure H) (d : Fin k → ℕ) : Prop where
  start : ∀ᵐ h ∂ρ, (P.branch 0 h).before = d
  next : ∀ t, ∀ᵐ h ∂iteratedHistoryLaw ρ P.answers (t+1),
    (P.branch (t+1) h).before = (P.branch t h.1).after

private theorem prior_eq_before {ρ : Measure H} {d : Fin k → ℕ} (fits : P.Fits ρ d)
    (b : ℝ) (t : ℕ) :
    iteratedResidualKernel (X := fun _ => TaggedTuple k) (Kernel.const H (taggedHaar d b))
      (P.afterKernel b) t =ᵐ[iteratedHistoryLaw ρ P.answers t] P.beforeKernel b t := by
  cases t with
  | zero =>
    filter_upwards [fits.start] with h hh
    change taggedHaar d b = taggedHaar (P.branch 0 h).before b
    rw [hh]
  | succ t =>
    filter_upwards [fits.next t] with h hh
    change taggedHaar (P.branch t h.1).after b = taggedHaar (P.branch (t+1) h).before b
    rw [hh]

private noncomputable def posterior (ρ : Measure H) [SFinite ρ] (d : Fin k → ℕ)
    (hd : ∀ j, 0 < d j) (fits : P.Fits ρ d) (b : ℝ) (hb : b = -1 ∨ b = 1) :
    QueryPosterior P.evolution (ρ.prod (taggedHaar d b)) ρ P.answers := by
  let := probability_taggedHaar hd hb
  refine ⟨Kernel.const H (taggedHaar d b), inferInstance, P.afterKernel b, P.markov_after hb, ?_, ?_⟩
  · change (ρ.prod (taggedHaar d b)).map id = _
    rw [Measure.map_id, Measure.compProd_const]
  · intro t
    filter_upwards [P.prior_eq_before fits b t] with h hh
    rw [hh]
    exact (P.branch t h).tagged_law hb h

private theorem markov_prior {d : Fin k → ℕ} (hd : ∀ j, 0 < d j) {b : ℝ}
    (hb : b = -1 ∨ b = 1) (t : ℕ) :
    IsMarkovKernel (iteratedResidualKernel (Y := Y) (X := fun _ => TaggedTuple k)
      (Kernel.const H (taggedHaar d b)) (P.afterKernel b) t) := by
  cases t with
  | zero =>
    let := probability_taggedHaar hd hb
    exact inferInstanceAs (IsMarkovKernel (Kernel.const H (taggedHaar d b)))
  | succ t =>
    let := P.markov_after hb t
    exact inferInstanceAs (IsMarkovKernel (Kernel.prodMkRight (Y t) (P.afterKernel b t)))

/-- For each finite time the joint law is the history law times the conditional
kernel of product Haar matrices at the actual history-selected dimensions. -/
theorem joint_law (ρ : Measure H) [SFinite ρ] (d : Fin k → ℕ) (hd : ∀ j, 0 < d j)
    (fits : P.Fits ρ d) (b : ℝ) (hb : b = -1 ∨ b = 1) (t : ℕ) :
    (ρ.prod (taggedHaar d b)).map (P.evolution.run t) =
      iteratedHistoryLaw ρ P.answers t ⊗ₘ P.beforeKernel b t := by
  let post := P.posterior ρ d hd fits b hb
  have h := post.joint_law t
  refine h.trans ?_
  let := P.markov_before hb t
  let := P.markov_prior hd hb t
  change (iteratedHistoryLaw ρ P.answers t ⊗ₘ iteratedResidualKernel (Y := Y)
    (X := fun _ => TaggedTuple k) (Kernel.const H (taggedHaar d b)) (P.afterKernel b) t) = _
  exact Measure.compProd_congr (P.prior_eq_before fits b t)

/-- The same policy has equal finite transcript laws on the negative and
positive determinant components. -/
theorem signs_same_history (ρ : Measure H) [SFinite ρ] (d : Fin k → ℕ) (hd : ∀ j, 0 < d j)
    (fits : P.Fits ρ d) (t : ℕ) :
    (ρ.prod (taggedHaar d (-1))).map (fun w => (P.evolution.run t w).1) =
      (ρ.prod (taggedHaar d 1)).map (fun w => (P.evolution.run t w).1) :=
  same_history_of_shared_answers (P.posterior ρ d hd fits (-1) (Or.inl rfl))
    (P.posterior ρ d hd fits 1 (Or.inr rfl)) t

#print axioms joint_law
#print axioms signs_same_history
end TaggedQueryPolicy
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
