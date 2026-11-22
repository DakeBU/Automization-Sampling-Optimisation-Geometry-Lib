import B4Transcript
import B4HistorySpace

/-!
# Lemma B.4 on the finite product of transcript records

The chronological list returned by the oracle has exactly one record per
time slot. Reading the first M entries is therefore lossless on this run,
including the absorbing padding records. A selector is measurable if it is
Borel on the ordinary product of records at each possible history length.
-/

open MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open scoped AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

variable {N k : ℕ}

/-- Read all time slots, preserving their chronological order. -/
noncomputable def transcriptVector (select : Trace k N → Option (Query k N)) (M : ℕ)
    (W : Fin k → O N) : Fin M → Record k N :=
  tupleAt none M (rawRun select M [] W)

/-- Restoring the vector as a list recovers the same complete transcript
on every draw, including the empty run. -/
theorem ofFn_transcriptVector (select : Trace k N → Option (Query k N)) (M : ℕ)
    (W : Fin k → O N) : List.ofFn (transcriptVector select M W) = rawRun select M [] W := by
  have recover (l : Trace k N) (m : ℕ) (len : l.length = m) :
      List.ofFn (tupleAt none m l) = l := by
    subst m
    exact tupleAt_length none l
  exact recover _ M (length_rawRun select M [] W)

/-- The joint law of all M = 2Tk records in the finite Cartesian product is
identical under either sign. Every queried record contains the block, vector,
sense and ambient answer. -/
theorem padded_transcript_vector_indistinguishability {T : ℕ} (hN : 2*T < N)
    (select : Trace k N → Option (Query k N))
    (hs : ∀ m, Measurable (fun v : Fin m → Record k N => select (List.ofFn v)))
    (cap : ∀ b : ℝ, b = -1 ∨ b = 1 →
      ∀ᵐ W ∂(Measure.pi fun _ : Fin k => componentHaar N b),
        ∀ j, blockCount j (rawRun select (2*T*k) [] W) ≤ 2*T) :
    (Measure.pi fun _ : Fin k => componentHaar N 1).map (transcriptVector select (2*T*k)) =
      (Measure.pi fun _ : Fin k => componentHaar N (-1)).map (transcriptVector select (2*T*k)) := by
  have hm := (measurable_history_iff_ofFn none select).mpr hs
  have hr := measurable_rawRun_fixed select hm (2*T*k) []
  change (Measure.pi fun _ : Fin k => componentHaar N 1).map
      (tupleAt (none : Record k N) (2*T*k) ∘ rawRun select (2*T*k) []) =
    (Measure.pi fun _ : Fin k => componentHaar N (-1)).map
      (tupleAt (none : Record k N) (2*T*k) ∘ rawRun select (2*T*k) [])
  have h := congrArg (Measure.map (tupleAt (none : Record k N) (2*T*k)))
    (padded_transcript_indistinguishability hN select hm cap)
  simpa only [Measure.map_map (measurable_tupleAt none (2*T*k)) hr] using h

#print axioms padded_transcript_vector_indistinguishability

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
