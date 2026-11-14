import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceGramRealization
import AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment

/-! Private real Ex126 consumer. On the literal original good event and actual
centered-sum deviation event, derive actual Gram norm bounds. The real threshold
is an explicit deterministic generalization; no event probability is claimed. -/
noncomputable section
open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity
open scoped BigOperators Matrix Kronecker Matrix.Norms.L2Operator
set_option autoImplicit false
namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceGramRealization

private theorem actual_source_gram_deviation_bounds
    {d q : ℕ} (hq : 2 * q + 1 < d) :
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 - 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun b : Fin (q + 1) => ω b i)
  let Y : Fin d → Ω →
      Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ := fun i ω =>
    if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec (WithLp.ofLp (row i ω)) (WithLp.ofLp (row i ω)))
        (Matrix.vecMulVec (t i) (t i))
    else 0
  let mean : Fin d → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i => ∫ ω, Y i ω ∂μ
  let Z : Fin d → Ω → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => Y i ω - mean i
  let a : ℝ := (∫ x : E, Set.indicator {y : E | ‖y‖ ^ 2 ≤ L}
    (fun y : E => ‖y‖ ^ 2) x ∂stdGaussian E) / r
  let w : Fin d → ℝ := fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i)
  let B : Ω → Matrix (Fin d) (Fin (q + 1) × Fin (q + 1)) ℝ := fun ω i u =>
    (Real.sqrt (d : ℝ))⁻¹ * (row i ω) u.1 * t i u.2
  let G : Ω → Prop := fun ω => ∀ i : Fin d, ‖row i ω‖ ^ 2 ≤ L
  ∀ Δ : ℝ, ∀ ω : Ω, G ω →
    ((‖∑ i : Fin d, Z i ω‖ ≤ Δ) ∧
      (‖∑ i : Fin d, w i • Z i ω‖ ≤ Δ)) →
    ((‖(B ω).transpose * B ω -
        (1 : Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ)‖
        ≤ Δ + (1 - a)) ∧
      (‖(B ω).transpose * Matrix.diagonal w * B ω‖ ≤ Δ))
 := by
  classical
  dsimp only
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 - 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun b : Fin (q + 1) => ω b i)
  let Y : Fin d → Ω →
      Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ := fun i ω =>
    if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec (WithLp.ofLp (row i ω)) (WithLp.ofLp (row i ω)))
        (Matrix.vecMulVec (t i) (t i))
    else 0
  let mean : Fin d → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i => ∫ ω, Y i ω ∂μ
  let Z : Fin d → Ω → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => Y i ω - mean i
  let a : ℝ := (∫ x : E, Set.indicator {y : E | ‖y‖ ^ 2 ≤ L}
    (fun y : E => ‖y‖ ^ 2) x ∂stdGaussian E) / r
  let w : Fin d → ℝ := fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i)
  let B : Ω → Matrix (Fin d) (Fin (q + 1) × Fin (q + 1)) ℝ := fun ω i u =>
    (Real.sqrt (d : ℝ))⁻¹ * (row i ω) u.1 * t i u.2
  let G : Ω → Prop := fun ω => ∀ i : Fin d, ‖row i ω‖ ^ 2 ≤ L
  let N := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
  have hp := FixedSpectrumSourceGramRealization.actual_source_centered_gram_realizations
    (d := d) (q := q) hq
  change (∀ ω : Ω, G ω →
    ((∑ i : Fin d, Z i ω) = (B ω).transpose * B ω - a • (1 : N)) ∧
    ((∑ i : Fin d, w i • Z i ω) =
      (B ω).transpose * Matrix.diagonal w * B ω)) at hp
  have hr : 0 < r := by dsimp [r]; positivity
  have moment := AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian
    (E := E)
  have hgood : MeasurableSet {y : E | ‖y‖ ^ 2 ≤ L} :=
    measurableSet_le (by fun_prop) measurable_const
  have hret := moment.1.indicator hgood
  have hretle : (∫ x : E, {y : E | ‖y‖ ^ 2 ≤ L}.indicator
      (fun y => ‖y‖ ^ 2) x ∂stdGaussian E) ≤ r := by
    calc
      _ ≤ ∫ x : E, ‖x‖ ^ 2 ∂stdGaussian E := by
        apply integral_mono hret moment.1
        intro x
        by_cases hx : ‖x‖ ^ 2 ≤ L
        · simp [Set.indicator, hx]
        · simpa [Set.indicator, hx] using sq_nonneg ‖x‖
      _ = r := by simpa [E, r] using moment.2
  have ha1 : a ≤ 1 := (div_le_one hr).2 hretle
  have identity_norm : ‖(1 : N)‖ = 1 := norm_one
  have bias_norm : ‖(1 - a) • (1 : N)‖ = 1 - a := by
    rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg (sub_nonneg.mpr ha1),
      identity_norm, mul_one]
  have actual_bias_identity (ω : Ω) (hG : G ω) :
      (B ω).transpose * B ω - (1 : N) =
        (∑ i : Fin d, Z i ω) - (1 - a) • (1 : N) := by
    rw [(hp ω hG).1]
    have split_identity : a • (1 : N) + (1 - a) • (1 : N) = (1 : N) := by
      rw [← add_smul, show a + (1 - a) = (1 : ℝ) by ring, one_smul]
    calc
      _ = (B ω).transpose * B ω - (a • (1 : N) + (1 - a) • (1 : N)) := by
        rw [split_identity]
      _ = _ := by abel
  change ∀ Δ : ℝ, ∀ ω : Ω, G ω →
    ((‖∑ i : Fin d, Z i ω‖ ≤ Δ) ∧ (‖∑ i : Fin d, w i • Z i ω‖ ≤ Δ)) →
    ((‖(B ω).transpose * B ω - (1 : N)‖ ≤ Δ + (1 - a)) ∧
      (‖(B ω).transpose * Matrix.diagonal w * B ω‖ ≤ Δ))
  intro Δ ω hG hΔ
  constructor
  · calc
      ‖(B ω).transpose * B ω - (1 : N)‖ =
          ‖(∑ i : Fin d, Z i ω) - (1 - a) • (1 : N)‖ := by
        rw [actual_bias_identity ω hG]
      _ ≤ ‖∑ i : Fin d, Z i ω‖ + ‖(1 - a) • (1 : N)‖ := norm_sub_le _ _
      _ = ‖∑ i : Fin d, Z i ω‖ + (1 - a) := by rw [bias_norm]
      _ ≤ Δ + (1 - a) := add_le_add hΔ.1 (le_refl (1 - a))
  · rw [← (hp ω hG).2]
    exact hΔ.2

end AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceGramRealization
