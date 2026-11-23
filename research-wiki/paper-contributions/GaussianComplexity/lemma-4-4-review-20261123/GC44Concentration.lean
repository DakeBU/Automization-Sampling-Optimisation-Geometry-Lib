import GC44FiniteSymbol
import GC44Net

/-! Simultaneous operator-norm bounds for both families of projected Gaussian row matrices. -/
open MeasureTheory ProbabilityTheory Matrix
open scoped BigOperators Matrix.Norms.L2Operator
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetEvent
noncomputable section
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

/-- For both families of weights at every grid point, the norm bound holds on
one event of probability at least 199/200 in the source experiment. -/
theorem simultaneous_weighted_row_bounds {d q : ℕ} (hq : 2*q+1 < d)
    (w : Bool → Fin d → Fin d → ℝ)
    (hw : ∀ b i, (∀ j, |w b i j| ≤ 2*(2*(q : ℝ)+1)/(d : ℝ)) ∧
      ∑ j, (w b i j)^2 ≤ 2*(2*(q : ℝ)+1)/(d : ℝ)) :
    let μ := Measure.pi (fun _ : Fin (q+1) => stdGaussian (Space d))
    (199/200 : ℝ) ≤ μ.real {g : Starts d q | ∀ b i,
      ‖weightedRowMatrix g (w b i)‖ ≤ queryThreshold 2048 d q} := by
  let τ := queryThreshold 2048 d q
  have hd : 1 ≤ (d : ℝ) := by exact_mod_cast (show 1 ≤ d by omega)
  have hl := Real.log_nonneg hd
  have hτ : 0 ≤ τ/2 := by dsimp [τ,queryThreshold]; positivity
  apply (finite_symbol_tests hq (sphereNet (q+1)) (fun _ => norm_of_mem_sphereNet)
    (sphereNet_card_le _) w hw).trans
  refine measureReal_mono ?_ (measure_ne_top _ _)
  intro g hg b i
  have h := opNorm_le_of_sphereNet (Nat.succ_pos q) _ (weightedRowMatrix_hermitian g (w b i)) hτ (hg b i)
  change ‖weightedRowMatrix g (w b i)‖ ≤ τ
  linarith

#print axioms simultaneous_weighted_row_bounds

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
