import AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureDensities
import AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockSeparation
import AutoSamplingTheory.TechnicalLemmas.InformationTheory.DensityAffinity

/-!
# The actual single-block affinity bound (Eq25)

Zhou--Suzuki, arXiv:2610.20492v1, Appendix B.2.3, Ex68--69 and Eq25.
The actual determinant-conditioned Gaussian bind laws and their actual density
representatives instantiate the single shared normalized-density comparison.
B.7 and the scalar log inequality then yield both exact Eq25 inequalities.
Only n>=3 and kappa>=4 are public assumptions; analytic ingredients are internal.
Actual block product laws, tensorization, amplification, oracle/precision/cost
adapters and both main lower bounds remain separate.
-/

open Matrix MeasureTheory
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.TechnicalLemmas.InformationTheory.DensityAffinity

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockAffinity
set_option autoImplicit false

theorem single_block_affinity_bound {n : ℕ} (hn : 3 ≤ n) {κ : ℝ} (hκ : 4 ≤ κ) :
    let μ := orthogonalHaar n
    let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
    let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
    let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
      fun O => ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ O)⁻¹
    let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision κ O).det /
        (2 * Real.pi) ^ ((n : ℝ) / 2) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ
          (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
    let qpos : EuclideanSpace ℝ (Fin n) → ℝ := fun x => ∫ O, p O x ∂νpos
    let qneg : EuclideanSpace ℝ (Fin n) → ℝ := fun x => ∫ O, p O x ∂νneg
    let Ppos := νpos.bind γ
    let Pneg := νneg.bind γ
    let δ : ℝ := sSup {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin n)),
      MeasurableSet B ∧ z = |Ppos.real B - Pneg.real B|}
    let a : ℝ := ∫ x, Real.sqrt (qpos x * qneg x)
    Integrable (fun x => Real.sqrt (qpos x * qneg x)) volume ∧
    0 ≤ a ∧ a ≤ 1 ∧ δ ≤ Real.sqrt (1 - a ^ 2) ∧
    a ≤ Real.sqrt (1 - (1 / 4 : ℝ) * Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ)) ∧
    Real.sqrt (1 - (1 / 4 : ℝ) * Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ)) ≤
      Real.exp (-(1 / 8 : ℝ) * Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ)) := by
  classical
  dsimp only
  let μ := orthogonalHaar n
  let νpos := (2 : ℝ≥0∞) • μ.restrict
    {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
  let νneg := (2 : ℝ≥0∞) • μ.restrict
    {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
  let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
    fun O => ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
      (singleBlockPrecision κ O)⁻¹
  let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
    fun O x => Real.sqrt (singleBlockPrecision κ O).det /
      (2 * Real.pi) ^ ((n : ℝ) / 2) *
      Real.exp (-((WithLp.ofLp x) ⬝ᵥ
        (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
  let qpos : EuclideanSpace ℝ (Fin n) → ℝ := fun x => ∫ O, p O x ∂νpos
  let qneg : EuclideanSpace ℝ (Fin n) → ℝ := fun x => ∫ O, p O x ∂νneg
  let Ppos := νpos.bind γ
  let Pneg := νneg.bind γ
  let δ : ℝ := sSup {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin n)),
    MeasurableSet B ∧ z = |Ppos.real B - Pneg.real B|}
  let a : ℝ := ∫ x, Real.sqrt (qpos x * qneg x)
  have hd := MixtureDensities.actual_mixture_densities hn hκ
  dsimp only at hd
  have hc := normalized_density_tv_affinity (volume : Measure (EuclideanSpace ℝ (Fin n)))
    (fun x => (hd.1 x).1) (fun x => (hd.1 x).2)
    hd.2.1 hd.2.2.1 hd.2.2.2.1 hd.2.2.2.2.1
    hd.2.2.2.2.2.1 hd.2.2.2.2.2.2.1
  dsimp only at hc
  have hreal (q : EuclideanSpace ℝ (Fin n) → ℝ)
      (hq0 : ∀ x, 0 ≤ q x) (hqm : Measurable q)
      (B : Set (EuclideanSpace ℝ (Fin n))) (hB : MeasurableSet B) :
      (volume.withDensity (fun x => ENNReal.ofReal (q x))).real B =
        ∫ x in B, q x := by
    rw [measureReal_def, withDensity_apply _ hB]
    exact (integral_eq_lintegral_of_nonneg_ae
      (Filter.Eventually.of_forall hq0) hqm.aestronglyMeasurable).symm
  have hpos (B : Set (EuclideanSpace ℝ (Fin n))) (hB : MeasurableSet B) :
      Ppos.real B = ∫ x in B, qpos x := by
    have he : Ppos = volume.withDensity (fun x => ENNReal.ofReal (qpos x)) :=
      hd.2.2.2.2.2.2.2.1
    rw [he]
    exact hreal qpos (fun x => (hd.1 x).1) hd.2.1 B hB
  have hneg (B : Set (EuclideanSpace ℝ (Fin n))) (hB : MeasurableSet B) :
      Pneg.real B = ∫ x in B, qneg x := by
    have he : Pneg = volume.withDensity (fun x => ENNReal.ofReal (qneg x)) :=
      hd.2.2.2.2.2.2.2.2
    rw [he]
    exact hreal qneg (fun x => (hd.1 x).2) hd.2.2.1 B hB
  have hset : {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin n)), MeasurableSet B ∧
        z = |Ppos.real B - Pneg.real B|} =
      {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin n)), MeasurableSet B ∧
        z = |(∫ x in B, qpos x) - (∫ x in B, qneg x)|} := by
    ext z
    constructor <;> rintro ⟨B, hB, hz⟩
    · exact ⟨B, hB, (by rw [← hpos B hB, ← hneg B hB]; exact hz)⟩
    · exact ⟨B, hB, (by rw [hpos B hB, hneg B hB]; exact hz)⟩
  have ha0 : 0 ≤ a := hc.2.1
  have ha1 : a ≤ 1 := hc.2.2.1
  have htv : δ ≤ Real.sqrt (1 - a ^ 2) := by
    dsimp only [δ]
    rw [hset]
    exact hc.2.2.2.2.2
  have hb7 := SingleBlockSeparation.single_block_separation hn hκ
  dsimp only at hb7
  have hlow : (1 / 2 : ℝ) * Real.exp (-(5 * (n : ℝ)) / Real.sqrt κ) ≤ δ :=
    hb7.1.trans hb7.2
  have hrad : 0 ≤ 1 - a ^ 2 := by nlinarith
  have hsquare : ((1 / 2 : ℝ) * Real.exp (-(5 * (n : ℝ)) / Real.sqrt κ)) ^ 2 ≤
      1 - a ^ 2 := by
    have he := hlow.trans htv
    have hpos : 0 ≤ (1 / 2 : ℝ) * Real.exp (-(5 * (n : ℝ)) / Real.sqrt κ) := by
      positivity
    have hs := Real.sq_sqrt hrad
    nlinarith [Real.sqrt_nonneg (1 - a ^ 2)]
  have hexp : Real.exp (-(5 * (n : ℝ)) / Real.sqrt κ) ^ 2 =
      Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ) := by
    rw [pow_two, ← Real.exp_add]
    congr 1
    ring
  have hfirst : a ≤ Real.sqrt
      (1 - (1 / 4 : ℝ) * Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ)) := by
    apply Real.le_sqrt_of_sq_le
    rw [mul_pow, hexp] at hsquare
    nlinarith
  let t : ℝ := (1 / 4 : ℝ) * Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ)
  have hn0 : (0 : ℝ) < n := by exact_mod_cast (lt_of_lt_of_le (by decide : 0 < 3) hn)
  have hs0 : 0 < Real.sqrt κ := Real.sqrt_pos.mpr (by linarith)
  have ht1 : t < 1 := by
    have he : Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ) ≤ 1 :=
      Real.exp_le_one_iff.mpr
        (div_nonpos_of_nonpos_of_nonneg (by linarith) hs0.le)
    dsimp only [t]
    linarith
  have hlog : Real.log (1 - t) ≤ -t := by
    have he := Real.log_le_sub_one_of_pos (sub_pos.mpr ht1)
    linarith
  have hsqrt : Real.sqrt (1 - t) = Real.exp (Real.log (1 - t) / 2) := by
    rw [Real.sqrt_eq_rpow, Real.rpow_def_of_pos (sub_pos.mpr ht1)]
    congr 1
    ring
  have hlast : Real.sqrt
      (1 - (1 / 4 : ℝ) * Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ)) ≤
      Real.exp (-(1 / 8 : ℝ) * Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ)) := by
    calc
      _ = Real.exp (Real.log (1 - t) / 2) := hsqrt
      _ ≤ Real.exp (-t / 2) := Real.exp_le_exp.mpr (by linarith)
      _ = _ := by congr 1; dsimp only [t]; ring
  exact ⟨hc.1, ha0, ha1, htv, hfirst, hlast⟩

end AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockAffinity
