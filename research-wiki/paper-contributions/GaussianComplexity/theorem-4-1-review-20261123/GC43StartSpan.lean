import GC43Gaussian

/-! Almost-sure span statement in the Gaussianization step of Fact C.4. -/
noncomputable section

open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

theorem residual_eval {m : ℕ} (r : ℕ) (j : Fin m) :
    ∃ i : Fin (m+r), ∀ x : Vec (m+r), residualCoords m r x j = x i := by
  induction r with
  | zero => exact ⟨j, fun _ => rfl⟩
  | succ r ih =>
    obtain ⟨i,hi⟩ := ih
    exact ⟨i.succ, fun x => hi (fun k => x k.succ)⟩

theorem gaussian_residual_ne_zero {m r : ℕ} [NeZero m] :
    ∀ᵐ x ∂stdGaussian (E (m+r)), ‖WithLp.toLp 2 (residualCoords m r (WithLp.ofLp x))‖ ≠ 0 := by
  let := nullSingletonClass_gaussianReal (μ := (0 : ℝ)) (v := 1) one_ne_zero
  obtain ⟨i,hi⟩ := residual_eval r (0 : Fin m)
  have hγ : MeasurePreserving (WithLp.toLp 2 : Vec (m+r) → E (m+r))
      (Measure.pi (fun _ : Fin (m+r) => gaussianReal 0 1)) (stdGaussian (E (m+r))) :=
    ⟨(PiLp.continuous_toLp 2 _).measurable, map_pi_eq_stdGaussian⟩
  have hcoord : ∀ᵐ x ∂(Measure.pi (fun _ : Fin (m+r) => gaussianReal 0 1)), x i ≠ 0 :=
    (measurePreserving_eval (fun _ : Fin (m+r) => gaussianReal 0 1) i).quasiMeasurePreserving.ae
      (show ∀ᵐ x ∂gaussianReal 0 1, x ≠ 0 by simp [ae_iff])
  have hm : Measurable (fun x : E (m+r) => ‖WithLp.toLp 2 (residualCoords m r x.ofLp)‖) :=
    ((PiLp.continuous_toLp 2 _).comp ((continuous_residualCoords m r).comp
      (PiLp.continuous_ofLp 2 _))).norm.measurable
  rw [← hγ.map_eq]
  apply (ae_map_iff hγ.measurable.aemeasurable (p := fun x : E (m+r) =>
    ‖WithLp.toLp 2 (residualCoords m r x.ofLp)‖ ≠ 0) _).2
  rotate_left
  · exact ((measurableSet_singleton (0 : ℝ)).compl.preimage hm)
  filter_upwards [hcoord] with x hx
  intro h
  have hh := norm_eq_zero.mp h
  have hz := congrArg (fun c : E m => WithLp.ofLp c (0 : Fin m)) hh
  exact hx ((hi x).symm.trans hz)

private theorem splitVec_sub_smul {m : ℕ} (r : ℕ) (a b : Vec r) (z : Vec m) (s t l : ℝ) :
    splitVec r a (s • z) - l • splitVec r b (t • z) =
      splitVec r (a - l • b) ((s - l * t) • z) := by
  induction r with
  | zero =>
    ext i
    simp only [splitVec, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
    ring
  | succ r ih =>
    funext i
    cases i using Fin.cases with
    | zero => simp [splitVec]
    | succ i =>
      have h := congrFun (ih (fun j => a j.succ) (fun j => b j.succ)) i
      exact h

/-- Any response with the revealed residual direction belongs to the old exposed
subspace plus the single new Gaussian. The rank may be zero. -/
theorem gaussianize_span_of_residual_ne {m r : ℕ} [NeZero m] (D : O (m+r))
    (P : Submodule ℝ (Vec (m+r))) (hP : ∀ a : Vec r, act D (splitVec r a (0 : Vec m)) ∈ P) :
    ∀ (x : E (m+r)), ‖WithLp.toLp 2 (residualCoords m r x.ofLp)‖ ≠ 0 →
      ∀ (z : S m) (a : Vec r) (s : ℝ),
      encodeResponse D a s z ∈ P ⊔ ℝ ∙ (gaussianize D x z).ofLp := by
  intro x hx z a s
  let b := exposedCoords m r x.ofLp
  let t := ‖WithLp.toLp 2 (residualCoords m r x.ofLp)‖
  let g := (gaussianize D x z).ofLp
  have he : encodeResponse D a s z - (s / t) • g = act D (splitVec r (a - (s / t) • b) 0) := by
    change D.val *ᵥ splitVec r a (s • z.val.ofLp) -
      (s / t) • (D.val *ᵥ splitVec r b (t • z.val.ofLp)) = _
    rw [← Matrix.mulVec_smul, ← Matrix.mulVec_sub, splitVec_sub_smul,
      div_mul_cancel₀ s hx, sub_self, zero_smul]
    rfl
  have hm : encodeResponse D a s z - (s/t) • g ∈ P := he ▸ hP _
  exact (Submodule.mem_sup.mpr ⟨_, hm, _, Submodule.smul_mem _ _ (Submodule.mem_span_singleton_self g),
    sub_add_cancel _ _⟩)

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
