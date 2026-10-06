import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedScorePosterior
import Mathlib.Analysis.InnerProductSpace.PiL2

noncomputable section
set_option autoImplicit false
set_option backward.isDefEq.respectTransparency false
open MeasureTheory InnerProductSpace
open scoped RealInnerProductSpace NNReal
open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedScorePosterior
namespace Tests.SmoothedScorePosterior

private def quadratic (c : ℝ) (x : ℝ) : ℝ := c*x^2/2
private theorem quadratic_gradient (c : ℝ) : gradient (quadratic c) = fun x => c*x := by
  funext x
  have h : HasDerivAt (quadratic c) (c*x) x := by
    convert (((hasDerivAt_id x).pow 2).const_mul c).div_const 2 using 1 <;>
      first | rfl | (simp only [id_eq]; ring)
  exact h.hasGradientAt.gradient

private theorem quadratic_curvature (c x v : ℝ) :
    fderiv ℝ (fderiv ℝ (quadratic c)) x v v = c*‖v‖^2 := by
  have hd (z : ℝ) : HasDerivAt (quadratic c) (c*z) z := by
    convert (((hasDerivAt_id z).pow 2).const_mul c).div_const 2 using 1 <;>
      first | rfl | (simp only [id_eq]; ring)
  have hf : fderiv ℝ (quadratic c) = fun z => (c*z) • ContinuousLinearMap.id ℝ ℝ := by
    funext z
    ext
    rw [fderiv_eq_smul_deriv,(hd z).deriv]
    simp
  have hh : deriv (fun z : ℝ => (c*z) • ContinuousLinearMap.id ℝ ℝ) x =
      c • ContinuousLinearMap.id ℝ ℝ := by
    simpa only [id_eq,mul_one] using
      (((hasDerivAt_id x).const_mul c).smul_const (ContinuousLinearMap.id ℝ ℝ)).deriv
  rw [hf,fderiv_eq_smul_deriv,hh]
  simp [Real.norm_eq_abs,pow_two]
  ring

-- eta=2 is beyond the old eta<=1 cap. All objects are the actual integral
-- potential and genuine posterior, with the exact printed Gaussian prefactor.
theorem quadratic_eta_two_score :
    let A := fun y : ℝ => ((Real.sqrt (4*Real.pi))⁻¹)*
      ∫ x,Real.exp (-x^2/2-‖y-x‖^2/4) ∂(volume : Measure ℝ)
    let R := ((volume : Measure ℝ).tilted (fun x => -x^2/2)).tilted
      (fun x => -‖x-3‖^2/4)
    IsProbabilityMeasure R ∧ Integrable id R ∧
      gradient (fun y => -Real.log (A y)) 3=1 ∧ (∫ x,x ∂R)=1 := by
  have hV : ContDiff ℝ 2 (quadratic 1) := by unfold quadratic; fun_prop
  have hH : ∀ x v : ℝ, (1 : ℝ)⁻¹*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ (quadratic 1)) x v v ∧
      fderiv ℝ (fderiv ℝ (quadratic 1)) x v v ≤ ‖v‖^2 := by
    intro x v; rw [quadratic_curvature]; norm_num
  obtain ⟨_hμ,_hC2,hpost,p,_hpm,hstat,hstd⟩ :=
    smoothed_score_posterior (κ := 1) (η := 2) (by norm_num) hV hH (by norm_num)
  let R := ((volume : Measure ℝ).tilted (fun x => -x^2/2)).tilted (fun x => -‖x-3‖^2/4)
  have hRorig : ((volume : Measure ℝ).tilted (fun x => -quadratic 1 x)).tilted
      (fun x => -‖x-3‖^2/(2*2))=R := by
    norm_num [R,quadratic,neg_div]
  let rho := fun u => quadratic 1 (p 3+Real.sqrt 2 • u)-quadratic 1 (p 3)-
    Real.sqrt 2*inner ℝ (gradient (quadratic 1) (p 3)) u
  let r := R.map (fun x => (Real.sqrt 2)⁻¹ • (x-p 3))
  have hp : p 3=1 := by
    have he := hstat 3
    rw [quadratic_gradient] at he
    simp only [one_mul,smul_eq_mul] at he
    linarith
  have hρ : rho=(fun u : ℝ => u^2) := by
    funext u
    dsimp only [rho]
    rw [quadratic_gradient]
    simp only [quadratic,one_mul,smul_eq_mul,real_inner_comm]
    change (p 3+Real.sqrt 2*u)^2/2-(p 3)^2/2-Real.sqrt 2*(p 3*u)=u^2
    nlinarith [Real.sq_sqrt (by norm_num : (0 : ℝ)≤2)]
  obtain ⟨hrlaw,_hrp,_hrlp,hscore,_heval⟩ := hstd 3
  have hr : r=(volume : Measure ℝ).tilted (fun u => -quadratic 3 u) := by
    have ht : r=(volume : Measure ℝ).tilted (fun u => -(‖u‖^2/2+rho u)) := by
      simpa only [r,R,rho,quadratic,one_mul,neg_div,
        show 2*(2 : ℝ)=4 by norm_num] using hrlaw
    rw [ht,hρ]
    congr 1
    funext u
    simp only [quadratic,Real.norm_eq_abs,sq_abs]
    ring
  have hHQ : ∀ x v : ℝ, ((3 : ℝ≥0) : ℝ)*‖v‖^2 ≤
      fderiv ℝ (fderiv ℝ (quadratic 3)) x v v ∧
      fderiv ℝ (fderiv ℝ (quadratic 3)) x v v ≤ ((3 : ℝ≥0) : ℝ)*‖v‖^2 := by
    intro x v; rw [quadratic_curvature]; norm_num
  have hm := AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMean.integrable_gradient_and_integral_eq_zero
    (by norm_num : (0 : ℝ≥0)<3) (by unfold quadratic; fun_prop) hHQ
  have hz : (∫ u,u ∂r)=0 := by
    have he := hr.symm ▸ hm.2.2
    rw [quadratic_gradient,integral_const_mul] at he
    linarith
  have hρgrad : gradient rho=(fun u : ℝ => 2*u) := by
    rw [hρ]
    funext u
    have hd : HasDerivAt (fun z : ℝ => z^2) (2*u) u := by
      convert! (hasDerivAt_id u).pow 2 using 1
      simp
    exact hd.hasGradientAt.gradient
  have hρzero : (∫ u,gradient rho u ∂r)=0 := by
    rw [hρgrad,integral_const_mul,hz,mul_zero]
  have hs : gradient (fun y : ℝ => -Real.log (((Real.sqrt (4*Real.pi))⁻¹)*
      ∫ x,Real.exp (-x^2/2-‖y-x‖^2/4) ∂(volume : Measure ℝ))) 3=1 := by
    have he := hscore
    dsimp only at he
    rw [hRorig] at he
    change gradient _ 3=gradient (quadratic 1) (p 3)+(Real.sqrt 2)⁻¹ •
      (∫ u,gradient rho u ∂r) at he
    rw [hρzero,smul_zero,add_zero,quadratic_gradient,hp] at he
    simp only [one_mul] at he
    simpa only [quadratic,one_mul,neg_div,Module.finrank_self,pow_one,
      show 2*(2 : ℝ)=4 by norm_num,
      show 2*Real.pi*2=4*Real.pi by ring] using he
  obtain ⟨hRp,hXL2,_hgradL1,hmean⟩ := hpost 3
  have hR' : IsProbabilityMeasure R := hRorig ▸ hRp
  have hX' : Integrable id R := hRorig ▸ hXL2.integrable (by norm_num)
  refine ⟨hR',hX',hs,?_⟩
  have he := hmean
  dsimp only at he
  rw [hRorig] at he
  rw [quadratic_gradient] at he
  simp only [one_mul] at he
  rw [← he]
  simpa only [quadratic,one_mul,neg_div,Module.finrank_self,pow_one,
    show 2*(2 : ℝ)=4 by norm_num,
    show 2*Real.pi*2=4*Real.pi by ring] using hs

#print axioms AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedScorePosterior.smoothed_score_posterior
#print axioms quadratic_eta_two_score

end Tests.SmoothedScorePosterior
