import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Topology.Algebra.Star.Unitary
import Mathlib.Topology.Instances.Matrix
import Mathlib.MeasureTheory.Constructions.BorelSpace.Real
import Mathlib.MeasureTheory.Measure.Haar.Unique
import Mathlib.MeasureTheory.Group.Integral

/-!
# Canonical Haar probability on the full real orthogonal group

Shared background for the two different experiments in Zhou--Suzuki,
arXiv:2610.20492v1: Section 2 / Appendix B.2.1 and Section 4.1.
Only the full Haar probability is common. Determinant conditioning, adaptive
posteriors, independence from an algorithm's seed and Krylov representations
are separate obligations. The construction includes dimension zero, without
asserting two determinant components in that dimension.
-/

open Matrix MeasureTheory Set TopologicalSpace

namespace AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar

private instance orthogonal_measurableSpace (n : ℕ) :
    MeasurableSpace (Matrix.orthogonalGroup (Fin n) ℝ) := borel _

private instance orthogonal_borelSpace (n : ℕ) :
    BorelSpace (Matrix.orthogonalGroup (Fin n) ℝ) := ⟨rfl⟩

private instance orthogonal_secondCountable (n : ℕ) :
    SecondCountableTopology (Matrix.orthogonalGroup (Fin n) ℝ) := by
  let : SecondCountableTopology (Matrix (Fin n) (Fin n) ℝ) :=
    inferInstanceAs (SecondCountableTopology (Fin n → Fin n → ℝ))
  exact secondCountableTopology_induced (Matrix.orthogonalGroup (Fin n) ℝ)
    (Matrix (Fin n) (Fin n) ℝ) Subtype.val

private instance orthogonal_compactSpace (n : ℕ) :
    CompactSpace (Matrix.orthogonalGroup (Fin n) ℝ) := by
  apply isCompact_iff_compactSpace.mp
  apply (isCompact_Icc : IsCompact (Icc (-1 : ℝ) 1)).matrix.of_isClosed_subset
    (isClosed_unitary : IsClosed
      (Matrix.orthogonalGroup (Fin n) ℝ : Set (Matrix (Fin n) (Fin n) ℝ)))
  intro A hA
  change ∀ i j, A i j ∈ Icc (-1 : ℝ) 1
  intro i j
  exact abs_le.mp (by simpa only [Real.norm_eq_abs] using
    entry_norm_bound_of_unitary hA i j)

/-- Real well-definedness: there exists exactly one Borel Haar probability law. -/
theorem existsUnique_orthogonalHaar (n : ℕ) :
    ∃! μ : Measure (Matrix.orthogonalGroup (Fin n) ℝ),
      IsProbabilityMeasure μ ∧ μ.IsHaarMeasure := by
  let μ : Measure (Matrix.orthogonalGroup (Fin n) ℝ) :=
    Measure.haarMeasure (⊤ : PositiveCompacts (Matrix.orthogonalGroup (Fin n) ℝ))
  have hprob : IsProbabilityMeasure μ := ⟨by
    simpa only [μ, PositiveCompacts.coe_top] using
      (Measure.haarMeasure_self (K₀ :=
        (⊤ : PositiveCompacts (Matrix.orthogonalGroup (Fin n) ℝ))))⟩
  have hhaar : μ.IsHaarMeasure := by dsimp only [μ]; infer_instance
  refine ⟨μ, ⟨hprob, hhaar⟩, ?_⟩
  intro ν hν
  let := hprob
  let := hhaar
  let := hν.1
  let := hν.2
  exact Measure.isHaarMeasure_eq_of_isProbabilityMeasure ν μ

/-- The actual Haar constructor normalized on the entire compact orthogonal group.
The preceding existence/uniqueness proof was independently audited before this definition. -/
noncomputable def orthogonalHaar (n : ℕ) :
    Measure (Matrix.orthogonalGroup (Fin n) ℝ) :=
  Measure.haarMeasure (⊤ : PositiveCompacts (Matrix.orthogonalGroup (Fin n) ℝ))

/-- Characterization and uniqueness of the constructed full Haar probability. -/
theorem orthogonalHaar_spec (n : ℕ) :
    IsProbabilityMeasure (orthogonalHaar n) ∧ (orthogonalHaar n).IsHaarMeasure ∧
      ∀ μ : Measure (Matrix.orthogonalGroup (Fin n) ℝ),
        IsProbabilityMeasure μ → μ.IsHaarMeasure → μ = orthogonalHaar n := by
  have hprob : IsProbabilityMeasure (orthogonalHaar n) := ⟨by
    simpa only [orthogonalHaar, PositiveCompacts.coe_top] using
      (Measure.haarMeasure_self (K₀ :=
        (⊤ : PositiveCompacts (Matrix.orthogonalGroup (Fin n) ℝ))))⟩
  have hhaar : (orthogonalHaar n).IsHaarMeasure := by
    dsimp only [orthogonalHaar]
    infer_instance
  refine ⟨hprob, hhaar, ?_⟩
  intro μ hp hh
  exact (existsUnique_orthogonalHaar n).unique ⟨hp, hh⟩ ⟨hprob, hhaar⟩

/-- The source's full Haar draw has the same law after every fixed left rotation/reflection. -/
theorem orthogonalHaar_map_mul_left (n : ℕ)
    (Q : Matrix.orthogonalGroup (Fin n) ℝ) :
    (orthogonalHaar n).map (fun O => Q * O) = orthogonalHaar n := by
  let := (orthogonalHaar_spec n).2.1
  exact map_mul_left_eq_self (orthogonalHaar n) Q

end AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
