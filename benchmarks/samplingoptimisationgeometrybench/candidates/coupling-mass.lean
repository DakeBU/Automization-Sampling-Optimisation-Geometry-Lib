import Mathlib.MeasureTheory.Measure.Prod

/-!
# Candidate L2 task: recover the joint probability interface

Compiler-checked candidate only, not an admitted QA or a new library leaf.
The fixed context reproduces the public `IsCoupling` definition from
`AutoSamplingTheory/TechnicalLemmas/Measure/Transport.lean`. The example
reconstructs its `isProbabilityMeasure_of_isCoupling_left` proof without
importing that target module. Retain the repository LICENSE and NOTICE.

Mathematics: for a coupling gamma with first marginal mu, projection onto
the first coordinate sends the whole product space to the whole first space.
Thus gamma(univ) = gamma.fst(univ) = mu(univ) = 1. Only mu needs a probability
assumption; no independent normalization assumption on nu is required.
This gives total mass, not integrability of an arbitrary unbounded function.

Before corpus admission: freeze the natural-language question and rubric,
independently decode an anonymous target and compare all semantic slots.
This public candidate belongs to the already-public coupling family and
must never be relabelled as an unseen private test.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Measure.Transport

open MeasureTheory

def IsCoupling {α β : Type*} [MeasurableSpace α] [MeasurableSpace β]
    (γ : Measure (α × β)) (μ : Measure α) (ν : Measure β) : Prop :=
  γ.fst = μ ∧ γ.snd = ν

example {α β : Type*} [MeasurableSpace α] [MeasurableSpace β]
    {γ : Measure (α × β)} {μ : Measure α} {ν : Measure β}
    [IsProbabilityMeasure μ] (hγ : IsCoupling γ μ ν) :
    IsProbabilityMeasure γ := by
  constructor
  rw [← Measure.fst_univ, hγ.1, measure_univ]

end AutoSamplingTheory.TechnicalLemmas.Measure.Transport
