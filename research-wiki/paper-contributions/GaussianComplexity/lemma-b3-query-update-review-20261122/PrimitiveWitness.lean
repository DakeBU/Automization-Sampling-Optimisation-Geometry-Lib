import B3PrimitiveQuery
import HaarOrientedSection

open Matrix MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarOrientedSection
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.TechnicalLemmas.Probability.ParameterizedPushforward

namespace IndependentPrimitive

private def d (i : Fin 2) := if i = 1 then 2 else 3
private noncomputable def q : Bool → Vec 3
  | false => ![-2, 1, 0]
  | true => ![7, 0, 1]

private theorem nz (h : Bool) :
    queryComplement (m := 2) (r := 1) (queryFrame h 1 1) (q h) ≠ 0 := by
  cases h <;> intro he
  · have := congrArg (fun x : E 2 => x 0) he
    norm_num [queryComplement, queryFrame, q, residualCoords, act] at this
  · have := congrArg (fun x : E 2 => x 1) he
    norm_num [queryComplement, queryFrame, q, residualCoords, act] at this

/-- A three-dimensional ambient forward query or transpose query, selected
by the old Boolean history. The other matrix has three residual coordinates. -/
theorem primitive_mixed (ρ : Measure Bool) [SFinite ρ] :
    ∃ (Q : S 2 → O 2) (hc : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin 2) 1 = WithLp.ofLp z.val),
      let frame := fun h => queryFrame h (1 : O 3) 1
      let u := fun h => residualUnit ⟨queryComplement (r := 1) (frame h) (q h), nz h⟩
      let step := fun h => updateHaarTuple (k := 1) d 1 0 rfl Q hc h (u h)
      let encode := fun h => responseFromSphere (r := 1) (frame h) (frame h) (q h)
      let μ := Measure.pi fun j => componentHaar (d j) (-1)
      let ν := Measure.pi fun j => componentHaar (Function.update d 1 1 j) (-1)
      (ρ.prod μ).map (fun p => ((p.1, primitiveAnswer (r := 1) 1 1 (castOrthogonal
        (show d 1 = 2 by rfl) (p.2 1)) (q p.1) p.1), (step p.1 p.2).2)) =
        (ρ ⊗ₘ kernel (sphereProbability 2) encode).prod ν := by
  obtain ⟨Q, hm, hc⟩ := exists_measurable_oriented_section 0
  have hfirst := fun z => (hc z).2
  have hd : ∀ j, 0 < d j := by intro j; unfold d; split <;> decide
  exact ⟨Q, hfirst, primitive_haar_query (k := 1) (r := 1) ρ d hd 1 0 rfl (-1) (Or.inl rfl)
    Q hm hfirst (fun z => (hc z).1) (fun _ => 1) (fun _ => 1) measurable_const measurable_const
    id measurable_id q (measurable_of_countable q) nz⟩

#print axioms primitive_mixed

end IndependentPrimitive
