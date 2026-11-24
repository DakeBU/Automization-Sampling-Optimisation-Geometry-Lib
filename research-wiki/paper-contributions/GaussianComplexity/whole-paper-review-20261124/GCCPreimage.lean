import GCCAmbientState
import GCCResidualLift
noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
open AutoSamplingTheory.TechnicalLemmas.Probability.ParameterizedPushforward
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

variable {N m : ℕ}

/-- The already known part of the preimage. In the public range frame keep the
first r coordinates, then put them back using the public domain frame. -/
def knownPreimage (F : BlockFrame N m) (x : Vec N) : Vec N :=
  castVec F.fits (act (castOrthogonal F.fits.symm F.domain)
    (splitVec F.rank (exposedCoords m F.rank (act (castOrthogonal F.fits.symm F.range)⁻¹
      (castVec F.fits.symm x))) (0 : Vec m)))

private theorem split_scaled (r : ℕ) (a : Vec r) (s : ℝ) (c : Vec m) :
    splitVec r a (s • c) = splitVec r a (0 : Vec m) + s • splitVec r 0 c := by
  induction r with
  | zero => simp [splitVec]
  | succ r ih =>
    funext i
    cases i using Fin.cases
    · simp [splitVec]
    · rename_i j
      exact congrFun (ih (fun i => a i.succ)) j

theorem frameResponse_preimage (F : BlockFrame N m) (x : Vec N) (z : S m) :
    frameResponse F true x z = knownPreimage F x +
      ‖frameComplement F true x‖ • residualLift F.domain F.rank F.fits z := by
  rcases F with ⟨r,e,D,R⟩; subst N
  change act D (splitVec r _ (‖queryComplement R x‖ • z.val.ofLp)) =
    act D (splitVec r _ (0 : Vec m)) + ‖queryComplement R x‖ • act D (splitVec r 0 (1 • z.val.ofLp))
  rw [one_smul, split_scaled]
  change D.val *ᵥ (_ + _ • _) = _ + _ • _
  rw [Matrix.mulVec_add, Matrix.mulVec_smul]
  rfl

/-- The normalized unknown part computed from the actual answer. It is zero
when the query has no component in the unexposed range. -/
def normalizedPreimage (F : BlockFrame N m) (A : O N) (x : Vec N) : Vec N :=
  ‖frameComplement F true x‖⁻¹ • (response true A x - knownPreimage F x)

theorem normalizedPreimage_lift [NeZero m] (F : BlockFrame N m) (W : O m) (x : Vec N)
    (hc : frameComplement F true x ≠ 0) :
    normalizedPreimage F (F.realize W) x =
      residualLift F.domain F.rank F.fits (frameObservation F true x W) := by
  rw [normalizedPreimage]
  change ‖frameComplement F true x‖⁻¹ • (act (F.realize W)⁻¹ x - _) = _
  rw [show act (F.realize W)⁻¹ x = frameResponse F true x (frameObservation F true x W) from
    frameAnswer_eq F true x W, frameResponse_preimage]
  simp [smul_smul,hc]

theorem preimage_decomposition [NeZero m] (F : BlockFrame N m) (W : O m) (x : Vec N) :
    response true (F.realize W) x = knownPreimage F x +
      ‖frameComplement F true x‖ • normalizedPreimage F (F.realize W) x := by
  by_cases c : frameComplement F true x = 0
  · have ey := (frameAnswer_eq F true x W).trans (frameResponse_preimage F x (frameObservation F true x W))
    simpa [response,c] using ey
  · rw [normalizedPreimage_lift F W x c]
    exact (frameAnswer_eq F true x W).trans (frameResponse_preimage F x (frameObservation F true x W))

variable {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H]
  {μ : Measure Ω} [IsFiniteMeasure μ] {h : Ω → H} {A : Ω → O N}

omit [IsFiniteMeasure μ] in
theorem HaarState.preimage_decomposition [NeZero m] {F : H → BlockFrame N m} {W : Ω → O m}
    (state : HaarState μ h A F W) (x : H → Vec N) :
    ∀ᵐ ω ∂μ, response true (A ω) (x (h ω)) = knownPreimage (F (h ω)) (x (h ω)) +
      ‖frameComplement (F (h ω)) true (x (h ω))‖ • normalizedPreimage (F (h ω)) (A ω) (x (h ω)) := by
  filter_upwards [state.reconstruct] with ω e
  rw [e]; exact HaarRevelation.preimage_decomposition (F (h ω)) (W ω) (x (h ω))

/-- On the nonzero query stratum the actual normalized vector in Equation
(27), conditional on the original history, has the image of the uniform
sphere under the isometric residual frame inclusion. -/
theorem HaarState.preimage_uniform {F : H → BlockFrame N (m+1)} {W : Ω → O (m+1)}
    (state : HaarState μ h A F W) {x : H → Vec N} (hx : Measurable x)
    (hc : ∀ᵐ ω ∂μ, frameComplement (F (h ω)) true (x (h ω)) ≠ 0) :
    ∀ᵐ a ∂μ.map h, condDistrib (fun ω => normalizedPreimage (F (h ω)) (A ω) (x (h ω))) h μ a =
      (sphereProbability (m+1)).map (residualLift (F a).domain (F a).rank (F a).fits) := by
  let := isProbabilityMeasure_sphereProbability (m+1)
  let u := fun a => frameUnit (F a) true (x a)
  have hu : Measurable u := measurable_frameUnit state.domain state.range measurable_const hx
  let z := fun ω => rotate (W ω)⁻¹ (u (h ω))
  let lift := fun a => residualLift (F a).domain (F a).rank (F a).fits
  have hL : Measurable (fun p : H × S (m+1) => lift p.1 p.2) :=
    measurable_residualLift (state.domain.comp measurable_fst) measurable_snd
  have hσ : LawGiven μ h z (sphereProbability (m+1)) := by
    have hf := (conditional_haar_revelation state.law true u hu).1
    have ee : (fun ω => (reveal true (u (h ω)) (W ω)).1) = z :=
      funext fun ω => reveal_direction true _ _
    rwa [ee] at hf
  let know := fun ω => normalizedPreimage (F (h ω)) (A ω) (x (h ω))
  let lifted := fun ω => lift (h ω) (z ω)
  have he : know =ᵐ[μ] lifted := by
    filter_upwards [hc,state.reconstruct] with ω c e
    change normalizedPreimage _ (A ω) _ = _
    rw [e]; exact normalizedPreimage_lift _ _ _ c
  change ∀ᵐ a ∂μ.map h, condDistrib know h μ a = _
  rw [condDistrib_congr he Filter.EventuallyEq.rfl]
  have joint : μ.map (fun ω => (h ω,lifted ω)) =
      ((μ.map h).prod (sphereProbability (m+1))).map (fun p : H × S (m+1) => (p.1,lift p.1 p.2)) := by
    rw [← hσ.map_eq,Measure.map_map (measurable_fst.prodMk hL) hσ.measurable]
    rfl
  let := isMarkovKernel_kernel (sphereProbability (m+1)) lift hL
  have hlifted : Measurable lifted := hL.comp hσ.measurable
  have key := condDistrib_ae_eq_of_measure_eq_compProd h hlifted.aemeasurable
    (joint.trans (map_prod_eq_compProd (μ.map h) (sphereProbability (m+1)) lift hL))
  filter_upwards [key] with a ha
  exact ha.trans (kernel_apply _ _ hL a)

#print axioms HaarState.preimage_uniform
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
