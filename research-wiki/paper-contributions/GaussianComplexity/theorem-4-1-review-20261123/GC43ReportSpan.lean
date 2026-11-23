import GC43ActualPath
import GC43WalkPath
import GC43CoupleLaw

/-! # The actual returned point belongs to the Krylov space of the even starts -/
noncomputable section
open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

/-- Appendix C.1, final span step on the actual finite sequence of reports.
Only inverse primitive times supply Gaussian starts, including the final output. -/
theorem actual_output_mem_of_walkPath {d : ℕ} {Seed State : Type*}
    [MeasurableSpace Seed] [MeasurableSpace State] (alg : Algorithm d Seed State)
    (κ : ℝ) (q : ℕ) (O : HaarConditional.O d) (s : Seed)
    (R : Fin (2*q+1) → Report d (State × Vec d))
    (hp : WalkPath (alternatingProgram alg κ q) 0 O (alg.start s,0) 1 0 R) :
    O.val.transpose *ᵥ WithLp.ofLp (alg.sample q (hiddenPrecision κ O) s) ∈
      krylov d q κ (fun i => (R (evenIndex q i)).start) := by
  let idx (t : ℕ) : Fin (2*q+1) := ⟨min t (2*q), by omega⟩
  have val (t : ℕ) (ht : t ≤ 2*q) : (idx t).val = t := min_eq_left ht
  let recd (t : ℕ) := R (idx t)
  let prog := alternatingProgram alg κ q
  let E (t : ℕ) := exposedSpace (recd t).priorDomain (recd t).priorRank
  let g : Starts d q := fun i => (R (evenIndex q i)).start
  let y (i : Fin (q+1)) := (recd (2*i.val)).answer
  have heven (i : Fin (q+1)) : idx (2*i.val) = evenIndex q i := Fin.ext (val _ (by omega))
  have hinit := hp.first (idx 0) (val 0 (by omega))
  have hstate₀ : (recd 0).priorState = (alg.start s,0) := hinit.1
  have hE₀ : E 0 = ⊥ := by
    change exposedSpace (R (idx 0)).priorDomain (R (idx 0)).priorRank = ⊥
    rw [hinit.2.1,hinit.2.2,exposedSpace_initial]
  have hnext (t : ℕ) (ht : t < 2*q) :
      (recd (t+1)).priorState = prog.update t (recd t).priorState (recd t).answer ∧
      E (t+1) = exposedSpace (recd t).nextDomain (recd t).nextRank := by
    have he := hp.adjacent (idx t) (idx (t+1)) (by rw [val _ (by omega),val _ ht.le])
    exact ⟨by simpa only [Nat.zero_add,val t ht.le] using he.1, by
      dsimp [E,recd]; rw [he.2.1,he.2.2]⟩
  have ha (t : ℕ) (ht : t ≤ 2*q) : (recd t).answer = actionAt prog O t (recd t).priorState := by
    simpa only [recd,actionAt,prog,Nat.zero_add,val t ht] using hp.answer (idx t)
  have last := alternating_final_answer alg κ q O s (fun t => (recd t).priorState) hstate₀
    (fun t ht => by rw [(hnext t ht).1, ha t ht.le])
  have hlast : y (Fin.last q) = O.val.transpose *ᵥ WithLp.ofLp (alg.sample q (hiddenPrecision κ O) s) :=
    (ha (2*q) le_rfl).trans last
  rw [← hlast]
  apply krylov_of_alternating_frames κ g E y hE₀
  · intro i
    have ht : 2*i.val ≤ 2*q := by omega
    have hh := hp.start_mem (idx (2*i.val)) (by
      simp only [Nat.zero_add,val _ ht,alternatingProgram,alternatingBack,Nat.mul_mod_right,decide_true])
    change (R (idx (2*i.val))).answer ∈ exposedSpace (R (idx (2*i.val))).priorDomain
      (R (idx (2*i.val))).priorRank ⊔ ℝ ∙ (R (evenIndex q i)).start.ofLp
    rwa [← heven i]
  · intro i
    let t := 2*i.val
    have ht : t < 2*q := by dsimp [t]; omega
    rw [(hnext t ht).2]
    have hh := hp.growth (idx t)
    simpa only [Nat.zero_add,val t ht.le,alternatingProgram,alternatingBack,t,
      Nat.mul_mod_right,decide_true,if_true,E,y,recd,Fin.val_castSucc] using hh
  · intro i
    let t := 2*i.val
    have ht : t+1 < 2*q := by dsimp [t]; omega
    have he := (hnext t (by omega)).1
    have hinput : prog.vector (t+1) (recd (t+1)).priorState = diagonalPrecision d κ *ᵥ y i.castSucc := by
      rw [he]
      simp [prog,alternatingProgram,alternatingVector,alternatingUpdate,alternatingBack,t,y]
    have hs : 2*i.val+2 = (t+1)+1 := rfl
    rw [hs,(hnext (t+1) ht).2,← hinput]
    have hh := hp.growth (idx (t+1))
    have hb : prog.back (t+1) = false := by simp [prog,alternatingProgram,alternatingBack,t]
    simpa only [Nat.zero_add,val _ ht.le,show (alternatingProgram alg κ q).back (t+1) = false from hb,
      Bool.false_eq_true,if_false] using hh

#print axioms actual_output_mem_of_walkPath

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
