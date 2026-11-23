import GC44GramUse
import Mathlib.Topology.Maps.Proper.Basic

/-! Measurability of membership in a varying finite-dimensional Krylov span. -/
noncomputable section
open MeasureTheory ProbabilityTheory Matrix
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

private instance matrixMeas (I J : Type*) : MeasurableSpace (Matrix I J ℝ) := borel _
private instance matrixBorel (I J : Type*) : BorelSpace (Matrix I J ℝ) := ⟨rfl⟩

theorem measurableSet_range_mulVec {I J : Type*} [Fintype I] [Fintype J] :
    MeasurableSet {p : Matrix I J ℝ × (I → ℝ) | p.2 ∈ Set.range (fun c => p.1 *ᵥ c)} := by
  classical
  let P := Matrix I J ℝ × (I → ℝ)
  let S (k : ℕ) : Set (J → ℝ) := Metric.closedBall 0 k
  let V (k : ℕ) : Set P := {p | ∃ c : S k, p.1 *ᵥ c.val = p.2}
  have hV (k : ℕ) : IsClosed (V k) := by
    let : CompactSpace (S k) := isCompact_iff_compactSpace.mp (isCompact_closedBall _ _)
    let W : Set (P × S k) := {x | x.1.1 *ᵥ x.2.val = x.1.2}
    have hW : IsClosed W := isClosed_eq ((continuous_fst.comp continuous_fst).matrix_mulVec
      (continuous_subtype_val.comp continuous_snd)) (continuous_snd.comp continuous_fst)
    have hE : V k = Prod.fst '' W := by
      ext p
      constructor
      · rintro ⟨c,hc⟩
        exact ⟨(p,c),hc,rfl⟩
      · rintro ⟨⟨p,c⟩,hc,rfl⟩
        exact ⟨c,hc⟩
    exact hE ▸ isClosedMap_fst_of_compactSpace _ hW
  have he : {p : P | p.2 ∈ Set.range (fun c => p.1 *ᵥ c)} = ⋃ k : ℕ, V k := by
    ext p
    simp only [Set.mem_ofPred_eq, Set.mem_iUnion, Set.mem_range]
    constructor
    · rintro ⟨c,hc⟩
      obtain ⟨k,hk⟩ := exists_nat_ge ‖c‖
      exact ⟨k,⟨c,by simpa only [S, Metric.mem_closedBall, dist_zero_right] using hk⟩,hc⟩
    · rintro ⟨k,c,hc⟩
      exact ⟨c.val,hc⟩
  rw [he]
  exact MeasurableSet.iUnion fun k => (hV k).measurableSet

theorem measurableSet_krylov_membership (d q : ℕ) (κ : ℝ) :
    MeasurableSet {p : Starts d q × (Fin d → ℝ) | p.2 ∈ krylov d q κ p.1} := by
  let B (g : Starts d q) : Matrix (Fin d) (Indices q) ℝ := fun i a =>
    ((diagonalPrecision d κ ^ a.2.val) *ᵥ (WithLp.ofLp (g a.1))) i
  have hB : Continuous B := by
    refine continuous_matrix (fun i a => ?_)
    exact (continuous_apply i).comp (continuous_const.matrix_mulVec
      ((PiLp.continuous_ofLp 2 (fun _ : Fin d => ℝ)).comp (continuous_apply a.1)))
  have hm : Measurable (fun p : Starts d q × (Fin d → ℝ) => (B p.1,p.2)) :=
    hB.measurable.prodMap measurable_id
  convert hm (measurableSet_range_mulVec (I := Fin d) (J := Indices q)) using 1
  ext p
  change p.2 ∈ Submodule.span ℝ (Set.range (B p.1).col) ↔ p.2 ∈ LinearMap.range (B p.1).mulVecLin
  rw [Matrix.range_mulVecLin]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
