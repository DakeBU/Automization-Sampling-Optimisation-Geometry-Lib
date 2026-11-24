import GCCLiftInverse

noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantComponents
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.RotatedPreimageWitness

private def swapAxes : O 2 :=
  ⟨!![(0:ℝ),1;1,0],by
    apply (Matrix.mem_orthogonalGroup_iff (Fin 2) ℝ).2
    ext i j
    fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply,Fin.sum_univ_two]⟩

local instance : IsProbabilityMeasure (orthogonalHaar 1) := (orthogonalHaar_spec 1).1

private def F : BlockFrame 2 1 := ⟨1,rfl,swapAxes,1⟩
private def x : Vec 2 := ![3,4]

private theorem known : knownPreimage F x = ![0,3] := by
  change act swapAxes (splitVec 1 (exposedCoords 1 1 (act (1 : O 2)⁻¹ x)) 0) = _
  rw [inv_one,show act (1 : O 2) x = x from Matrix.one_mulVec _]
  funext i
  fin_cases i <;> norm_num [act,swapAxes,x,splitVec,exposedCoords,Matrix.mulVec,dotProduct,Fin.sum_univ_two]

private theorem scale : ‖frameComplement F true x‖ = 4 := by
  let c := frameComplement F true x
  have h : c.ofLp = (![4] : Vec 1) := by
    change residualCoords 1 1 (act (1 : O 2)⁻¹ x) = _
    rw [inv_one,show act (1 : O 2) x = x from Matrix.one_mulVec _]
    funext i
    fin_cases i; rfl
  have e := EuclideanSpace.real_norm_sq_eq c
  change ‖c‖^2 = ∑ i, c.ofLp i ^ 2 at e
  rw [h] at e
  norm_num [Fin.sum_univ_one] at e
  change ‖c‖ = 4
  nlinarith [norm_nonneg c]

private theorem explicit_preimage (W : O 1) :
    response true (F.realize W) x = ![4 * W.val 0 0,3] := by
  change act (framed (r := 1) swapAxes 1 W)⁻¹ x = _
  have hx : x = act (1 : O 2) (splitVec 1 (![3] : Vec 1) (![4] : Vec 1)) := by
    have hh : splitVec 1 (![3] : Vec 1) (![4] : Vec 1) = x := by
      funext i; fin_cases i <;> rfl
    rw [hh]; exact (Matrix.one_mulVec _).symm
  rw [hx,inverse_response]
  funext i; fin_cases i <;>
    simp [act,swapAxes,splitVec,Matrix.mulVec,dotProduct,Fin.sum_univ_two,mul_comm]

private theorem explicit_residual (W : O 1) :
    normalizedPreimage F (F.realize W) x = ![W.val 0 0,0] := by
  rw [normalizedPreimage,scale,known,explicit_preimage]
  ext i
  fin_cases i <;> norm_num [Pi.smul_apply]
  ring

private theorem prior : HaarState (orthogonalHaar 1) (fun _ => ()) F.realize (fun _ : Unit => F) id := by
  refine ⟨measurable_const,measurable_const,F.measurable_realize,?_,ae_of_all _ (fun _ => rfl)⟩
  refine ⟨measurable_const.prodMk measurable_id,?_⟩
  rw [Measure.map_const,measure_univ,one_smul,Measure.dirac_prod]
  rfl

/-- Input (3,4) has a nonzero known component and a nonzero component in the
one-dimensional unexposed space. Swapping the frame axes sends the known first
coordinate to the second coordinate of the preimage. -/
theorem rotated_last_axis :
    (∀ W : O 1, knownPreimage F x = (![0,3] : Vec 2) ∧
      normalizedPreimage F (F.realize W) x = ![W.val 0 0,0] ∧
      response true (F.realize W) x = ![0,3] + (4:ℝ) • normalizedPreimage F (F.realize W) x) ∧
    (∀ᵐ a ∂(orthogonalHaar 1).map (fun _ => ()), condDistrib
      (fun W => WithLp.toLp 2 (normalizedPreimage F (F.realize W) x))
      (fun _ => ()) (orthogonalHaar 1) a = complementSphere (exposedEuclidean swapAxes 1)) := by
  refine ⟨fun W => ⟨known,explicit_residual W,?_⟩,?_⟩
  · simpa only [known,scale] using HaarRevelation.preimage_decomposition F W x
  · apply prior.preimage_uniform_complement (x := fun _ => x) measurable_const
    exact ae_of_all _ (fun _ hc => by have h := scale; rw [hc,norm_zero] at h; norm_num at h)

/-- In the final residual dimension, the ambient directions (1,0) and (-1,0) each
have probability exactly one half. The observed coordinate contributes a separate (0,3). -/
theorem opposite_directions_half :
    (orthogonalHaar 1) {W | normalizedPreimage F (F.realize W) x = (![1,0] : Vec 2)} = (2 : ℝ≥0∞)⁻¹ ∧
    (orthogonalHaar 1) {W | normalizedPreimage F (F.realize W) x = (![-1,0] : Vec 2)} = (2 : ℝ≥0∞)⁻¹ := by
  have e (s : ℝ) : {W : O 1 | normalizedPreimage F (F.realize W) x = (![s,0] : Vec 2)} =
      {W : O 1 | W.val.det = s} := by
    ext W
    change normalizedPreimage F (F.realize W) x = _ ↔ W.val.det = s
    rw [explicit_residual,Matrix.det_fin_one]
    constructor
    · intro h; exact congrFun h 0
    · intro h; rw [h]
  rw [e,e]
  exact ⟨(component_probabilities (n := 1) (by decide)).1,
    (component_probabilities (n := 1) (by decide)).2.1⟩

#print axioms rotated_last_axis
#print axioms opposite_directions_half
end AutoSamplingTheory.ExampleCases.GaussianComplexity.RotatedPreimageWitness
