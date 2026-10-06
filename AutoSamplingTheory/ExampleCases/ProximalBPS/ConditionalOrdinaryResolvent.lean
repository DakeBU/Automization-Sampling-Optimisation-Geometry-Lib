import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.OrdinaryWeakResolvent
import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradient

set_option autoImplicit false
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped ContDiff NNReal RealInnerProductSpace Topology
noncomputable section
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalOrdinaryResolvent

theorem conditional_ordinary_resolvent {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : NNReal} {η : ℝ}
    (hα : 0 < (α:ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (α:ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β:ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β:ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2)) (μ.prod (stdGaussian E))
    let W := fun y u : E => V ((1/2:ℝ) • (y+u)) + ‖u-y‖^2/(8*η)
    ∃ R S : Kernel E E, IsMarkovKernel R ∧ IsMarkovKernel S ∧
      (J.map Prod.swap).IsCondKernel R ∧
      (∀ y, S y = (R y).map (fun x => (2:ℝ) • x-y)) ∧
      ∀ y, S y = (volume : Measure E).tilted (fun u => -W y u) ∧
        ContDiff ℝ 2 (W y) ∧ Integrable (fun u => Real.exp (-W y u)) ∧
        0 < (∫ u, Real.exp (-W y u)) ∧
        ∃ D : Lp ℝ 2 (S y) →ₗ.[ℝ] Lp E 2 (S y),
          Dense (D.domain : Set (Lp ℝ 2 (S y))) ∧ D.IsClosable ∧ D.closure.IsClosed ∧
          (∀ (u : Lp ℝ 2 (S y)) (v : Lp E 2 (S y)), (u,v) ∈ D.graph ↔
            ∃ f : E → ℝ, ContDiff ℝ ∞ f ∧ HasCompactSupport f ∧
              u =ᵐ[S y] f ∧ v =ᵐ[S y] gradient f) ∧
      ∀ (ε : ℝ), 0 < ε → ∀ f : Lp ℝ 2 (S y),
      ∃ u : D.closure.domain,
        (∀ v : D.closure.domain,
          ε * ⟪(u : Lp ℝ 2 (S y)), (v : Lp ℝ 2 (S y))⟫ +
            ⟪D.closure u, D.closure v⟫ = ⟪f, (v : Lp ℝ 2 (S y))⟫) ∧
        LocallyIntegrable (fun x => (u : Lp ℝ 2 (S y)) x) ∧
        LocallyIntegrable (fun x => D.closure u x) ∧
        (∀ ψ : E → ℝ, ContDiff ℝ 1 ψ → HasCompactSupport ψ → ∀ v : E,
          Integrable (fun x => ψ x * inner ℝ (D.closure u x) v) ∧
          Integrable (fun x => (u : Lp ℝ 2 (S y)) x * fderiv ℝ ψ x v) ∧
          (∫ x, ψ x * inner ℝ (D.closure u x) v) =
            - ∫ x, (u : Lp ℝ 2 (S y)) x * fderiv ℝ ψ x v) ∧
        LocallyIntegrable (fun x => ‖ε * (u : Lp ℝ 2 (S y)) x +
          inner ℝ (gradient (W y) x) (D.closure u x) - f x‖ ^ 2) ∧
        (∀ K : Set E, IsCompact K →
          MemLp (fun x => (u : Lp ℝ 2 (S y)) x) 2 (volume.restrict K) ∧
          MemLp (fun x => D.closure u x) 2 (volume.restrict K) ∧
          MemLp (fun x => ε * (u : Lp ℝ 2 (S y)) x +
            inner ℝ (gradient (W y) x) (D.closure u x) - f x) 2 (volume.restrict K)) ∧
        ∀ φ : E → ℝ, ContDiff ℝ 2 φ → HasCompactSupport φ →
          Integrable (fun x => (u : Lp ℝ 2 (S y)) x * Laplacian.laplacian φ x) ∧
          Integrable (fun x => (ε * (u : Lp ℝ 2 (S y)) x +
            inner ℝ (gradient (W y) x) (D.closure u x) - f x) * φ x) ∧
          (∫ x, (u : Lp ℝ 2 (S y)) x * Laplacian.laplacian φ x) =
            ∫ x, (ε * (u : Lp ℝ 2 (S y)) x +
              inner ℝ (gradient (W y) x) (D.closure u x) - f x) * φ x := by
  obtain ⟨R,S,hR,hS,hcond,hSR,hfiber⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradient.conditional_gradient_closable hα hαβ hV hH hη hβη
  dsimp only
  refine ⟨R,S,hR,hS,hcond,hSR,?_⟩
  intro y
  obtain ⟨hSy,hW,hI,hZ,D,hDense,hClose,hClosed,hgraph⟩ := hfiber y
  refine ⟨hSy,hW,hI,hZ,D,hDense,hClose,hClosed,hgraph,?_⟩
  intro ε hε f
  let Wy : E → ℝ := fun u => V ((1/2:ℝ) • (y+u)) + ‖u-y‖^2/(8*η)
  have hW1 : ContDiff ℝ 1 Wy := hW.of_le (by norm_num)
  have hwc := AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.OrdinaryWeakResolvent.weak_resolvent_laplacian Wy hW1 hI
  dsimp only at hwc
  rw [← hSy] at hwc
  exact hwc D hClose hgraph ε hε f

end AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalOrdinaryResolvent
