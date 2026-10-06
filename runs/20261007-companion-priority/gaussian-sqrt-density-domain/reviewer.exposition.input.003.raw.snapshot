import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOSqrtDensity
noncomputable section
set_option autoImplicit false
set_option backward.isDefEq.respectTransparency false
open MeasureTheory InnerProductSpace ProbabilityTheory
open scoped RealInnerProductSpace NNReal
open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOSqrtDensity
namespace Tests.StandardizedRGOSqrtDensity

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

-- Genuine eta=2, y=3 posterior, not a Gaussian-output oracle or supplied moment.
-- The stationary point is forced to 1, and the relative residual is u^2.
theorem quadratic_eta_two_domains :
    let gamma := stdGaussian ℝ
    let R := ((volume : Measure ℝ).tilted (fun x => -x^2/2)).tilted
      (fun x => -‖x-3‖^2/4)
    let r := R.map (fun x => (Real.sqrt 2)⁻¹*(x-1))
    let Z := ∫ u, Real.exp (-u^2) ∂gamma
    let q := fun u => Real.exp (-u^2)/Z
    let f := fun u => Real.exp (-u^2/2)/Real.sqrt Z
    IsProbabilityMeasure r ∧
      r=gamma.withDensity (fun u => ENNReal.ofReal (q u)) ∧
      Integrable (fun u => q u*Real.log (q u)) gamma ∧
      MemLp f 2 gamma ∧ MemLp (gradient f) 2 gamma ∧
      (∀ u, gradient f u= -u*f u) ∧
      (∫ u, ‖gradient f u‖^2 ∂gamma)=(∫ u,u^2 ∂r) := by
  have hV : ContDiff ℝ 2 (quadratic 1) := by unfold quadratic; fun_prop
  have hH : ∀ x v : ℝ, (1 : ℝ)⁻¹*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ (quadratic 1)) x v v ∧
      fderiv ℝ (fderiv ℝ (quadratic 1)) x v v ≤ ‖v‖^2 := by
    intro x v; rw [quadratic_curvature]; norm_num
  obtain ⟨p,_hpm,hstat,hdata⟩ := standardized_rgo_sqrt_density_domain
    (κ := 1) (eta := fun _ : Unit => (2 : ℝ)) (y := fun _ : Unit => (3 : ℝ))
    (by norm_num) hV hH measurable_const measurable_const (by intro s; norm_num)
  have hp : p ()=1 := by
    have he := hstat ()
    rw [quadratic_gradient] at he
    simp only [one_mul,smul_eq_mul] at he
    linarith
  have hρ : (fun u => quadratic 1 (p ()+Real.sqrt 2 • u)-quadratic 1 (p ())-
      Real.sqrt 2*inner ℝ (gradient (quadratic 1) (p ())) u)=(fun u : ℝ => u^2) := by
    funext u
    rw [quadratic_gradient]
    simp only [quadratic,one_mul,smul_eq_mul,real_inner_comm]
    change (p ()+Real.sqrt 2*u)^2/2-(p ())^2/2-Real.sqrt 2*(p ()*u)=u^2
    nlinarith [Real.sq_sqrt (by norm_num : (0 : ℝ)≤2)]
  have hs := hdata ()
  have hρpoint (u : ℝ) : quadratic 1 (p ()+Real.sqrt 2 • u)-quadratic 1 (p ())-
      Real.sqrt 2*inner ℝ (gradient (quadratic 1) (p ())) u=u^2 := congrFun hρ u
  dsimp only at hs
  simp only [hρpoint] at hs
  obtain ⟨_hZ,_hZone,_hlaw,hdensity,hprob,_hfq,_hqone,_hf,hflp,hfglp,
      _hρlp,he,hdf,_hdlog,henergy⟩ := hs
  have hρgrad : gradient (fun u : ℝ => u^2)=(fun u => 2*u) := by
    funext u
    have hd : HasDerivAt (fun z : ℝ => z^2) (2*u) u := by
      convert! (hasDerivAt_id u).pow 2 using 1
      simp
    exact hd.hasGradientAt.gradient
  rw [hρgrad] at hdf henergy
  have hdf' : ∀ u, gradient
      (fun u : ℝ => Real.exp (-u^2/2)/Real.sqrt (∫ z,Real.exp (-z^2) ∂stdGaussian ℝ)) u =
      -u*(Real.exp (-u^2/2)/Real.sqrt (∫ z,Real.exp (-z^2) ∂stdGaussian ℝ)) := by
    intro u
    rw [hdf u]
    simp only [smul_eq_mul]
    ring
  simp_rw [Real.norm_eq_abs,sq_abs,mul_pow] at henergy
  rw [integral_const_mul] at henergy
  simp only [show (2:ℝ)^2=4 by norm_num,← mul_assoc,
    show (1/4:ℝ)*4=1 by norm_num,one_mul] at henergy
  refine ⟨?_,?_,?_,?_,?_,?_,?_⟩
  · simpa only [quadratic,one_mul,neg_div,hp,smul_eq_mul,
      show 2*(2 : ℝ)=4 by norm_num] using hprob
  · simpa only [quadratic,one_mul,neg_div,hp,smul_eq_mul,
      show 2*(2 : ℝ)=4 by norm_num] using hdensity
  · simpa only [neg_div] using he
  · simpa only [neg_div] using hflp
  · simpa only [neg_div] using hfglp
  · simpa only [neg_div] using hdf'
  · simpa only [quadratic,one_mul,neg_div,hp,smul_eq_mul,
      Real.norm_eq_abs,sq_abs,show 2*(2 : ℝ)=4 by norm_num] using henergy

#print axioms AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOSqrtDensity.standardized_rgo_sqrt_density_domain
#print axioms quadratic_eta_two_domains
end Tests.StandardizedRGOSqrtDensity
