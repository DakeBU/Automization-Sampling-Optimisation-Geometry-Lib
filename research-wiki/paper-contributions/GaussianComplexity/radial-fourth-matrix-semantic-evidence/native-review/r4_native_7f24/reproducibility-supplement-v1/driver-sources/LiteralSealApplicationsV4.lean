import Lean
import Tests.GaussianComplexityFixedSpectrumRadialFourthMoment
noncomputable section
open MeasureTheory ProbabilityTheory WithLp
open scoped Matrix.Norms.L2Operator
set_option autoImplicit false
open Lean
elab "independentPrivateRoot" : term => do
  let foundRoots := (← getEnv).constants.toList.filter (fun (n, _) => n.toString == "_private.Tests.GaussianComplexityFixedSpectrumRadialFourthMoment.0.AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumRadialFourthMoment.actual_truncated_summand_second_moment_bound")
  if foundRoots.length != 1 then throwError "private root lookup failed"
  pure (mkConst foundRoots.head!.1)
theorem IndependentLiteralProducer {d q : ℕ} (hq : 2 * q + 1 < d) :
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let R : E → ℝ := fun x => ‖x‖ ^ 2
  let G : E → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    fun x => Matrix.vecMulVec (WithLp.ofLp x) (WithLp.ofLp x)
  let weighted : E → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    fun x => R x • G x
  Integrable weighted μ ∧
    (∫ x, weighted x ∂μ) = (r + 2) • (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ)
 := by
  exact AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment.actual_radial_fourth_moment_matrix hq
theorem IndependentLiteralPrivateConsumer {d q : ℕ} (hq : 2 * q + 1 < d) (i : Fin d) :
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let R : E → ℝ := fun x => ‖x‖ ^ 2
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun j => ((j.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun j k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ j)
  let G : E → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    fun x => Matrix.vecMulVec (WithLp.ofLp x) (WithLp.ofLp x)
  let feature : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    Matrix.vecMulVec (t i) (t i)
  let Y : E → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    Set.indicator {y : E | R y ≤ L}
      (fun x => (d : ℝ)⁻¹ • Matrix.kronecker (G x) feature)
  let squared := fun x => Y x * Y x
  let upper : Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    (((r + 2) * (∑ k : Fin (q + 1), (t i k) ^ 2)) / (d : ℝ) ^ 2) •
      Matrix.kronecker (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ) feature
  Integrable squared μ ∧ Matrix.PosSemidef (upper - (∫ x, squared x ∂μ))
 := by
  exact independentPrivateRoot (d := d) (q := q) hq i
#print axioms IndependentLiteralProducer
#print axioms IndependentLiteralPrivateConsumer
