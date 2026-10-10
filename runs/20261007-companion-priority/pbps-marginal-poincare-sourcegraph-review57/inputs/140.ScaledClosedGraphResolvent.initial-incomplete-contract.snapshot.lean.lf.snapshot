import Mathlib.Analysis.InnerProductSpace.Dual
import Mathlib.Analysis.InnerProductSpace.ProdL2
import Mathlib.Analysis.Normed.Module.WeakDual
import Mathlib.Topology.Algebra.Module.LinearPMap
set_option autoImplicit false
noncomputable section
open Filter InnerProductSpace
open scoped Topology RealInnerProductSpace
namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.ScaledClosedGraphResolvent
variable {H K : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]

theorem scaled_resolvent_sequence_tendsto_zero
    [TopologicalSpace.SeparableSpace H]
    (D : H →ₗ.[ℝ] K) (hD : D.IsClosed) (f : H)
    (ε : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hε0 : Tendsto ε atTop (𝓝 0))
    (u : ℕ → D.domain)
    (hv : ∀ n, ∀ v : D.domain,
      ε n*inner ℝ (u n : H) (v : H)+inner ℝ (D (u n)) (D v)=inner ℝ f (v : H))
    (hk : ∀ v : D.domain, D v=0 → inner ℝ f (v : H)=0) :
    Tendsto (fun n => ε n • (u n : H)) atTop (𝓝 0) ∧
    Tendsto (fun n => ε n • D (u n)) atTop (𝓝 0) 