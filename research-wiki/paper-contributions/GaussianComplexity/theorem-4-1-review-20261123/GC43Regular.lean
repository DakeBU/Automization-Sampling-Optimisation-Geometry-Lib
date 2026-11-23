import GC43Flow

noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

def Regular {N : ℕ} (x : E N) : Prop := ∀ i, x.ofLp i ≠ 0

theorem gaussian_regular (N : ℕ) : ∀ᵐ x ∂stdGaussian (E N), Regular x := by
  let := nullSingletonClass_gaussianReal (μ := (0 : ℝ)) (v := 1) one_ne_zero
  have hh : ∀ᵐ x ∂(Measure.pi (fun _ : Fin N => gaussianReal 0 1)), ∀ i, x i ≠ 0 := by
    apply ae_all_iff.mpr
    intro i
    exact (measurePreserving_eval (fun _ : Fin N => gaussianReal 0 1) i).quasiMeasurePreserving.ae
      (show ∀ᵐ x ∂gaussianReal 0 1, x ≠ 0 by simp [ae_iff])
  rw [← map_pi_eq_stdGaussian]
  apply (ae_map_iff (PiLp.continuous_toLp 2 _).measurable.aemeasurable (p := Regular) _).2
  · exact hh
  · exact MeasurableSet.iInter (fun i : Fin N => ((measurableSet_singleton (0 : ℝ)).compl.preimage
      (EuclideanSpace.proj i).continuous.measurable)) |>.congr (by ext; simp [Regular])

theorem regular_start_array (N fuel : ℕ) :
    ∀ᵐ z ∂(Measure.pi (fun _ : Fin fuel => stdGaussian (E N))), ∀ i, Regular (z i) :=
  ae_all_iff.mpr (fun i =>
    (measurePreserving_eval (fun _ : Fin fuel => stdGaussian (E N)) i).quasiMeasurePreserving.ae
      (gaussian_regular N))

theorem frameStart_mem {N m : ℕ} [NeZero m] (F : BlockFrame N m) (v : Vec N)
    (x : E N) (hx : Regular x) (z : S m) :
    frameResponse F true v z ∈ exposedSpace F.domain F.rank ⊔
      ℝ ∙ (perStepStart F true v x z).ofLp := by
  rcases F with ⟨r,h,D,R⟩
  subst N
  let F : BlockFrame (m+r) m := ⟨r,rfl,D,R⟩
  let c := queryComplement (m := m) (r := r) R v
  let a := exposedCoords m r (act R⁻¹ v)
  change encodeResponse D a ‖c‖ z ∈ exposedSpace D r ⊔ ℝ ∙ (perStepStart F true v x z).ofLp
  have hP (t : Vec r) : act D (splitVec r t (0 : Vec m)) ∈ exposedSpace D r := by
    rw [exposedSpace_iff, act_inv_act, residualCoords_splitVec]
  by_cases hc : c = 0
  · have hzero : encodeResponse D a ‖c‖ z = act D (splitVec r a (0 : Vec m)) := by
      simp [hc,encodeResponse]
    rw [hzero]
    exact Submodule.mem_sup_left (hP a)
  · have he : perStepStart F true v x z = gaussianize D x z := by
      change (if true = true ∧ c ≠ 0 then _ else _) = _
      rw [if_pos ⟨rfl,hc⟩]
      rfl
    rw [he]
    apply gaussianize_span_of_residual_ne D _ hP x _ z a _
    obtain ⟨i,hi⟩ := residual_eval r (0 : Fin m)
    intro hz
    have e := congrArg (fun e : E m => e.ofLp (0 : Fin m)) (norm_eq_zero.mp hz)
    exact hx i ((hi x.ofLp).symm.trans e)

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
