import B3AdaptiveQuery
import B3FrameUpdate

/-!
# The response of the actual matrix oracle

Fix the queried block and current dimensions in the informative branch of
Zhou–Suzuki, Lemma B.3. Feed an arbitrary history-measurable ambient vector
to the reconstructed matrix or its transpose. The joint law of that response,
the old history and the tuple of actual updated residuals has a product form.
-/

open Matrix MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.TechnicalLemmas.Probability.ParameterizedPushforward

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

/-- Choose the input frame from the domain and range frames. Interchanging
the last two arguments selects the output frame. -/
def queryFrame {m : ℕ} (backward : Bool) (D R : O m) : O m :=
  if backward then R else D

theorem measurable_queryFrame {H : Type*} [MeasurableSpace H] {m : ℕ}
    {b : H → Bool} {D R : H → O m} (hb : Measurable b) (hD : Measurable D)
    (hR : Measurable R) : Measurable (fun h => queryFrame (b h) (D h) (R h)) :=
  Measurable.ite (hb (measurableSet_singleton true)) hR hD

/-- The orthogonal-complement coordinates of the ambient query. -/
noncomputable def queryComplement {m r : ℕ} (F : O (m+r)) (v : Vec (m+r)) : E m :=
  WithLp.toLp 2 (residualCoords m r (act F⁻¹ v))

theorem measurable_queryComplement {H : Type*} [MeasurableSpace H] {m r : ℕ}
    {F : H → O (m+r)} {v : H → Vec (m+r)} (hF : Measurable F) (hv : Measurable v) :
    Measurable (fun h => queryComplement (F h) (v h)) :=
  (PiLp.continuous_toLp 2 (fun _ : Fin m => ℝ)).measurable.comp
    ((continuous_residualCoords m r).measurable.comp
      ((continuous_act _).measurable.comp (hF.inv.prodMk hv)))

/-- The vector returned when the queried ambient block is applied to the input. -/
noncomputable def primitiveAnswer {m r : ℕ} (D R : O (m+r)) (W : O m) (v : Vec (m+r))
    (backward : Bool) : Vec (m+r) :=
  if backward then act (framed D R W)⁻¹ v else act (framed D R W) v

/-- Compute the response from the public frames, the query, and a sphere observation. -/
noncomputable def responseFromSphere {m r : ℕ} (input output : O (m+r))
    (v : Vec (m+r)) (z : S m) : Vec (m+r) :=
  encodeResponse output (exposedCoords m r (act input⁻¹ v)) ‖queryComplement input v‖ z

theorem measurable_responseFromSphere {H : Type*} [MeasurableSpace H] {m r : ℕ}
    {input output : H → O (m+r)} {v : H → Vec (m+r)}
    (hi : Measurable input) (ho : Measurable output) (hv : Measurable v) :
    Measurable (fun p : H × S m => responseFromSphere (input p.1) (output p.1) (v p.1) p.2) :=
  measurable_encodeResponse (ho.comp measurable_fst)
    (((continuous_exposedCoords m r).measurable.comp
      ((continuous_act _).measurable.comp (hi.inv.prodMk hv))).comp measurable_fst)
    ((measurable_queryComplement hi hv).norm.comp measurable_fst) measurable_snd

theorem primitiveAnswer_eq {m r : ℕ} (D R : O (m+r)) (W : O m) (v : Vec (m+r))
    (b : Bool) (hc : queryComplement (queryFrame b D R) v ≠ 0) :
    let u := residualUnit ⟨queryComplement (queryFrame b D R) v, hc⟩
    primitiveAnswer D R W v b = responseFromSphere (queryFrame b D R) (queryFrame b R D) v
      (if b then rotate W⁻¹ u else rotate W u) := by
  let F := queryFrame b D R
  let a := exposedCoords m r (act F⁻¹ v)
  let c : {x : E m // x ≠ 0} := ⟨queryComplement F v, hc⟩
  have hv : act F (splitVec r a (‖c.val‖ • WithLp.ofLp (residualUnit c).val)) = v := by
    rw [scaled_residualUnit]
    exact query_from_coordinates F v
  cases b
  · exact (congrArg (act (framed D R W)) hv.symm).trans
      (normalized_responses D R W a ‖c.val‖ (residualUnit c)).1
  · exact (congrArg (act (framed D R W)⁻¹) hv.symm).trans
      (normalized_responses D R W a ‖c.val‖ (residualUnit c)).2

/-- Joint law of the ambient response to an informative primitive query and
all the labeled new residuals, for history-dependent vectors, frames and senses. -/
theorem primitive_haar_query {H : Type*} [MeasurableSpace H] {k r : ℕ}
    (ρ : Measure H) [SFinite ρ] (dim : Fin (k+1) → ℕ) (hd : ∀ j, 0 < dim j)
    (i : Fin (k+1)) (n : ℕ) (hi : dim i = n+2) (b : ℝ) (hb : b = -1 ∨ b = 1)
    (Q : S (n+2) → O (n+2)) (hQ : Measurable Q)
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (hdet : ∀ z, (Q z).val.det = 1)
    (D R : H → O ((n+2)+r)) (hD : Measurable D) (hR : Measurable R)
    (backward : H → Bool) (hbw : Measurable backward)
    (v : H → Vec ((n+2)+r)) (hv : Measurable v)
    (hc : ∀ h, queryComplement (queryFrame (backward h) (D h) (R h)) (v h) ≠ 0) :
    let input := fun h => queryFrame (backward h) (D h) (R h)
    let output := fun h => queryFrame (backward h) (R h) (D h)
    let u := fun h => residualUnit ⟨queryComplement (input h) (v h), hc h⟩
    let read := fun h => updateHaarTuple dim i n hi Q hfirst (backward h) (u h)
    let answer := fun h (x : ∀ j, O (dim j)) =>
      primitiveAnswer (D h) (R h) (castOrthogonal hi (x i)) (v h) (backward h)
    let encode := fun h => responseFromSphere (input h) (output h) (v h)
    let μ := Measure.pi fun j => componentHaar (dim j) b
    let ν := Measure.pi fun j => componentHaar (Function.update dim i (n+1) j) b
    (ρ.prod μ).map (fun p => ((p.1, answer p.1 p.2), (read p.1 p.2).2)) =
      (ρ ⊗ₘ kernel (sphereProbability (n+2)) encode).prod ν := by
  intro input output u read answer encode μ ν
  have hin : Measurable input := measurable_queryFrame hbw hD hR
  have hout : Measurable output := measurable_queryFrame hbw hR hD
  have hu : Measurable u := (continuous_residualUnit _).measurable.comp
    ((measurable_queryComplement hin hv).subtype_mk (h := hc))
  have he : Measurable (Function.uncurry encode) := measurable_responseFromSphere hin hout hv
  have hobs (h : H) (x : ∀ j, O (dim j)) : answer h x = encode h (read h x).1 := by
    have heq := primitiveAnswer_eq (D h) (R h) (castOrthogonal hi (x i)) (v h) (backward h) (hc h)
    cases hcase : backward h <;>
      simpa only [answer, encode, read, updateHaarTuple, selectedHaarStep, input, output, u,
        hcase, Bool.false_eq_true, if_false, if_true] using heq
  simp_rw [hobs]
  exact adaptive_haar_query ρ dim hd i n hi b hb Q hQ hfirst hdet backward hbw u hu encode he

#print axioms primitive_haar_query

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
