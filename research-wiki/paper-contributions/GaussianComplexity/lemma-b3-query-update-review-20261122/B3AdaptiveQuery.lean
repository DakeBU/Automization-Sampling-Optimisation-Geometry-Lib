import B3AdaptiveResponse
import B3HaarProduct

/-!
# A nonzero residual query on a fixed dimension profile

In the informative branch of Lemma B.3 (Zhou–Suzuki, arXiv:2610.20492v1),
the old history chooses a unit direction, a query type and an encoding of
the response. Append the encoded response and keep every residual matrix
under its original block label. The response kernel has no sign parameter.
-/

open Matrix MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.TechnicalLemmas.Probability.ParameterizedPushforward

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

variable {H Y : Type*} [MeasurableSpace H] [MeasurableSpace Y] {k : ℕ}

/-- On histories selecting this block and dimension profile, the posterior of
the entire updated tuple is the product of the smaller selected Haar component
and the untouched Haar components. The query sense, direction, and response
encoding may all depend measurably on the history. -/
theorem adaptive_haar_query (ρ : Measure H) [SFinite ρ]
    (dim : Fin (k+1) → ℕ) (hd : ∀ j, 0 < dim j)
    (i : Fin (k+1)) (n : ℕ) (hi : dim i = n+2) (b : ℝ) (hb : b = -1 ∨ b = 1)
    (Q : S (n+2) → O (n+2)) (hQ : Measurable Q)
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (hdet : ∀ z, (Q z).val.det = 1)
    (backward : H → Bool) (hbw : Measurable backward)
    (u : H → S (n+2)) (hu : Measurable u)
    (encode : H → S (n+2) → Y) (he : Measurable (Function.uncurry encode)) :
    let update := fun h => updateHaarTuple dim i n hi Q hfirst (backward h) (u h)
    let μ := Measure.pi fun j => componentHaar (dim j) b
    let ν := Measure.pi fun j => componentHaar (Function.update dim i (n+1) j) b
    (ρ.prod μ).map (fun p => ((p.1, encode p.1 (update p.1 p.2).1), (update p.1 p.2).2)) =
      (ρ ⊗ₘ kernel (sphereProbability (n+2)) encode).prod ν := by
  let : NeZero (n+2) := ⟨by omega⟩
  let := isProbabilityMeasure_sphereProbability (n+2)
  let prob (j) := isProbabilityMeasure_componentHaar (hd j) hb
  have hpos (j) : 0 < Function.update dim i (n+1) j := by
    by_cases h : j = i
    · subst j; simp
    · simpa only [Function.update_of_ne h] using hd j
  let nextProb (j) := isProbabilityMeasure_componentHaar (hpos j) hb
  intro update μ ν
  refine extend_encoded_response ρ μ (sphereProbability (n+2)) ν update ?_ ?_ encode he
  · let f := fun (p : Bool × (S (n+2) × (∀ j, O (dim j)))) =>
      updateHaarTuple dim i n hi Q hfirst p.1 p.2.1 p.2.2
    have hf : Measurable f := measurable_from_prod_countable_right fun t =>
      measurable_updateHaarTuple dim i n hi Q hQ hfirst t
    exact hf.comp ((hbw.comp measurable_fst).prodMk ((hu.comp measurable_fst).prodMk measurable_snd))
  · intro h
    exact (query_selected_haar_product dim i n hi b hb Q hQ hfirst hdet (backward h) (u h)).map_eq

#print axioms adaptive_haar_query

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
