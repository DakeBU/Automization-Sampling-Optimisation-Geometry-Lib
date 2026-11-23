import GC41Power
import GC41Reversal
import GC41TwoPoint
import Mathlib.LinearAlgebra.Matrix.Charpoly.Basic

/-!
# Two hard inputs with the same disclosed spectrum

Take the midpoint cosine grid in the original order and in reverse order. The
two precisions have identical eigenvalues with multiplicity. At mode one the
strict detection events are disjoint, while each target passes its own event
with probability at least 9/10. This gives a concrete two-input obstruction
for procedures seeing the spectrum before they make any queries.
-/

open MeasureTheory Matrix
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetEvent
open AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle (run)

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation

/-- The disclosed characteristic polynomial lists precisely the grid eigenvalues,
including multiplicities, for every hidden orientation. -/
theorem hiddenPrecision_charpoly {d : ℕ} (κ : ℝ) (O : Matrix.orthogonalGroup (Fin d) ℝ) :
    (hiddenPrecision κ O).charpoly = ∏ i : Fin d,
      (Polynomial.X - Polynomial.C ((κ+1)/2 + (κ-1)/2 * Real.cos (gridAngle d i))) := by
  have hO : O.val.transpose * O.val = 1 :=
    (Matrix.mem_orthogonalGroup_iff' (n := Fin d) (R := ℝ)).mp O.property
  rw [hiddenPrecision, Matrix.charpoly_mul_comm, ← Matrix.mul_assoc, hO, one_mul]
  exact Matrix.charpoly_diagonal _

/-- A visible spectrum and a seed fully determine the zero-query output.
The algorithm itself may be chosen as a function of the entire spectrum. -/
theorem outputLaw_zero_of_same_spectrum {d : ℕ} {Seed State : Type*}
    [MeasurableSpace Seed] [MeasurableSpace State] (ρ : Measure Seed)
    (alg : Polynomial ℝ → Algorithm d Seed State) {A B : Precision d}
    (hs : A.charpoly = B.charpoly) :
    (alg A.charpoly).outputLaw ρ 0 A = (alg B.charpoly).outputLaw ρ 0 B := by
  rw [hs]
  unfold Algorithm.outputLaw
  congr 1
  funext s
  unfold Algorithm.sample
  cases h : (alg B.charpoly).next ((alg B.charpoly).start s) <;> simp [run, h]

/-- For all sufficiently large dimensions, the two explicit rotated inputs
have identical spectra and target TV distance at least 4/5. Every zero-query
algorithm supplied with that spectrum has error at least 2/5 on one input. -/
theorem eventual_known_spectrum_zero_query_obstruction {δ : ℝ} (hδ : 0 < δ) (hδ' : δ < 1) :
    ∃ d₀ : ℕ, ∀ d ≥ d₀, ∀ κ : ℝ, 2 ≤ κ → κ ≤ (d : ℝ)^(1-δ) →
      let A := hiddenPrecision κ (1 : Matrix.orthogonalGroup (Fin d) ℝ)
      let B := hiddenPrecision κ (reversal d)
      A.charpoly = B.charpoly ∧ 4/5 ≤ eventTV (targetLaw A) (targetLaw B) ∧
      ∀ {Seed State : Type*} [MeasurableSpace Seed] [MeasurableSpace State]
        (ρ : Measure Seed) [IsProbabilityMeasure ρ] (alg : Polynomial ℝ → Algorithm d Seed State),
        2/5 ≤ max (eventTV ((alg A.charpoly).outputLaw ρ 0 A) (targetLaw A))
          (eventTV ((alg B.charpoly).outputLaw ρ 0 B) (targetLaw B)) := by
  obtain ⟨D, hD⟩ := eventual_rotated_target_power 1 zero_lt_one hδ hδ'
  refine ⟨max 2 D, ?_⟩
  intro d hd κ hκ hcap
  let A := hiddenPrecision κ (1 : Matrix.orthogonalGroup (Fin d) ℝ)
  let B := hiddenPrecision κ (reversal d)
  let τ := queryThreshold 1 d 0
  have hd2 := (le_max_left 2 D).trans hd
  have hl : 0 ≤ Real.log (d : ℝ) := Real.log_nonneg (by exact_mod_cast (show 1 ≤ d by omega))
  have hτ : 0 ≤ τ := by dsimp [τ, queryThreshold]; positivity
  have hq : (0 : ℝ) ≤ δ/256 * Real.sqrt κ * Real.log (d : ℝ) := by positivity
  have power := hD d ((le_max_right 2 D).trans hd) κ hκ hcap 0 (by simpa only [Nat.cast_zero] using hq)
  have h := two_point_event_separation (targetLaw A) (targetLaw B)
    (measurableSet_detectorEvent κ 1 τ A) (measurableSet_detectorEvent κ 1 τ B)
    (disjoint_reversed_detector_events hd2 hκ hτ) (power 1) (power (reversal d))
  have hs : A.charpoly = B.charpoly :=
    (hiddenPrecision_charpoly κ 1).trans (hiddenPrecision_charpoly κ (reversal d)).symm
  refine ⟨hs, h.1, ?_⟩
  intro Seed State _ _ ρ _ alg
  let μ := (alg A.charpoly).outputLaw ρ 0 A
  let : IsProbabilityMeasure μ := Measure.isProbabilityMeasure_map
    ((((alg A.charpoly).measurable_sample 0).comp (measurable_prodMk_right (y := A))).aemeasurable)
  have he := outputLaw_zero_of_same_spectrum ρ alg hs
  change 2/5 ≤ max (eventTV μ (targetLaw A)) (eventTV ((alg B.charpoly).outputLaw ρ 0 B) (targetLaw B))
  rw [← he]
  exact h.2 μ

#print axioms hiddenPrecision_charpoly
#print axioms eventual_known_spectrum_zero_query_obstruction

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
