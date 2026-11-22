import B3PrimitiveQuery
import B3TaggedUpdate

/-!
# Choosing the rank update from the ambient query

At a block with at least two residual dimensions, an arbitrary measurable
ambient query selects its own informative or determined branch. The chart
reads the same vector as the forward or inverse matrix oracle on every draw.
-/

open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

variable {H : Type*} [MeasurableSpace H]

/-- The public input to one primitive query, in the frames at the old history. -/
structure FramedQuery (H : Type*) [MeasurableSpace H] (m r : ℕ) where
  domainFrame : H → O (m+r)
  rangeFrame : H → O (m+r)
  backward : H → Bool
  vector : H → Vec (m+r)
  measurable_domainFrame : Measurable domainFrame
  measurable_rangeFrame : Measurable rangeFrame
  measurable_backward : Measurable backward
  measurable_vector : Measurable vector

namespace FramedQuery

variable {m r : ℕ} (q : FramedQuery H m r)

def inputFrame (h : H) := queryFrame (q.backward h) (q.domainFrame h) (q.rangeFrame h)
def outputFrame (h : H) := queryFrame (q.backward h) (q.rangeFrame h) (q.domainFrame h)
noncomputable def complement (h : H) := queryComplement (q.inputFrame h) (q.vector h)
noncomputable def encode (h : H) := responseFromSphere (q.inputFrame h) (q.outputFrame h) (q.vector h)

private theorem measurable_input : Measurable q.inputFrame :=
  measurable_queryFrame q.measurable_backward q.measurable_domainFrame q.measurable_rangeFrame
private theorem measurable_output : Measurable q.outputFrame :=
  measurable_queryFrame q.measurable_backward q.measurable_rangeFrame q.measurable_domainFrame
private theorem measurable_complement : Measurable q.complement :=
  measurable_queryComplement q.measurable_input q.measurable_vector
private theorem measurable_encode : Measurable (Function.uncurry q.encode) :=
  measurable_responseFromSphere q.measurable_input q.measurable_output q.measurable_vector

/-- The sphere-valued direction is total, including on the region that will
choose the determined chart. -/
noncomputable def unit [NeZero m] (h : H) : S m :=
  decodeResponse (q.inputFrame h) ‖q.complement h‖ (q.vector h)

theorem unit_eq [NeZero m] (h : H) (hc : q.complement h ≠ 0) :
    q.unit h = residualUnit ⟨q.complement h, hc⟩ := by
  let F := q.inputFrame h
  let v := q.vector h
  let a := exposedCoords m r (act F⁻¹ v)
  let c : {x : E m // x ≠ 0} := ⟨q.complement h, hc⟩
  have hv : encodeResponse F a ‖c.val‖ (residualUnit c) = v := by
    unfold encodeResponse
    rw [scaled_residualUnit]
    exact query_from_coordinates F v
  exact (congrArg (decodeResponse F ‖c.val‖) hv.symm).trans
    (decode_encodeResponse F a (norm_ne_zero_iff.mpr hc) _)

noncomputable def informative (h : H) : Bool := by
  classical exact decide (q.complement h ≠ 0)

theorem measurable_informative : Measurable q.informative := by
  classical
  change Measurable (fun h => if q.complement h ≠ 0 then true else false)
  exact Measurable.ite (q.measurable_complement (measurableSet_singleton 0)).compl
    measurable_const measurable_const

private theorem determined_answer [NeZero m] (h : H) (W : O m) (hc : q.complement h = 0) :
    primitiveAnswer (q.domainFrame h) (q.rangeFrame h) W (q.vector h) (q.backward h) =
      q.encode h (coordinatePoint 0) := by
  let F := q.inputFrame h
  let a := exposedCoords m r (act F⁻¹ (q.vector h))
  have hc' : residualCoords m r (act F⁻¹ (q.vector h)) = 0 :=
    congrArg WithLp.ofLp hc
  have hv : act F (splitVec r a 0) = q.vector h := by
    simpa only [← hc'] using query_from_coordinates F (q.vector h)
  have hnorm : ‖queryComplement F (q.vector h)‖ = 0 := by rw [show queryComplement F (q.vector h) = 0 from hc, norm_zero]
  change primitiveAnswer _ _ _ _ _ =
    encodeResponse (q.outputFrame h) a ‖queryComplement F (q.vector h)‖ _
  rw [hnorm]
  simp only [encodeResponse, zero_smul]
  cases hb : q.backward h
  · have hi : F = q.domainFrame h := by simp [F, inputFrame, hb, queryFrame]
    have ho : q.outputFrame h = q.rangeFrame h := by simp [outputFrame, hb, queryFrame]
    rw [hi] at hv
    rw [ho]
    exact (congrArg (act (framed (q.domainFrame h) (q.rangeFrame h) W)) hv.symm).trans
      (zero_residual_response _ _ W a).1
  · have hi : F = q.rangeFrame h := by simp [F, inputFrame, hb, queryFrame]
    have ho : q.outputFrame h = q.domainFrame h := by simp [outputFrame, hb, queryFrame]
    rw [hi] at hv
    rw [ho]
    exact (congrArg (act (framed (q.domainFrame h) (q.rangeFrame h) W)⁻¹) hv.symm).trans
      (zero_residual_response _ _ W a).2

end FramedQuery

variable {k n r : ℕ}

/-- The two charts for this primitive ambient query. Select with
`q.informative`, determined by the old history alone. -/
noncomputable def primitiveCharts (q : FramedQuery H (n+2) r)
    (d : Fin (k+1) → ℕ) (hd : ∀ j, 0 < d j) (i : Fin (k+1)) (hi : d i = n+2)
    (Q : S (n+2) → O (n+2)) (hQ : Measurable Q)
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (hdet : ∀ z, (Q z).val.det = 1) : Bool → ResidualChart H (Vec ((n+2)+r)) (k+1)
  | true => informativeChart d hd i n hi Q hQ hfirst hdet q.backward q.measurable_backward
      q.unit (measurable_decodeResponse q.measurable_input q.measurable_complement.norm
        q.measurable_vector) q.encode q.measurable_encode
  | false => determinedChart d hd (fun h => q.encode h (coordinatePoint 0))
      (q.measurable_encode.comp (measurable_id.prodMk measurable_const))

/-- In both branches the selected chart returns the true ambient oracle
answer, and it drops one residual dimension exactly on the nonzero branch. -/
theorem primitive_chart_correct (q : FramedQuery H (n+2) r)
    (d : Fin (k+1) → ℕ) (hd : ∀ j, 0 < d j) (i : Fin (k+1)) (hi : d i = n+2)
    (Q : S (n+2) → O (n+2)) (hQ : Measurable Q)
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (hdet : ∀ z, (Q z).val.det = 1) (h : H) (w : ResidualTuple d) :
    let charts := primitiveCharts q d hd i hi Q hQ hfirst hdet
    let c := charts (q.informative h)
    c.before = d ∧
      c.after = (if q.informative h then Function.update d i (n+1) else d) ∧
      (c.taggedUpdate h ⟨d,w⟩).1 =
        primitiveAnswer (q.domainFrame h) (q.rangeFrame h) (castOrthogonal hi (w i))
          (q.vector h) (q.backward h) := by
  classical
  intro charts c
  by_cases hc : q.complement h = 0
  · have hs : q.informative h = false := by simp [FramedQuery.informative, hc]
    dsimp only [c, charts]
    rw [hs]
    exact ⟨rfl, rfl, (q.determined_answer h _ hc).symm⟩
  · have hs : q.informative h = true := by simp [FramedQuery.informative, hc]
    simp only [c, charts, hs, primitiveCharts, if_true]
    refine ⟨rfl, rfl, ?_⟩
    change q.encode h (selectedHaarStep Q hfirst (q.backward h) (q.unit h)
      (castOrthogonal hi (readTagged d ⟨d,w⟩ i))).1 = _
    rw [readTagged_mk, q.unit_eq h hc]
    have he := primitiveAnswer_eq (q.domainFrame h) (q.rangeFrame h) (castOrthogonal hi (w i))
      (q.vector h) (q.backward h) hc
    simpa only [FramedQuery.encode, FramedQuery.inputFrame, FramedQuery.outputFrame,
      FramedQuery.complement, selectedHaarStep, apply_ite Prod.fst] using he.symm

/-- With an available query under the source cap, the selected residual has
at least two dimensions. The zero/nonzero rank update matches the residual
dimension update and preserves the rank and query bounds at every label. -/
theorem primitive_rank_budget {N T k : ℕ} (rank count : Fin k → ℕ) (i : Fin k)
    (hr : ∀ j, rank j ≤ count j) (hcap : ∀ j, count j ≤ 2*T)
    (hnext : count i < 2*T) (hN : 2*T < N) (informative : Bool) :
    let d := fun j => N - rank j
    let nextRank := if informative then Function.update rank i (rank i + 1) else rank
    let nextCount := Function.update count i (count i + 1)
    2 ≤ d i ∧ (∀ j, nextRank j ≤ nextCount j ∧ nextCount j ≤ 2*T) ∧
      (fun j => N - nextRank j) =
        (if informative then Function.update d i (d i - 1) else d) := by
  intro d nextRank nextCount
  have hi := hr i
  refine ⟨show 2 ≤ N - rank i by omega, ?_, ?_⟩
  · intro j
    by_cases h : j = i
    · subst j
      cases informative <;> simp [nextRank, nextCount] <;> omega
    · cases informative <;> simpa [nextRank, nextCount, Function.update_of_ne h] using ⟨hr j, hcap j⟩
  · funext j
    by_cases h : j = i
    · subst j
      cases informative <;> simp [nextRank, d]
      omega
    · cases informative <;> simp [nextRank, d, Function.update_of_ne h]

#print axioms primitive_chart_correct
#print axioms primitive_rank_budget

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
