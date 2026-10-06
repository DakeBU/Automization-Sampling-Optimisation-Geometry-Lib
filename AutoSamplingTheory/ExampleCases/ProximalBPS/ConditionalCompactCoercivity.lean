import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactWeightedPoissonCoercivity
import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreDomain
import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalLocalizedResolvent

set_option autoImplicit false
open MeasureTheory ProbabilityTheory InnerProductSpace
open TemperedDistribution
open scoped SchwartzMap ContDiff NNReal RealInnerProductSpace Topology
noncomputable section
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalCompactCoercivity

theorem conditional_compact_coercivity {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
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
        (∀ φ : E → ℝ, ContDiff ℝ 2 φ → HasCompactSupport φ →
          Integrable (fun x => (u : Lp ℝ 2 (S y)) x * Laplacian.laplacian φ x) ∧
          Integrable (fun x => (ε * (u : Lp ℝ 2 (S y)) x +
            inner ℝ (gradient (W y) x) (D.closure u x) - f x) * φ x) ∧
          (∫ x, (u : Lp ℝ 2 (S y)) x * Laplacian.laplacian φ x) =
            ∫ x, (ε * (u : Lp ℝ 2 (S y)) x +
              inner ℝ (gradient (W y) x) (D.closure u x) - f x) * φ x) ∧
        ∀ χ : E → ℝ, ContDiff ℝ 2 χ → HasCompactSupport χ →
    let v := fun x => χ x * (u : Lp ℝ 2 (S y)) x
    let Gχ := fun x => χ x • D.closure u x + (u : Lp ℝ 2 (S y)) x • gradient χ x
    let Fχ := fun x => χ x * (ε * (u : Lp ℝ 2 (S y)) x + inner ℝ (gradient (W y) x) (D.closure u x) - f x) + 2 * inner ℝ (gradient χ x) (D.closure u x) +
      (u : Lp ℝ 2 (S y)) x * Laplacian.laplacian χ x
    MemLp v 2 volume ∧ MemLp Gχ 2 volume ∧ MemLp Fχ 2 volume ∧
    tsupport v ⊆ tsupport χ ∧ tsupport Gχ ⊆ tsupport χ ∧ tsupport Fχ ⊆ tsupport χ ∧
    (∀ ψ : E → ℝ, ContDiff ℝ 1 ψ → HasCompactSupport ψ → ∀ a : E,
      Integrable (fun x => ψ x * inner ℝ (Gχ x) a) ∧
      Integrable (fun x => v x * fderiv ℝ ψ x a) ∧
      (∫ x, ψ x * inner ℝ (Gχ x) a) = -∫ x, v x * fderiv ℝ ψ x a) ∧
    (∀ ψ : E → ℝ, ContDiff ℝ 2 ψ → HasCompactSupport ψ →
      Integrable (fun x => v x * Laplacian.laplacian ψ x) ∧
      Integrable (fun x => Fχ x * ψ x) ∧
      (∫ x, v x * Laplacian.laplacian ψ x) = ∫ x, Fχ x * ψ x) ∧
    let Aχ := fun x => inner ℝ (gradient (W y) x) (Gχ x)-Fχ x
    MemLp v 2 (S y) ∧ MemLp Gχ 2 (S y) ∧ MemLp Aχ 2 (S y) ∧
    ∃ vW AW : Lp ℝ 2 (S y), ∃ GW : Lp E 2 (S y),
      vW =ᵐ[S y] v ∧ AW =ᵐ[S y] Aχ ∧ GW =ᵐ[S y] Gχ ∧
      (vW,GW) ∈ D.closure.graph ∧ (((α:ℝ)+1/η)/4) * ‖GW‖^2 ≤ ‖AW‖^2 := by
  obtain ⟨_R2,_S2,_hR2,_hS2,_hcond2,_hSR2,hcurv⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreDomain.conditional_curvature_and_score_domain
      hα hαβ hV hH hη hβη
  obtain ⟨R,S,hR,hS,hcond,hSR,hfiber⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalLocalizedResolvent.conditional_localized_resolvent hα hαβ hV hH hη hβη
  dsimp only
  refine ⟨R,S,hR,hS,hcond,hSR,?_⟩
  intro y
  obtain ⟨hSy,hW,hI,hZ,D,hDense,hClose,hClosed,hgraph,hsolve⟩ := hfiber y
  obtain ⟨_,_,_,_,hlower,_,_⟩ := hcurv y
  refine ⟨hSy,hW,hI,hZ,D,hDense,hClose,hClosed,hgraph,?_⟩
  intro ε hε f
  obtain ⟨u,hu,huL,hgradL,hd,hr2,hl,hp,hcut⟩ := hsolve ε hε f
  refine ⟨u,hu,huL,hgradL,hd,hr2,hl,hp,?_⟩
  intro χ hχ hc
  obtain ⟨hv,hg,hf,hvs,hgs,hfs,hfirst,hsecond⟩ := hcut χ hχ hc
  refine ⟨hv,hg,hf,hvs,hgs,hfs,hfirst,hsecond,?_⟩
  exact AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactWeightedPoissonCoercivity.compact_weak_poisson_weighted_coercivity
    (fun z => V ((1/2:ℝ) • (y+z)) + ‖z-y‖^2/(8*η)) hW hI hZ
    (((α:ℝ)+1/η)/4) hlower (S y) hSy D hClose hgraph
    (fun x => χ x * (u : Lp ℝ 2 (S y)) x)
    (fun x => χ x * (ε * (u : Lp ℝ 2 (S y)) x +
      inner ℝ (gradient (fun z => V ((1/2:ℝ) • (y+z)) + ‖z-y‖^2/(8*η)) x)
        (D.closure u x) - f x) + 2 * inner ℝ (gradient χ x) (D.closure u x) +
      (u : Lp ℝ 2 (S y)) x * Laplacian.laplacian χ x)
    (fun x => χ x • D.closure u x + (u : Lp ℝ 2 (S y)) x • gradient χ x)
    (tsupport χ) hc hvs hfs hgs hv hf hg hfirst hsecond

end AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalCompactCoercivity
