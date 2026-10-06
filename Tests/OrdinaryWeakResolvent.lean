import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalOrdinaryResolvent
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.InnerProductSpace.NormPow
import Mathlib.Analysis.Calculus.BumpFunction.Convolution

set_option autoImplicit false
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped ContDiff NNReal RealInnerProductSpace Topology
noncomputable section
namespace Tests.OrdinaryWeakResolvent

private def potential (x : ℝ) : ℝ := (3/8)*x^2 + (1/8)*Real.sin x
private theorem potential_curvature :
    ∀ z v : ℝ, (1/(2*(1:ℝ)))*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ potential) z v) v ∧
      (fderiv ℝ (fderiv ℝ potential) z v) v ≤ ‖v‖^2 := by
  have hder (z : ℝ) : HasDerivAt potential ((3/4)*z+(1/8)*Real.cos z) z := by
    convert (((hasDerivAt_id z).pow 2).const_mul (3/8)).add
      ((Real.hasDerivAt_sin z).const_mul (1/8)) using 1 <;> first | rfl | (simp [potential, Pi.add_apply, mul_comm]; ring)
  have hD : fderiv ℝ potential = fun z =>
      ((3/4)*z+(1/8)*Real.cos z) • ContinuousLinearMap.id ℝ ℝ := by
    funext z
    ext
    rw [fderiv_eq_smul_deriv, (hder z).deriv]
    simp
  have hDD (z v : ℝ) : (fderiv ℝ (fderiv ℝ potential) z v) v =
      ((3/4)-(1/8)*Real.sin z)*v^2 := by
    have hd : HasDerivAt (fun w : ℝ => (3/4)*w+(1/8)*Real.cos w)
        ((3/4)-(1/8)*Real.sin z) z := by
      convert ((hasDerivAt_id z).const_mul (3/4)).add
        ((Real.hasDerivAt_cos z).const_mul (1/8)) using 1 <;> (try dsimp only [id]) <;> first | rfl | ring
    rw [hD, fderiv_eq_smul_deriv,
      (hd.smul_const (ContinuousLinearMap.id ℝ ℝ)).deriv]
    simp
    ring
  intro z v
  rw [hDD]
  simp only [Real.norm_eq_abs, sq_abs]
  constructor <;> nlinarith [Real.sin_le_one z, Real.neg_one_le_sin z, sq_nonneg v]




theorem actual_nonconstant_c2_pde {η : ℝ} (hη : 0<η) (hη1 : η≤1) :
    let bump : ContDiffBump (0:ℝ) := {rIn:=1,rOut:=2,rIn_pos:=by norm_num,rIn_lt_rOut:=by norm_num}
    let μ := (volume : Measure ℝ).tilted (fun x => -potential x)
    let J := Measure.map (fun p : ℝ × ℝ => (p.1,p.1+Real.sqrt η • p.2)) (μ.prod (stdGaussian ℝ))
    let W := fun y u : ℝ => potential ((1/2:ℝ) • (y+u)) + ‖u-y‖^2/(8*η)
    ∃ R S : Kernel ℝ ℝ, IsMarkovKernel R ∧ IsMarkovKernel S ∧
      (J.map Prod.swap).IsCondKernel R ∧
      (∀ y, S y = (R y).map (fun x => (2:ℝ) • x-y)) ∧
      ∀ y, S y = (volume : Measure ℝ).tilted (fun u => -W y u) ∧
        ContDiff ℝ 2 (W y) ∧ Integrable (fun u => Real.exp (-W y u)) ∧
        0 < (∫ u, Real.exp (-W y u)) ∧
        ∃ D : Lp ℝ 2 (S y) →ₗ.[ℝ] Lp ℝ 2 (S y),
          Dense (D.domain : Set (Lp ℝ 2 (S y))) ∧ D.IsClosable ∧ D.closure.IsClosed ∧
          (∀ (u : Lp ℝ 2 (S y)) (v : Lp ℝ 2 (S y)), (u,v) ∈ D.graph ↔
            ∃ f : ℝ → ℝ, ContDiff ℝ ∞ f ∧ HasCompactSupport f ∧
              u =ᵐ[S y] f ∧ v =ᵐ[S y] gradient f) ∧
      ∀ (ε : ℝ), 0 < ε → ∀ f : Lp ℝ 2 (S y),
      ∃ u : D.closure.domain,
        (∀ v : D.closure.domain,
          ε * ⟪(u : Lp ℝ 2 (S y)), (v : Lp ℝ 2 (S y))⟫ +
            ⟪D.closure u, D.closure v⟫ = ⟪f, (v : Lp ℝ 2 (S y))⟫) ∧
        LocallyIntegrable (fun x => (u : Lp ℝ 2 (S y)) x) ∧
        LocallyIntegrable (fun x => D.closure u x) ∧
        (∀ ψ : ℝ → ℝ, ContDiff ℝ 1 ψ → HasCompactSupport ψ → ∀ v : ℝ,
          Integrable (fun x => ψ x * inner ℝ (D.closure u x) v) ∧
          Integrable (fun x => (u : Lp ℝ 2 (S y)) x * fderiv ℝ ψ x v) ∧
          (∫ x, ψ x * inner ℝ (D.closure u x) v) =
            - ∫ x, (u : Lp ℝ 2 (S y)) x * fderiv ℝ ψ x v) ∧
        LocallyIntegrable (fun x => ‖ε * (u : Lp ℝ 2 (S y)) x +
          inner ℝ (gradient (W y) x) (D.closure u x) - f x‖ ^ 2) ∧
        (∀ K : Set ℝ, IsCompact K →
          MemLp (fun x => (u : Lp ℝ 2 (S y)) x) 2 (volume.restrict K) ∧
          MemLp (fun x => D.closure u x) 2 (volume.restrict K) ∧
          MemLp (fun x => ε * (u : Lp ℝ 2 (S y)) x +
            inner ℝ (gradient (W y) x) (D.closure u x) - f x) 2 (volume.restrict K)) ∧
        let φ : ℝ → ℝ := fun x => bump.normed (volume : Measure ℝ) x * (x^2)^(5/2:ℝ)
        ;
          Integrable (fun x => (u : Lp ℝ 2 (S y)) x * Laplacian.laplacian φ x) ∧
          Integrable (fun x => (ε * (u : Lp ℝ 2 (S y)) x +
            inner ℝ (gradient (W y) x) (D.closure u x) - f x) * φ x) ∧
          (∫ x, (u : Lp ℝ 2 (S y)) x * Laplacian.laplacian φ x) =
            ∫ x, (ε * (u : Lp ℝ 2 (S y)) x +
              inner ℝ (gradient (W y) x) (D.closure u x) - f x) * φ x := by
  let bump : ContDiffBump (0:ℝ) := {rIn:=1,rOut:=2,rIn_pos:=by norm_num,rIn_lt_rOut:=by norm_num}
  let φ : ℝ → ℝ := fun x => bump.normed (volume : Measure ℝ) x * (x^2)^(5/2:ℝ)
  have hφ : ContDiff ℝ 2 φ :=
    (contDiff_infty.mp bump.contDiff_normed 2).mul
      ((Real.contDiff_rpow_const_of_le (by norm_num : ((2:ℕ):ℝ)≤5/2)).comp (contDiff_id.pow 2))
  have hc : HasCompactSupport φ := bump.hasCompactSupport_normed.mul_right
  have hf : ContDiff ℝ 2 potential := by unfold potential; fun_prop
  have hh : ∀ x v : ℝ, ((1/2:ℝ≥0):ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ potential) x v v ∧
      fderiv ℝ (fderiv ℝ potential) x v v ≤ ((1:ℝ≥0):ℝ)*‖v‖^2 := by
    intro x v
    simpa using potential_curvature x v
  obtain ⟨R,S,hR,hS,hcond,hSR,hfiber⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalOrdinaryResolvent.conditional_ordinary_resolvent
      (by norm_num : (0:ℝ≥0)<1/2) (by norm_num : (1/2:ℝ≥0)≤1) hf hh hη (by simpa using hη1)
  dsimp only
  refine ⟨R,S,hR,hS,hcond,hSR,?_⟩
  intro y
  obtain ⟨hSy,hW,hI,hZ,D,hDense,hClose,hClosed,hgraph,hsolve⟩ := hfiber y
  refine ⟨hSy,hW,hI,hZ,D,hDense,hClose,hClosed,hgraph,?_⟩
  intro ε hε f
  obtain ⟨u,hu,huL,hGL,hderiv,hr2,hlocal,hall⟩ := hsolve ε hε f
  refine ⟨u,hu,huL,hGL,hderiv,hr2,hlocal,?_⟩
  exact hall φ hφ hc

#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.OrdinaryWeakResolvent.weak_resolvent_laplacian
#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalOrdinaryResolvent.conditional_ordinary_resolvent
#print axioms actual_nonconstant_c2_pde
end Tests.OrdinaryWeakResolvent
