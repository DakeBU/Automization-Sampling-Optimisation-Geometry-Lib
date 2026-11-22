import B2JointLaw

open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarStabilizerBlock

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames

set_option autoImplicit false

/-- The first `r` coordinates are fixed, and the last `m` carry the orthogonal matrix. -/
def prefixEmbed (m : ℕ) : (r : ℕ) → O m →* O (m + r)
  | 0 => MonoidHom.id _
  | r + 1 => (residualEmbed (m + r)).comp (prefixEmbed m r)

theorem continuous_prefixEmbed (m r : ℕ) : Continuous (prefixEmbed m r) := by
  induction r with
  | zero => exact continuous_id
  | succ r ih => exact (continuous_residualEmbed _).comp ih

theorem det_prefixEmbed {m : ℕ} (r : ℕ) (W : O m) :
    (prefixEmbed m r W).val.det = W.val.det := by
  induction r with
  | zero => rfl
  | succ r ih => exact (det_residualEmbed _).trans ih

private theorem residualEmbed_heq {m n : ℕ} (h : m = n) {A : O m} {B : O n}
    (hAB : HEq A B) : HEq (residualEmbed m A) (residualEmbed n B) := by
  subst n
  cases eq_of_heq hAB
  rfl

/-- In the ambient dimension equality `(m+1)+r = m+(r+1)`, the nested block is exactly
the rank-`r+1` prefixed embedding. -/
theorem prefixEmbed_next {m : ℕ} (r : ℕ) (V : O m) :
    HEq (prefixEmbed (m+1) r (residualEmbed m V)) (prefixEmbed m (r+1) V) := by
  induction r with
  | zero => rfl
  | succ r ih => exact residualEmbed_heq (show (m+1)+r = m+(r+1) by omega) ih

abbrev Vec (m : ℕ) := Fin m → ℝ

/-- Concatenate the exposed coordinates and the residual coordinates. -/
def splitVec {m : ℕ} : (r : ℕ) → Vec r → Vec m → Vec (m + r)
  | 0, _, c => c
  | r + 1, a, c => Fin.cons (a 0) (splitVec r (fun i => a i.succ) c)

/-- Read the last `m` coordinates in a frame with `r` exposed directions. -/
def residualCoords (m : ℕ) : (r : ℕ) → Vec (m + r) → Vec m
  | 0, x => x
  | r + 1, x => residualCoords m r (fun i => x i.succ)

/-- Read the initial exposed coordinates. -/
def exposedCoords (m : ℕ) : (r : ℕ) → Vec (m + r) → Vec r
  | 0, _ => Fin.elim0
  | r + 1, x => Fin.cons (x 0) (exposedCoords m r (fun i => x i.succ))

theorem residualCoords_splitVec {m : ℕ} (r : ℕ) (a : Vec r) (c : Vec m) :
    residualCoords m r (splitVec r a c) = c := by
  induction r with
  | zero => rfl
  | succ r ih =>
    simpa only [residualCoords, splitVec, Fin.cons_succ] using ih (fun i => a i.succ)

theorem splitVec_coords (m r : ℕ) (x : Vec (m+r)) :
    splitVec r (exposedCoords m r x) (residualCoords m r x) = x := by
  induction r with
  | zero => rfl
  | succ r ih =>
    simp only [exposedCoords, residualCoords, splitVec, Fin.cons_zero, Fin.cons_succ, ih]
    exact Fin.cons_self_tail x

noncomputable def act {m : ℕ} (R : O m) (x : Vec m) : Vec m := R.val *ᵥ x

theorem act_mul {m : ℕ} (R D : O m) (x : Vec m) :
    act (R * D) x = act R (act D x) := (Matrix.mulVec_mulVec _ _ _).symm

@[simp] theorem act_inv_act {m : ℕ} (R : O m) (x : Vec m) :
    act R⁻¹ (act R x) = x := by
  rw [← act_mul, inv_mul_cancel]
  exact Matrix.one_mulVec _

private theorem act_residualEmbed {m : ℕ} (W : O m) (s : ℝ) (x : Vec m) :
    act (residualEmbed m W) (Fin.cons s x) = Fin.cons s (act W x) := by
  funext i
  cases i using Fin.cases <;>
    simp [act, residualEmbed_val, blockMatrix, Matrix.mulVec, dotProduct, Fin.sum_univ_succ]

theorem act_prefixEmbed {m : ℕ} (r : ℕ) (W : O m) (a : Vec r) (c : Vec m) :
    act (prefixEmbed m r W) (splitVec r a c) = splitVec r a (act W c) := by
  induction r with
  | zero => rfl
  | succ r ih =>
    change act (residualEmbed _ (prefixEmbed _ r W))
      (Fin.cons (a 0) (splitVec r (fun i => a i.succ) c)) = _
    rw [act_residualEmbed, ih]
    rfl

/-- The inner one-coordinate embedding supplies the next exposed direction after the old ones. -/
theorem act_nextBlock {m : ℕ} (r : ℕ) (V : O m) (a : Vec r) (s : ℝ) (c : Vec m) :
    act (prefixEmbed (m+1) r (residualEmbed m V)) (splitVec r a (Fin.cons s c)) =
      splitVec r a (Fin.cons s (act V c)) := by
  rw [act_prefixEmbed, act_residualEmbed]

/-- The ambient matrix reconstructed from the two frames and the residual block. -/
noncomputable def framed {m r : ℕ} (D R : O (m+r)) (W : O m) : O (m+r) :=
  R * prefixEmbed m r W * D⁻¹

theorem framed_inv {m r : ℕ} (D R : O (m+r)) (W : O m) :
    (framed D R W)⁻¹ = framed R D W⁻¹ := by
  simp only [framed, _root_.mul_inv_rev, inv_inv, map_inv, mul_assoc]

theorem forward_response {m r : ℕ} (D R : O (m+r)) (W : O m) (a : Vec r) (c : Vec m) :
    act (framed D R W) (act D (splitVec r a c)) = act R (splitVec r a (act W c)) := by
  rw [framed, act_mul, act_inv_act, act_mul, act_prefixEmbed]

theorem inverse_response {m r : ℕ} (D R : O (m+r)) (W : O m) (a : Vec r) (c : Vec m) :
    act (framed D R W)⁻¹ (act R (splitVec r a c)) = act D (splitVec r a (act W⁻¹ c)) := by
  rw [framed_inv, forward_response]

theorem zero_residual_response {m r : ℕ} (D R : O (m+r)) (W : O m) (a : Vec r) :
    act (framed D R W) (act D (splitVec r a 0)) = act R (splitVec r a 0) ∧
    act (framed D R W)⁻¹ (act R (splitVec r a 0)) = act D (splitVec r a 0) := by
  rw [forward_response, inverse_response]
  simp only [act, Matrix.mulVec_zero, and_self]

/-- The observable oracle response associated with a normalized residual observation. -/
noncomputable def encodeResponse {m r : ℕ} (F : O (m+r)) (a : Vec r) (s : ℝ) (z : S m) :
    Vec (m+r) :=
  act F (splitVec r a (s • WithLp.ofLp z.val))

/-- Apply the inverse frame, read the residual coordinates and divide by the residual norm. -/
noncomputable def readResponse {m r : ℕ} (F : O (m+r)) (s : ℝ) (y : Vec (m+r)) : Vec m :=
  s⁻¹ • residualCoords m r (act F⁻¹ y)

theorem read_encodeResponse {m r : ℕ} (F : O (m+r)) (a : Vec r) {s : ℝ} (hs : s ≠ 0)
    (z : S m) : readResponse F s (encodeResponse F a s z) = WithLp.ofLp z.val := by
  simp [readResponse, encodeResponse, act_inv_act, residualCoords_splitVec, smul_smul, hs]

theorem normalized_responses {m r : ℕ} (D R : O (m+r)) (W : O m)
    (a : Vec r) (s : ℝ) (u : S m) :
    act (framed D R W) (act D (splitVec r a (s • WithLp.ofLp u.val))) =
      encodeResponse R a s (rotate W u) ∧
    act (framed D R W)⁻¹ (act R (splitVec r a (s • WithLp.ofLp u.val))) =
      encodeResponse D a s (rotate W⁻¹ u) := by
  rw [forward_response, inverse_response]
  simp only [encodeResponse, act, rotate_val, Matrix.mulVec_smul, and_self]

/-- Extend an ambient frame by a rotation on just the residual coordinates. -/
noncomputable def extendFrame {m r : ℕ} (F : O (m+r)) (A : O m) : O (m+r) :=
  F * prefixEmbed m r A

theorem continuous_extendFrame (m r : ℕ) :
    Continuous (fun p : O (m+r) × O m => extendFrame p.1 p.2) :=
  continuous_fst.mul ((continuous_prefixEmbed m r).comp continuous_snd)

theorem extendFrame_oriented {m r : ℕ} {F : O (m+r)} {A : O m}
    (hF : F.val.det = 1) (hA : A.val.det = 1) : (extendFrame F A).val.det = 1 := by
  change (F.val * (prefixEmbed m r A).val).det = 1
  rw [Matrix.det_mul, det_prefixEmbed, hA, hF, one_mul]

theorem forward_frame_update {n r : ℕ} (D R : O ((n+2)+r))
    (Q : S (n+2) → O (n+2)) (u z : S (n+2)) (V : O (n+1)) :
    framed D R (assemble Q u z V) =
      framed (extendFrame D (Q u)) (extendFrame R (Q z)) (residualEmbed (n+1) V) := by
  simp only [framed, assemble, extendFrame, map_mul, map_inv, _root_.mul_inv_rev]
  group

theorem inverse_frame_update {n r : ℕ} (D R : O ((n+2)+r))
    (Q : S (n+2) → O (n+2)) (u z : S (n+2)) (V : O (n+1)) :
    framed D R (assemble Q u z V)⁻¹ =
      framed (extendFrame D (Q z)) (extendFrame R (Q u)) (residualEmbed (n+1) V⁻¹) := by
  simp only [framed, assemble, extendFrame, map_mul, map_inv, _root_.mul_inv_rev, inv_inv]
  group

/-- An arbitrary ambient query is recovered from its coordinates in a chosen frame. -/
theorem query_from_coordinates {m r : ℕ} (F : O (m+r)) (v : Vec (m+r)) :
    act F (splitVec r (exposedCoords m r (act F⁻¹ v)) (residualCoords m r (act F⁻¹ v))) = v := by
  rw [splitVec_coords, ← act_mul, mul_inv_cancel]
  exact Matrix.one_mulVec _

/-- Normalize the residual part using its Euclidean norm. -/
noncomputable def residualUnit {m : ℕ} (c : {x : E m // x ≠ 0}) : S m :=
  ⟨‖c.val‖⁻¹ • c.val, mem_sphere_zero_iff_norm.mpr (by
    simp [norm_smul, c.property])⟩

theorem continuous_residualUnit (m : ℕ) :
    Continuous (residualUnit (m := m)) := by
  apply Continuous.subtype_mk
  exact (continuous_subtype_val.norm.inv₀ (fun c => norm_ne_zero_iff.mpr c.property)).smul
    continuous_subtype_val

theorem scaled_residualUnit {m : ℕ} (c : {x : E m // x ≠ 0}) :
    ‖c.val‖ • WithLp.ofLp (residualUnit c).val = WithLp.ofLp c.val := by
  change WithLp.ofLp (‖c.val‖ • ‖c.val‖⁻¹ • c.val) = _
  rw [smul_smul, mul_inv_cancel₀ (norm_ne_zero_iff.mpr c.property), one_smul]

theorem encodeResponse_injective {m r : ℕ} (F : O (m+r)) (a : Vec r) {s : ℝ} (hs : s ≠ 0) :
    Function.Injective (encodeResponse F a s) := by
  intro z z' h
  apply Subtype.ext
  apply (WithLp.equiv 2 (Vec m)).injective
  change WithLp.ofLp z.val = WithLp.ofLp z'.val
  simpa only [read_encodeResponse F a hs] using congrArg (readResponse F s) h

private theorem continuous_splitVec_family {H : Type*} [TopologicalSpace H] {m : ℕ}
    (r : ℕ) {a : H → Vec r} {c : H → Vec m} (ha : Continuous a) (hc : Continuous c) :
    Continuous (fun h => splitVec r (a h) (c h)) := by
  induction r with
  | zero => exact hc
  | succ r ih =>
    apply continuous_pi
    intro i
    cases i using Fin.cases with
    | zero =>
      simp only [splitVec, Fin.cons_zero]
      exact (continuous_apply 0).comp ha
    | succ i =>
      simp only [splitVec, Fin.cons_succ]
      have htail : Continuous (fun h (j : Fin r) => a h j.succ) :=
        continuous_pi fun (j : Fin r) => (continuous_apply j.succ).comp ha
      exact (continuous_apply i).comp (ih htail)

theorem continuous_residualCoords (m r : ℕ) : Continuous (residualCoords m r) := by
  induction r with
  | zero => exact continuous_id
  | succ r ih => exact ih.comp (continuous_pi fun i => continuous_apply i.succ)

theorem continuous_exposedCoords (m r : ℕ) : Continuous (exposedCoords m r) := by
  induction r with
  | zero => exact continuous_const
  | succ r ih =>
    apply continuous_pi
    intro i
    cases i using Fin.cases with
    | zero =>
      simp only [exposedCoords, Fin.cons_zero]
      exact continuous_apply 0
    | succ i =>
      simp only [exposedCoords, Fin.cons_succ]
      exact (continuous_apply i).comp (ih.comp (continuous_pi fun j => continuous_apply j.succ))

theorem continuous_act (m : ℕ) : Continuous (fun p : O m × Vec m => act p.1 p.2) :=
  (continuous_subtype_val.comp continuous_fst).matrix_mulVec continuous_snd

theorem measurable_encodeResponse {H : Type*} [MeasurableSpace H] {m r : ℕ}
    {F : H → O (m+r)} {a : H → Vec r} {s : H → ℝ} {z : H → S m}
    (hF : Measurable F) (ha : Measurable a) (hs : Measurable s) (hz : Measurable z) :
    Measurable (fun h => encodeResponse (F h) (a h) (s h) (z h)) := by
  have hsplit : Continuous (fun p : Vec r × Vec m => splitVec r p.1 p.2) :=
    continuous_splitVec_family r continuous_fst continuous_snd
  have hzv : Measurable (fun h => WithLp.ofLp (z h).val) :=
    (PiLp.continuous_ofLp 2 (fun _ : Fin m => ℝ)).measurable.comp
      (measurable_subtype_coe.comp hz)
  exact (continuous_act _).measurable.comp
    (hF.prodMk (hsplit.measurable.comp (ha.prodMk (hs.smul hzv))))

theorem measurable_readResponse {H : Type*} [MeasurableSpace H] {m r : ℕ}
    {F : H → O (m+r)} {s : H → ℝ} {y : H → Vec (m+r)}
    (hF : Measurable F) (hs : Measurable s) (hy : Measurable y) :
    Measurable (fun h => readResponse (F h) (s h) (y h)) :=
  hs.inv.smul ((continuous_residualCoords m r).measurable.comp
    ((continuous_act _).measurable.comp (hF.inv.prodMk hy)))

private noncomputable def spherePointOr {m : ℕ} (fallback : S m) (x : E m) : S m := by
  classical
  exact if hx : x ∈ Metric.sphere (0 : E m) 1 then ⟨x, hx⟩ else fallback

private theorem measurable_spherePointOr {m : ℕ} (fallback : S m) :
    Measurable (spherePointOr fallback) := by
  classical
  exact Measurable.dite measurable_id measurable_const
    (Metric.isClosed_sphere (x := (0 : E m)) (ε := 1)).measurableSet

/-- A sphere-valued decoder on all ambient responses, using the first coordinate as a
default outside the response fiber. -/
noncomputable def decodeResponse {m r : ℕ} [NeZero m] (F : O (m+r)) (s : ℝ)
    (y : Vec (m+r)) : S m :=
  spherePointOr (coordinatePoint 0) (WithLp.toLp 2 (readResponse F s y))

theorem measurable_decodeResponse {H : Type*} [MeasurableSpace H] {m r : ℕ} [NeZero m]
    {F : H → O (m+r)} {s : H → ℝ} {y : H → Vec (m+r)}
    (hF : Measurable F) (hs : Measurable s) (hy : Measurable y) :
    Measurable (fun h => decodeResponse (F h) (s h) (y h)) :=
  (measurable_spherePointOr _).comp ((PiLp.continuous_toLp 2 (fun _ : Fin m => ℝ)).measurable.comp
    (measurable_readResponse hF hs hy))

theorem decode_encodeResponse {m r : ℕ} [NeZero m] (F : O (m+r)) (a : Vec r) {s : ℝ}
    (hs : s ≠ 0) (z : S m) : decodeResponse F s (encodeResponse F a s z) = z := by
  rw [decodeResponse, read_encodeResponse F a hs, WithLp.toLp_ofLp]
  simp only [spherePointOr, z.property, dite_true]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
