import GC43Membership
import GC43CoupleLaw

/-! Joint-law version of the Krylov representation. The extension keeps
the original orientation and the actual point as one random variable. -/
noncomputable section
open MeasureTheory ProbabilityTheory Matrix
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HiddenEigenbasis
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

abbrev Orientation (d : ℕ) := Matrix.orthogonalGroup (Fin d) ℝ
abbrev Pair (d : ℕ) := Orientation d × Space d
abbrev Extension (d q : ℕ) := Pair d × Starts d q

def inKrylov {d q : ℕ} (κ : ℝ) (p : Extension d q) : Prop :=
  p.1.1.val.transpose *ᵥ WithLp.ofLp p.1.2 ∈ krylov d q κ p.2

theorem measurableSet_inKrylov (d q : ℕ) (κ : ℝ) :
    MeasurableSet {p : Extension d q | inKrylov κ p} := by
  have hu : Continuous (fun p : Pair d => p.1.val.transpose *ᵥ WithLp.ofLp p.2) :=
    (continuous_subtype_val.comp continuous_fst).matrix_transpose.matrix_mulVec
      ((PiLp.continuous_ofLp 2 _).comp continuous_snd)
  exact (measurable_snd.prodMk (hu.measurable.comp measurable_fst))
    (measurableSet_krylov_membership d q κ)

def HasKrylovRepresentation {d q : ℕ} (κ : ℝ) (law : Measure (Pair d)) : Prop :=
  ∃ M : Measure (Extension d q), IsProbabilityMeasure M ∧
    MeasurePreserving Prod.fst M law ∧ MeasurePreserving Prod.snd M (gaussianStarts d q) ∧
    ∀ᵐ p ∂M, inKrylov κ p

variable {d q : ℕ} {Seed State Noise : Type*} [MeasurableSpace Seed]
  [MeasurableSpace State] [MeasurableSpace Noise]

theorem representation_of_fixed_seeds (κ : ℝ)
    (ρ : Measure Seed) [IsProbabilityMeasure ρ] (alg : Algorithm d Seed State)
    (ν : Measure Noise) [IsProbabilityMeasure ν]
    (g : Seed × Orientation d × Noise → Starts d q) (hg : Measurable g)
    (hlaw : ∀ s, ((orthogonalHaar d).prod ν).map (fun x => g (s,x)) = gaussianStarts d q)
    (hmem : ∀ s, ∀ᵐ x ∂(orthogonalHaar d).prod ν,
      inKrylov κ (fixedPair κ q alg s x.1, g (s,x))) :
    HasKrylovRepresentation (q := q) κ (experimentLaw κ q ρ alg) := by
  let U := orthogonalHaar d
  let : IsProbabilityMeasure U := (orthogonalHaar_spec d).1
  let μ := ρ.prod (U.prod ν)
  let F (z : Seed × Orientation d × Noise) : Pair d := experimentPair κ q alg (z.1,z.2.1)
  have hproj : MeasurePreserving (fun z : Seed × Orientation d × Noise => (z.1,z.2.1))
      μ (ρ.prod U) := (MeasurePreserving.id ρ).prod (measurePreserving_fst (μ := U) (ν := ν))
  have hpair : MeasurePreserving F μ (experimentLaw κ q ρ alg) :=
    (⟨measurable_experimentPair κ q alg, rfl⟩ :
      MeasurePreserving (experimentPair κ q alg) (ρ.prod U) _).comp hproj
  have hsg : MeasurePreserving (fun z : Seed × Orientation d × Noise => (z.1,g z))
      μ (ρ.prod (gaussianStarts d q)) :=
    (MeasurePreserving.id ρ).skew_product (g := fun s x => g (s,x)) hg (ae_of_all _ hlaw)
  let : IsProbabilityMeasure (gaussianStarts d q) := by unfold gaussianStarts; infer_instance
  have hstarts : MeasurePreserving g μ (gaussianStarts d q) :=
    (measurePreserving_snd (μ := ρ) (ν := gaussianStarts d q)).comp hsg
  let J (z : Seed × Orientation d × Noise) : Extension d q := (F z,g z)
  have hJ : Measurable J := hpair.measurable.prodMk hg
  have hI := measurableSet_inKrylov d q κ
  have hp : IsProbabilityMeasure μ := by dsimp [μ]; infer_instance
  refine ⟨μ.map J, Measure.isProbabilityMeasure_map hJ.aemeasurable, ⟨measurable_fst, ?_⟩,
    ⟨measurable_snd, ?_⟩, ?_⟩
  · rw [Measure.map_map measurable_fst hJ]
    exact hpair.map_eq
  · rw [Measure.map_map measurable_snd hJ]
    exact hstarts.map_eq
  · exact (ae_map_iff hJ.aemeasurable hI).mpr ((Measure.ae_prod_iff_ae_ae (hJ hI)).mpr (ae_of_all _ hmem))

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
