import Mathlib.Analysis.InnerProductSpace.Projection.Basic
import Mathlib.Analysis.InnerProductSpace.ProdL2
import Mathlib.Topology.Algebra.Module.LinearPMap
namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.ClosedGraphResolvent
open scoped RealInnerProductSpace

theorem weak_resolvent {H K : Type*}
    [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    [NormedAddCommGroup K] [InnerProductSpace ℝ K] [CompleteSpace K]
    (A : H →ₗ.[ℝ] K) (hA : A.IsClosed) (ε : ℝ) (hε : 0 < ε) (f : H) :
    ∃ u : A.domain,
      (∀ v : A.domain, ε * ⟪(u : H), (v : H)⟫ + ⟪A u, A v⟫ = ⟪f, (v : H)⟫) ∧
      ε * ‖(u : H)‖^2 + ‖A u‖^2 = ⟪f, (u : H)⟫ ∧
      ‖(u : H)‖ ≤ ε⁻¹ * ‖f‖ ∧
      ε * ‖(u : H)‖^2 + ‖A u‖^2 ≤ ε⁻¹ * ‖f‖^2 ∧
      ∀ w : A.domain,
        (∀ v : A.domain, ε * ⟪(w : H), (v : H)⟫ + ⟪A w, A v⟫ = ⟪f, (v : H)⟫) → w = u 