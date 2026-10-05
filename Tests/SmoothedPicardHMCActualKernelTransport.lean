import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ActualKernelTransport
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv

noncomputable section
set_option backward.isDefEq.respectTransparency false
open Set MeasureTheory ProbabilityTheory InnerProductSpace
open scoped BigOperators RealInnerProductSpace
open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ActualKernelTransport

-- Nonconstant positive Hessian, not a supplied gradient/Hessian certificate.
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

open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PhaseMetric

-- Full actual Gaussian Markov law and source transport for all probability inputs.
example {h : ℝ} {J : ℕ} (hJ : 2 ≤ J) (hh : 0 < h) :
    let t := fun i : Fin J => h/2*(1-Real.cos ((i : ℝ)/(J-1 : ℝ)*Real.pi))
    let ell := fun j : Fin J => Lagrange.basis Finset.univ t j
    let Λ := sSup ((fun s : ℝ => ∑ j : Fin J, |(ell j).eval s|) '' Icc 0 h)
    let ω := fun i j : Fin J => ∫ s in 0..t i, (t i-s)*(ell j).eval s
    let b := fun j : Fin J => ∫ s in 0..h, (ell j).eval s
    let c := fun j : Fin J => ∫ s in 0..h, (h-s)*(ell j).eval s
    h * Λ ≤ 1/(65536*(1:ℝ)) →
    let a := Real.exp (-h / 2)
    let sigma := Real.sqrt (1 - Real.exp (-h))
    let P0 := fun (z ζ : ℝ × ℝ) => a • z.2 + sigma • ζ.1
    let Y0 := fun (z ζ : ℝ × ℝ) j => z.1 + t j • P0 z ζ
    let Y1 := fun (z ζ : ℝ × ℝ) i => Y0 z ζ i - ∑ j, ω i j • gradient potential (Y0 z ζ j)
    let Φ := fun w : (ℝ × ℝ) × (ℝ × ℝ) =>
      (w.1.1 + h • P0 w.1 w.2 - ∑ j, c j • gradient potential (Y1 w.1 w.2 j),
        a • (P0 w.1 w.2 - ∑ j, b j • gradient potential (Y1 w.1 w.2 j)) + sigma • w.2.2)
    let Γ := (stdGaussian ℝ).prod (stdGaussian ℝ)
    ∃ K : Kernel (ℝ × ℝ) (ℝ × ℝ), IsMarkovKernel K ∧
      (∀ z, K z = Γ.map (fun ζ => Φ (z,ζ))) ∧
      ∀ (μ ν : Measure (ℝ × ℝ)), IsProbabilityMeasure μ → IsProbabilityMeasure ν →
        K ∘ₘ μ = (μ.prod Γ).map Φ ∧ K ∘ₘ ν = (ν.prod Γ).map Φ ∧
        phaseWassersteinSq (1:ℝ) (K ∘ₘ μ) (K ∘ₘ ν) ≤
          ENNReal.ofReal ((1-h/(65536*(1:ℝ)))^2) * phaseWassersteinSq (1:ℝ) μ ν := by
  have hf : ContDiff ℝ 2 potential := by unfold potential; fun_prop
  exact source_kernel_transport_contraction (by norm_num : (1:ℝ) ≤ 1) hf potential_curvature hJ hh

#print axioms source_kernel_transport_contraction
#print axioms AutoSamplingTheory.TechnicalLemmas.Measure.RandomizedMapTransport.transportCost_randomized_map_le
