import GCCFrameChart
import B4Frames

noncomputable section
open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarStabilizerBlock
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames

private theorem mul_projection_iff {N r : ℕ} (X : O N) :
    X.val * projectionMatrix (front N r) = projectionMatrix (front N r) ↔
      ∀ y ∈ front N r, act X y.ofLp = y.ofLp := by
  let M := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin N)
  have h (y : E N) : M X.val y = WithLp.toLp 2 (act X y.ofLp) := rfl
  have he : M (projectionMatrix (front N r)) = (front N r).starProjection := M.apply_symm_apply _
  constructor
  · intro e y hy
    have hh := congrArg (fun A : Mat N => M A y) e
    simp only [map_mul,he,mul_apply_eq_comp,
      (front N r).starProjection_eq_self_iff.mpr hy,h] at hh
    exact congrArg WithLp.ofLp hh
  · intro e
    apply M.injective
    rw [map_mul]
    change M X.val * M (projectionMatrix (front N r)) = M (projectionMatrix (front N r))
    rw [he]
    ext z : 1
    change M X.val ((front N r).starProjection z) = (front N r).starProjection z
    exact congrArg (WithLp.toLp 2) (e _ ((front N r).orthogonalProjectionOnto z).property)

private theorem residual_zero_of_front {m : ℕ} (r : ℕ) (v : Vec (m+r))
    (hv : ∀ i : Fin (m+r), r ≤ i.val → v i = 0) : residualCoords m r v = 0 := by
  induction r with
  | zero => funext i; exact hv i (Nat.zero_le _)
  | succ r ih => exact ih (fun i => v i.succ) (fun i hi => hv i.succ (by simpa using hi))

private theorem prefix_projection {m : ℕ} (r : ℕ) (W : O m) :
    (prefixEmbed m r W).val * projectionMatrix (front (m+r) r) = projectionMatrix (front (m+r) r) := by
  apply (mul_projection_iff _).2
  intro y hy
  have hc := residual_zero_of_front r y.ofLp hy
  have hs := splitVec_coords m r y.ofLp
  rw [hc] at hs
  calc
    _ = act (prefixEmbed m r W) (splitVec r (exposedCoords m r y.ofLp) (0 : Vec m)) := congrArg _ hs.symm
    _ = _ := by rw [act_prefixEmbed,show act W 0 = 0 from Matrix.mulVec_zero _]; exact hs

private theorem exists_prefix_of_cols {m : ℕ} (r : ℕ) (X : O (m+r))
    (hX : ∀ j : Fin (m+r), j.val < r → ∀ i, X.val i j = (1 : Mat (m+r)) i j) :
    ∃ W : O m, prefixEmbed m r W = X := by
  induction r with
  | zero => exact ⟨X,rfl⟩
  | succ r ih =>
    have hcol : X.val *ᵥ Pi.single (0 : Fin (m+r+1)) (1 : ℝ) = Pi.single 0 1 := by
      rw [Matrix.mulVec_single_one]
      funext i
      exact (hX 0 (Nat.zero_lt_succ _) i).trans (by
        classical
        simp [Matrix.one_apply,Pi.single_apply])
    let U : O (m+r) := ⟨lowerBlock X.val, lowerBlock_mem_orthogonal_of_fixes X hcol⟩
    have hU (j : Fin (m+r)) (hj : j.val < r) (i : Fin (m+r)) :
        U.val i j = (1 : Mat (m+r)) i j := by
      have t := hX j.succ (by simpa using hj) i.succ
      change X.val i.succ j.succ = (1 : Mat (m+r)) i j
      simpa only [Matrix.one_apply,Fin.succ_inj] using t
    obtain ⟨W,hW⟩ := ih U hU
    refine ⟨W,?_⟩
    change residualEmbed (m+r) (prefixEmbed m r W) = X
    rw [hW]
    exact residualEmbed_lowerBlock_of_fixes X hcol

private theorem exists_prefix_of_projection {m r : ℕ} (X : O (m+r))
    (hX : X.val * projectionMatrix (front (m+r) r) = projectionMatrix (front (m+r) r)) :
    ∃ W : O m, prefixEmbed m r W = X := by
  apply exists_prefix_of_cols
  intro j hj i
  let y := WithLp.toLp 2 (Pi.single j (1 : ℝ) : Vec (m+r))
  have hy : y ∈ front (m+r) r := by
    intro s hs
    have hsj : s ≠ j := by intro eq; subst s; omega
    exact Pi.single_eq_of_ne hsj _
  have e := congrFun ((mul_projection_iff X).1 hX y hy) i
  change (X.val *ᵥ Pi.single j (1 : ℝ)) i = (Pi.single j 1 : Vec (m+r)) i at e
  rw [Matrix.mulVec_single_one] at e
  simpa [Matrix.col_apply,Pi.single_apply,Matrix.one_apply,eq_comm] using e

/-- The orthogonal matrices consistent with the observed projector and partial action
are precisely the completions obtained by ranging over the full residual orthogonal group. -/
theorem range_realize_eq_compatible {N m : ℕ} (F : BlockFrame N m) :
    Set.range F.realize = {A : O N | A.val * (frameObservation F.rank (F.domain,F.range)).1 =
      (frameObservation F.rank (F.domain,F.range)).2} := by
  rcases F with ⟨r,e,D,R⟩; subst N
  let P := projectionMatrix (front (m+r) r)
  have hR' : R⁻¹.val * R.val = 1 := R.property.1
  have hD : D⁻¹.val * D.val = 1 := D.property.1
  ext A
  constructor
  · rintro ⟨W,rfl⟩
    change (R.val * (prefixEmbed m r W).val * D⁻¹.val) * (D.val * P * D⁻¹.val) = R.val * P * D⁻¹.val
    have hP : (prefixEmbed m r W).val * P = P := prefix_projection r W
    calc
      _ = R.val * ((prefixEmbed m r W).val * (D⁻¹.val * D.val) * P) * D⁻¹.val := by simp only [mul_assoc]
      _ = _ := by rw [hD,mul_one,hP]
  · intro he
    change A.val * (D.val * P * D⁻¹.val) = R.val * P * D⁻¹.val at he
    let X := R⁻¹ * A * D
    have hP : X.val * P = P := by
      change (R⁻¹.val * A.val * D.val) * P = P
      calc
        _ = R⁻¹.val * (A.val * (D.val * P * D⁻¹.val)) * D.val := by simp only [mul_assoc,hD,mul_one]
        _ = P := by rw [he]; simp only [← mul_assoc,hR',one_mul]; rw [mul_assoc,hD,mul_one]
    obtain ⟨W,hW⟩ := exists_prefix_of_projection X hP
    refine ⟨W,?_⟩
    change R * prefixEmbed m r W * D⁻¹ = A
    simp only [hW,X,mul_assoc,mul_inv_cancel,mul_one,mul_inv_cancel_left]
#print axioms range_realize_eq_compatible
end AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames
