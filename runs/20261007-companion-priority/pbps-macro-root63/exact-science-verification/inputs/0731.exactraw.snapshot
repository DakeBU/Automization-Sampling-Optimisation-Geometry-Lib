import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ApproximateProximalExecution
import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.Probability.Kernel.Composition.Prod
import Mathlib.MeasureTheory.Constructions.Pi

/-!
# The implemented two-layer Picard phase

Chen--Chewi--Lu--Zhang, arXiv:2609.06906v1, Algorithm 3.1 steps 1--4,
with the gradient-only proximal implementation of Appendix D.1/D.2.
The kernel below uses both independent Gaussian arrays and both half-refreshes.
Every proximal evaluation is the actual finite residual-stopped program.

Finite deterministic nodes and quadrature weights are inputs of this bounded
interface. Their Chebyshev--Lobatto construction, repeated-history estimates,
sampling error, invariant law, and expected run cost remain separate.
-/

noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped BigOperators NNReal

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ImplementedPhaseKernel

variable {E ι : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
  [Fintype ι]

/-- The full two-layer phase is a measurable Markov kernel, with its law given
by the explicit independent Gaussian pushforward and every proximal draw bound
to the actual stopped interpreter. No quadrature or convergence premise is
assumed to manufacture a kernel. -/
theorem implemented_phase_kernel {V : E → ℝ} {κ : ℝ≥0}
    (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (κ : ℝ)⁻¹ * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖ ^ 2)
    {eta c eps : ℝ} (heta : 0 < eta) (hec : eta ≤ c) (hc : c < 1) (heps : 0 < eps)
    (h : ℝ) (hh : 0 ≤ h) (t : ι → ℝ) (omega : ι → ι → ℝ)
    (positionWeight momentumWeight : ι → ℝ) :
    ∃ p q : E → E, ∃ N : E → ℕ,
      Measurable p ∧ Measurable q ∧ Measurable N ∧
      (∀ y, p y + eta • gradient V (p y) = y ∧ ‖q y - p y‖ ≤ eps ∧
        ApproximateProximalExecution.proximalQuery (gradient V) eta eps y (N y + 1) y =
          some (q y, N y + 1)) ∧
      let a := Real.exp (-h / 2)
      let sigma := Real.sqrt (1 - Real.exp (-h))
      let γ := ((stdGaussian E).prod (stdGaussian E)).prod
        ((Measure.pi (fun _ : ι => stdGaussian E)).prod
          (Measure.pi (fun _ : ι => stdGaussian E)))
      let Φ := fun w : (E × E) × ((E × E) × ((ι → E) × (ι → E))) =>
        let P0 := a • w.1.2 + sigma • w.2.1.1
        let Y0 := fun i => w.1.1 + t i • P0
        let Z0 := fun j => gradient V (q (Y0 j) + Real.sqrt eta • w.2.2.1 j)
        let Y1 := fun i => Y0 i - ∑ j, omega i j • Z0 j
        let Z1 := fun j => gradient V (q (Y1 j) + Real.sqrt eta • w.2.2.2 j)
        (w.1.1 + h • P0 - ∑ j, positionWeight j • Z1 j,
          a • (P0 - ∑ j, momentumWeight j • Z1 j) + sigma • w.2.1.2)
      0 ≤ 1 - Real.exp (-h) ∧
      Measurable Φ ∧ ∃ K : Kernel (E × E) (E × E), IsMarkovKernel K ∧
        ∀ s, K s = γ.map (fun z => Φ (s, z)) := by
  classical
  obtain ⟨p, N, hp, hN, hq, hall⟩ :=
    ApproximateProximalExecution.approximate_proximal_execution
      hκ hV hH heta hec hc heps
  let q := fun y => (fun x : E => y - eta • gradient V x)^[N y] y
  have hqm : Measurable q := hq
  refine ⟨p, q, N, hp, hqm, hN, fun y =>
    ⟨(hall y).1, (hall y).2.2.2.2.1, (hall y).2.2.2.2.2.2⟩, ?_⟩
  dsimp only
  have hg : Measurable (gradient V) := by
    unfold gradient
    exact ((InnerProductSpace.toDual ℝ E).symm.continuous.comp
      (hV.continuous_fderiv (by norm_num))).measurable
  let γ := ((stdGaussian E).prod (stdGaussian E)).prod
    ((Measure.pi (fun _ : ι => stdGaussian E)).prod
      (Measure.pi (fun _ : ι => stdGaussian E)))
  let Φ := fun w : (E × E) × ((E × E) × ((ι → E) × (ι → E))) =>
    let P0 := Real.exp (-h / 2) • w.1.2 + Real.sqrt (1 - Real.exp (-h)) • w.2.1.1
    let Y0 := fun i => w.1.1 + t i • P0
    let Z0 := fun j => gradient V (q (Y0 j) + Real.sqrt eta • w.2.2.1 j)
    let Y1 := fun i => Y0 i - ∑ j, omega i j • Z0 j
    let Z1 := fun j => gradient V (q (Y1 j) + Real.sqrt eta • w.2.2.2 j)
    (w.1.1 + h • P0 - ∑ j, positionWeight j • Z1 j,
      Real.exp (-h / 2) • (P0 - ∑ j, momentumWeight j • Z1 j) +
        Real.sqrt (1 - Real.exp (-h)) • w.2.1.2)
  have hΦ : Measurable Φ := by
    dsimp only [Φ]
    fun_prop
  let K := (Kernel.id ×ₖ Kernel.const (E × E) γ).map Φ
  have hK : IsMarkovKernel K := Kernel.IsMarkovKernel.map _ hΦ
  refine ⟨sub_nonneg.mpr (Real.exp_le_one_iff.mpr (by linarith)),
    hΦ, K, hK, fun s => ?_⟩
  dsimp only [K]
  rw [Kernel.map_apply _ hΦ, Kernel.prod_apply, Kernel.id_apply, Kernel.const_apply,
    Measure.dirac_prod, Measure.map_map hΦ (by fun_prop)]
  rfl

end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ImplementedPhaseKernel
