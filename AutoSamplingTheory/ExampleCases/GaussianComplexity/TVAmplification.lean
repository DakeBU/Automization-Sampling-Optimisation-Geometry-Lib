import AutoSamplingTheory.ExampleCases.GaussianComplexity.AffinityTensorization
import AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockAffinity
import Mathlib.MeasureTheory.Measure.Decomposition.IntegralRNDeriv
open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal BigOperators
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.TVAmplification
set_option autoImplicit false
/-!
# Actual Gaussian-mixture TV amplification

Zhou--Suzuki, arXiv:2610.20492v1, Appendix B.2.3 Ex72 (final inequality).
The laws below are the actual determinant-component matrix-prior Gaussian
binds, and TV is the measurable-event supremum. Their probability and
absolute-continuity certificates identify event masses with genuine L1
RN-density integrals. The shared normalized-density comparison, actual Ex71
tensorization and actual Eq25 single-block estimate imply the stated bound.
No supplied density, integrability, probability or scalar-affinity premise
is added. The canonical producers include the zero-residual convention.
The oracle/query lower bounds remain separate.
-/
theorem actual_averaged_tv_lower_bound {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ) :
    letI : MeasurableSpace (Matrix (Fin d) (Fin d) ℝ) := borel _
    let μ := orthogonalHaar n
    let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
    let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
    let Dpos := (Measure.pi (fun _ : Fin (d / n) => νpos)).map (blockPrecision κ)
    let Dneg := (Measure.pi (fun _ : Fin (d / n) => νneg)).map (blockPrecision κ)
    let γ : Matrix (Fin d) (Fin d) ℝ → Measure (EuclideanSpace ℝ (Fin d)) :=
      fun A => multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹
    let Mpos := Dpos.bind γ
    let Mneg := Dneg.bind γ
    let δ : ℝ := sSup {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin d)),
      MeasurableSet B ∧ z = |Mpos.real B - Mneg.real B|}
    1 - Real.exp (-(((d / n : ℕ) : ℝ) / 8) *
      Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ)) ≤ δ := by
  classical
  dsimp only
  let : MeasurableSpace (Matrix (Fin d) (Fin d) ℝ) := borel _
  let μ := orthogonalHaar n
  let νpos := (2 : ℝ≥0∞) • μ.restrict
    {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
  let νneg := (2 : ℝ≥0∞) • μ.restrict
    {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
  let Dpos := (Measure.pi (fun _ : Fin (d / n) => νpos)).map (blockPrecision κ)
  let Dneg := (Measure.pi (fun _ : Fin (d / n) => νneg)).map (blockPrecision κ)
  let γ : Matrix (Fin d) (Fin d) ℝ → Measure (EuclideanSpace ℝ (Fin d)) :=
    fun A => multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹
  let Mpos := Dpos.bind γ
  let Mneg := Dneg.bind γ
  let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
    fun O x => Real.sqrt (singleBlockPrecision κ O).det /
      (2 * Real.pi) ^ ((n : ℝ) / 2) *
      Real.exp (-((WithLp.ofLp x) ⬝ᵥ
        (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
  let qpos : EuclideanSpace ℝ (Fin n) → ℝ := fun x => ∫ O, p O x ∂νpos
  let qneg : EuclideanSpace ℝ (Fin n) → ℝ := fun x => ∫ O, p O x ∂νneg
  let a : ℝ := ∫ x, Real.sqrt (qpos x * qneg x)
  let F : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    Real.sqrt (((Mpos.rnDeriv volume) x).toReal * ((Mneg.rnDeriv volume) x).toReal)

  let δ : ℝ := sSup {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin d)),
    MeasurableSet B ∧ z = |Mpos.real B - Mneg.real B|}
  let f : EuclideanSpace ℝ (Fin d) → ℝ := fun x => (Mpos.rnDeriv volume x).toReal
  let g : EuclideanSpace ℝ (Fin d) → ℝ := fun x => (Mneg.rnDeriv volume x).toReal
  -- Actual law probability is a canonical Ex6 output, not a new premise.
  have hp := AveragedBlockLaw.actual_averaged_block_product hn hnd hκ (b := 1) (Or.inl rfl)
  have hm := AveragedBlockLaw.actual_averaged_block_product hn hnd hκ (b := -1) (Or.inr rfl)
  let : IsProbabilityMeasure Mpos := hp.2.2.2.1
  let : IsProbabilityMeasure Mneg := hm.2.2.2.1
  have ht := AffinityTensorization.actual_affinity_tensorization hn hnd hκ
  have hb := SingleBlockAffinity.single_block_affinity_bound hn hκ
  dsimp only at ht hb
  -- RN integration over these actual finite laws has no infinity fallback.
  have hf0 (x) : 0 ≤ f x := ENNReal.toReal_nonneg
  have hg0 (x) : 0 ≤ g x := ENNReal.toReal_nonneg
  have hfm : Measurable f := (Measure.measurable_rnDeriv Mpos volume).ennreal_toReal
  have hgm : Measurable g := (Measure.measurable_rnDeriv Mneg volume).ennreal_toReal
  have hfi : Integrable f volume := Measure.integrable_toReal_rnDeriv
  have hgi : Integrable g volume := Measure.integrable_toReal_rnDeriv
  have hf1 : (∫ x, f x) = 1 := by
    calc
      _ = Mpos.real Set.univ := Measure.integral_toReal_rnDeriv ht.1
      _ = 1 := by simp [measureReal_def]
  have hg1 : (∫ x, g x) = 1 := by
    calc
      _ = Mneg.real Set.univ := Measure.integral_toReal_rnDeriv ht.2.1
      _ = 1 := by simp [measureReal_def]
  have hc := AutoSamplingTheory.TechnicalLemmas.InformationTheory.DensityAffinity.normalized_density_tv_affinity
    volume hf0 hg0 hfm hgm hfi hgi hf1 hg1
  dsimp only at hc
  -- Identify exactly the event supremum used in the source definition of TV.
  have hset : {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin d)), MeasurableSet B ∧
      z = |(∫ x in B, f x) - (∫ x in B, g x)|} =
      {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin d)), MeasurableSet B ∧
      z = |Mpos.real B - Mneg.real B|} := by
    ext z
    constructor <;> rintro ⟨B, hB, hz⟩
    · exact ⟨B, hB, (by rw [Measure.setIntegral_toReal_rnDeriv ht.1,
        Measure.setIntegral_toReal_rnDeriv ht.2.1] at hz; exact hz)⟩
    · exact ⟨B, hB, (by rw [Measure.setIntegral_toReal_rnDeriv ht.1,
        Measure.setIntegral_toReal_rnDeriv ht.2.1]; exact hz)⟩
  have htv : 1 - (∫ x, F x) ≤ δ := by
    have h := hc.2.2.2.2.1
    rw [hset] at h
    exact h
  -- Eq25 controls the true block affinity; Ex71 lifts it to the actual laws.
  have ha := hb.2.2.2.2.1.trans hb.2.2.2.2.2
  have hpow : a ^ (d / n) ≤ Real.exp
      (-(((d / n : ℕ) : ℝ) / 8) * Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ)) := by
    calc
      _ ≤ (Real.exp (-(1 / 8 : ℝ) *
          Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ))) ^ (d / n) :=
        pow_le_pow_left₀ hb.2.1 ha (d / n)
      _ = _ := by
        rw [← Real.exp_nat_mul]
        congr 1
        ring
  rw [ht.2.2.2] at htv
  exact (sub_le_sub_left hpow 1).trans htv
end AutoSamplingTheory.ExampleCases.GaussianComplexity.TVAmplification
