import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.FirstOrderDifference
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv

noncomputable section
set_option backward.isDefEq.respectTransparency false
open Set MeasureTheory ProbabilityTheory InnerProductSpace
open scoped BigOperators RealInnerProductSpace
open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.FirstOrderDifference

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

-- The real nonlinear numerical phase: actual coefficients, both Gaussian
-- half-refreshes and all synchronously coupled inputs, including equal inputs.
example {h : ℝ} {J : ℕ}
    (hJ : 2 ≤ J) (hh : 0 < h) :
    let t := fun i : Fin J => h/2*(1-Real.cos ((i : ℝ)/(J-1 : ℝ)*Real.pi))
    let ell := fun j : Fin J => Lagrange.basis Finset.univ t j
    let Λ := sSup ((fun s : ℝ => ∑ j : Fin J, |(ell j).eval s|) '' Icc 0 h)
    let ω := fun i j : Fin J => ∫ s in 0..t i, (t i-s)*(ell j).eval s
    let b := fun j : Fin J => ∫ s in 0..h, (ell j).eval s
    let c := fun j : Fin J => ∫ s in 0..h, (h-s)*(ell j).eval s
    h ^ 2 * Λ ≤ 1 →
    let a := Real.exp (-h / 2)
    let sigma := Real.sqrt (1 - Real.exp (-h))
    let Γ := (stdGaussian ℝ).prod (stdGaussian ℝ)
    let P0 := fun (z ζ : ℝ × ℝ) => a • z.2 + sigma • ζ.1
    let Y0 := fun (z ζ : ℝ × ℝ) j => z.1 + t j • P0 z ζ
    let Y1 := fun (z ζ : ℝ × ℝ) i => Y0 z ζ i - ∑ j, ω i j • gradient potential (Y0 z ζ j)
    let Φ := fun w : (ℝ × ℝ) × (ℝ × ℝ) =>
      (w.1.1 + h • P0 w.1 w.2 - ∑ j, c j • gradient potential (Y1 w.1 w.2 j),
        a • (P0 w.1 w.2 - ∑ j, b j • gradient potential (Y1 w.1 w.2 j)) + sigma • w.2.2)
    Measurable Φ ∧
      (∃ K : Kernel (ℝ × ℝ) (ℝ × ℝ), IsMarkovKernel K ∧
        ∀ z, K z = Γ.map (fun ζ => Φ (z, ζ))) ∧
      ∀ z z' ζ : ℝ × ℝ,
        let H := h⁻¹ • ∑ j, b j •
          (∫ u in (0 : ℝ)..1, InnerProductSpace.continuousLinearMapOfBilin
            (fderiv ℝ (fderiv ℝ potential)
              (Y1 z' ζ j + u • (Y1 z ζ j - Y1 z' ζ j))))
        let d := WithLp.toLp 2 (z.1 - z'.1, z.2 - z'.2)
        H.toLinearMap.IsSymmetric ∧
          (∀ v, (1 / (2 * (1:ℝ))) * ‖v‖ ^ 2 ≤ inner ℝ (H v) v ∧
            inner ℝ (H v) v ≤ ‖v‖ ^ 2) ∧ ‖H‖ ≤ 1 ∧
          ∃ R : WithLp 2 (ℝ × ℝ) →L[ℝ] WithLp 2 (ℝ × ℝ),
            ‖R‖ ≤ 8 * Λ * h ^ 2 ∧
            WithLp.toLp 2 ((Φ (z,ζ)).1 - (Φ (z',ζ)).1,
              (Φ (z,ζ)).2 - (Φ (z',ζ)).2) =
                d + h • WithLp.toLp 2 (z.2-z'.2, -H (z.1-z'.1)-(z.2-z'.2)) + R d := by
  have hf : ContDiff ℝ 2 potential := by unfold potential; fun_prop
  exact source_first_order_difference (by norm_num : (1:ℝ) ≤ 1) hf
    potential_curvature hJ hh

#check @source_first_order_difference
#print axioms source_first_order_difference
