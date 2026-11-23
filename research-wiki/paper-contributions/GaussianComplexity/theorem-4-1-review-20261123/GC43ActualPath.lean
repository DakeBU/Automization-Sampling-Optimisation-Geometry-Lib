import GC43Flow
import GC43Path

/-! # Alternating inverse and forward queries realizing one first-order call

The last inverse query reveals the actual returned vector in hidden coordinates.
Forward steps use the disclosed diagonal matrix on each previously pulled query.
-/
noncomputable section
open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior (precisionReply)
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

variable {d q : ℕ} {Seed State : Type*} [MeasurableSpace Seed] [MeasurableSpace State]

def alternatingBack (t : ℕ) : Bool := decide (t%2=0)

def alternatingVector (alg : Algorithm d Seed State) (κ : ℝ) (q t : ℕ) (s : State × Vec d) : Vec d :=
  if alternatingBack t then
    WithLp.ofLp (if t=2*q then alg.output s.1 else queryOrZero alg s.1)
  else diagonalPrecision d κ *ᵥ s.2

def alternatingUpdate (alg : Algorithm d Seed State) (t : ℕ) (s : State × Vec d) (v : Vec d) : State × Vec d :=
  if alternatingBack t then (s.1,v) else (observedStep alg s.1 (WithLp.toLp 2 v),0)

def alternatingProgram (alg : Algorithm d Seed State) (κ : ℝ) (q : ℕ) : Program d (State × Vec d) where
  back := alternatingBack
  vector := alternatingVector alg κ q
  update := alternatingUpdate alg
  measurable_vector := by
    intro t
    unfold alternatingVector
    split_ifs
    · exact (PiLp.continuous_ofLp 2 _).measurable.comp (alg.measurable_output.comp measurable_fst)
    · exact (PiLp.continuous_ofLp 2 _).measurable.comp ((measurable_queryOrZero alg).comp measurable_fst)
    · exact ((continuous_const.matrix_mulVec continuous_id : Continuous (fun v : Vec d =>
        diagonalPrecision d κ *ᵥ v)).measurable.comp measurable_snd)
  measurable_update := by
    intro t
    unfold alternatingUpdate Function.uncurry
    split_ifs
    · exact (measurable_fst.comp measurable_fst).prodMk measurable_snd
    · exact ((measurable_observedStep alg).comp ((measurable_fst.comp measurable_fst).prodMk
        ((PiLp.continuous_toLp 2 _).measurable.comp measurable_snd))).prodMk measurable_const

/-- The primitive's underlying rotation is the same at every clock tick. -/
def actionAt {S : Type*} [MeasurableSpace S] (P : Program d S) (O : HaarConditional.O d) (t : ℕ) (s : S) : Vec d :=
  if P.back t then act O⁻¹ (P.vector t s) else act O (P.vector t s)

private theorem back_even (i : ℕ) : alternatingBack (2*i) = true := by simp [alternatingBack]
private theorem back_odd (i : ℕ) : alternatingBack (2*i+1) = false := by simp [alternatingBack]

theorem act_inverse_coordinates (O : HaarConditional.O d) (v : Vec d) :
    act O⁻¹ v = O.val.transpose *ᵥ v := by
  rfl

theorem paired_updates (alg : Algorithm d Seed State) (κ : ℝ) {q i : ℕ} (hi : i < q)
    (O : HaarConditional.O d) (s : State × Vec d) :
    let P := alternatingProgram alg κ q
    let t := 2*i
    let y := P.update t s (actionAt P O t s)
    P.update (t+1) y (actionAt P O (t+1) y) =
      (observedStep alg s.1 (precisionReply (hiddenPrecision κ O) (queryOrZero alg s.1)).2,0) := by
  have hne : 2*i ≠ 2*q := by omega
  simp only [alternatingProgram,alternatingVector,alternatingUpdate,actionAt,back_even,back_odd,
    Bool.false_eq_true,if_false,if_true,hne,act_inverse_coordinates,gradient_hiddenPrecision]
  rfl

/-- The transcript of the alternating program returns to the true bounded
algorithm state every two clock ticks. The final primitive response is OᵀX. -/
theorem alternating_final_answer (alg : Algorithm d Seed State) (κ : ℝ) (q : ℕ)
    (O : HaarConditional.O d) (s : Seed) (path : ℕ → State × Vec d)
    (h₀ : path 0 = (alg.start s,0))
    (hstep : ∀ t < 2*q, path (t+1) = (alternatingProgram alg κ q).update t (path t)
      (actionAt (alternatingProgram alg κ q) O t (path t))) :
    actionAt (alternatingProgram alg κ q) O (2*q) (path (2*q)) =
      O.val.transpose *ᵥ WithLp.ofLp (alg.sample q (hiddenPrecision κ O) s) := by
  have hs (i : ℕ) (hi : i ≤ q) : path (2*i) = (paddedState alg (hiddenPrecision κ O) i s,0) := by
    induction i with
    | zero => simpa only [Nat.mul_zero,paddedState_zero] using h₀
    | succ i ih =>
      have h₁ := hstep (2*i) (by omega)
      have h₂ := hstep (2*i+1) (by omega)
      rw [h₁] at h₂
      rw [paired_updates alg κ (by omega : i < q) O (path (2*i)), ih (by omega)] at h₂
      simpa [Nat.mul_succ,paddedState_succ,add_assoc] using h₂
  rw [hs q le_rfl]
  simp only [actionAt,alternatingProgram,alternatingVector,back_even,if_true,act_inverse_coordinates]
  rfl

/-- Pair adjacent forward and inverse revelations and apply the degree-q
span induction. All members of the previous frames can depend on the path. -/
theorem krylov_of_alternating_frames (κ : ℝ) (g : Starts d q)
    (P : ℕ → Submodule ℝ (Vec d)) (y : Fin (q+1) → Vec d) (h₀ : P 0 = ⊥)
    (hpre : ∀ i, y i ∈ P (2*i.val) ⊔ Submodule.span ℝ {WithLp.ofLp (g i)})
    (hback : ∀ i : Fin q, P (2*i.val+1) ≤ P (2*i.val) ⊔ Submodule.span ℝ {y i.castSucc})
    (hfwd : ∀ i : Fin q, P (2*i.val+2) ≤ P (2*i.val+1) ⊔
      Submodule.span ℝ {diagonalPrecision d κ *ᵥ y i.castSucc}) :
    y (Fin.last q) ∈ krylov d q κ g := by
  apply krylov_of_revelations κ g (fun t => P (2*t)) (fun i => y i.castSucc) _ (by simpa using h₀)
  · exact fun i => hpre i.castSucc
  · intro i
    rw [Nat.mul_succ]
    exact (hfwd i).trans (sup_le_sup_right (hback i) _)
  · exact hpre (Fin.last q)

#print axioms alternating_final_answer
#print axioms krylov_of_alternating_frames

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
