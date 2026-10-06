import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.FullRangeProximalGaussianOracle
import AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment
import Mathlib.Analysis.InnerProductSpace.PiL2

noncomputable section
set_option autoImplicit false
open MeasureTheory ProbabilityTheory InnerProductSpace
open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.FullRangeProximalGaussianOracle
namespace Tests.FullRangeProximalGaussianOracle

private def quadratic (x : ℝ) : ℝ := x^2/2

private theorem quadratic_gradient : gradient quadratic = id := by
  funext x
  have hd : HasDerivAt quadratic x x := by
    convert ((hasDerivAt_id x).pow 2).div_const 2 using 1 <;>
      first | rfl | (simp only [id_eq];ring)
  simpa using hd.hasGradientAt.gradient

private theorem quadratic_curvature (x v : ℝ) :
    fderiv ℝ (fderiv ℝ quadratic) x v v = ‖v‖^2 := by
  have hd (z : ℝ) : HasDerivAt quadratic z z := by
    convert ((hasDerivAt_id z).pow 2).div_const 2 using 1 <;>
      first | rfl | (simp only [id_eq];ring)
  have hf : fderiv ℝ quadratic = fun z => z • ContinuousLinearMap.id ℝ ℝ := by
    funext z
    ext
    rw [fderiv_eq_smul_deriv,(hd z).deriv]
    simp
  have hDD : deriv (fun z : ℝ => z • ContinuousLinearMap.id ℝ ℝ) x =
      ContinuousLinearMap.id ℝ ℝ := by
    simpa only [id_eq,one_smul] using
      ((hasDerivAt_id x).smul_const (ContinuousLinearMap.id ℝ ℝ)).deriv
  rw [hf,fderiv_eq_smul_deriv,hDD]
  simp [Real.norm_eq_abs,pow_two]

-- The source constructor is tested with genuinely varying eta and center.
-- For the quadratic potential its gradient-output law has centered moment eta;
-- this is a noise-evaluation law, not the RGO posterior law.
theorem quadratic_variable_eta
    {S : Type*} [MeasurableSpace S] {eta y : S → ℝ}
    (heta : Measurable eta) (hy : Measurable y)
    (hpos : ∀ s, 0 < eta s) :
    ∃ K : Kernel S ℝ, IsMarkovKernel K ∧
      ∀ s, K s = (stdGaussian ℝ).map
        (fun z => y s/(1+eta s)+Real.sqrt (eta s)*z) ∧
        (∫ w, ‖w-y s/(1+eta s)‖^2 ∂K s) = eta s ∧
        (∀ z, (quadratic z+(eta s)⁻¹/2*‖z-y s‖^2 ≤
          quadratic (y s/(1+eta s))+(eta s)⁻¹/2*‖y s/(1+eta s)-y s‖^2)
          ↔ z=y s/(1+eta s)) ∧
        Integrable (fun w : ℝ => w) (K s) ∧
          ∀ (a t : ℝ), Integrable
            (fun w => Real.exp (t*inner ℝ a (w-∫ v, v ∂K s))) (K s) := by
  have hV : ContDiff ℝ 2 quadratic := by unfold quadratic;fun_prop
  have hH : ∀ x v : ℝ, (1:ℝ)⁻¹*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ quadratic) x v v ∧
      fderiv ℝ (fderiv ℝ quadratic) x v v ≤ ‖v‖^2 := by
    intro x v;rw [quadratic_curvature];norm_num
  obtain ⟨p,hp,heq,hmin,hnexp,hG,hLip,K,hK,hKs,hDomain⟩ :=
    full_range_proximal_gaussian_oracle (κ:=1) (by norm_num) hV hH heta hy hpos
  have hpform (s : S) : p s=y s/(1+eta s) := by
    apply (eq_div_iff (ne_of_gt (by linarith [hpos s] : 0<1+eta s))).mpr
    have h := heq s
    rw [quadratic_gradient] at h
    simp only [id_eq,smul_eq_mul] at h
    nlinarith
  refine ⟨K,hK,fun s => ?_⟩
  have hlaw : K s=(stdGaussian ℝ).map
      (fun z => y s/(1+eta s)+Real.sqrt (eta s)*z) := by
    simpa only [quadratic_gradient,id_eq,hpform,smul_eq_mul] using hKs s
  refine ⟨hlaw,?_,?_,hDomain s⟩
  · rw [hlaw,integral_map (by fun_prop) (by fun_prop)]
    have hm := AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian (E:=ℝ)
    calc
      _ = ∫ z : ℝ, eta s*‖z‖^2 ∂stdGaussian ℝ := by
        apply integral_congr_ae
        filter_upwards with z
        simp only [add_sub_cancel_left,norm_mul,Real.norm_eq_abs,sq_abs,mul_pow]
        rw [Real.sq_sqrt (hpos s).le]
      _ = eta s := by rw [integral_const_mul,hm.2];simp
  · intro z
    simpa only [hpform] using (hmin s z).2

theorem quadratic_eta_one :
    ∃ K : Kernel ℝ ℝ, IsMarkovKernel K ∧
      ∀ y, K y=(stdGaussian ℝ).map (fun z => y/2+z) ∧
        (∫ w, ‖w-y/2‖^2 ∂K y)=1 := by
  obtain ⟨K,hK,h⟩ := quadratic_variable_eta (eta:=fun _ : ℝ => 1) (y:=id)
    measurable_const measurable_id (by norm_num)
  refine ⟨K,hK,fun y => ?_⟩
  have hy := h y
  norm_num at hy
  refine ⟨hy.1,?_⟩
  simpa only [Real.norm_eq_abs,sq_abs] using hy.2.1

-- This unbounded parameter family has contraction factors tending to one;
-- its actual centered Gaussian-output moment grows without a uniform cap.
theorem quadratic_unbounded_eta :
    ∃ K : Kernel ℕ ℝ, IsMarkovKernel K ∧
      ∀ n, K n=(stdGaussian ℝ).map
          (fun z => 3/((n:ℝ)+3)+Real.sqrt ((n:ℝ)+2)*z) ∧
        (∫ w, ‖w-3/((n:ℝ)+3)‖^2 ∂K n)=(n:ℝ)+2 ∧
        Integrable (fun w : ℝ => w) (K n) ∧
          Integrable (fun w => Real.exp ((-3)*inner ℝ (2:ℝ) (w-∫ v, v ∂K n))) (K n) := by
  obtain ⟨K,hK,h⟩ := quadratic_variable_eta
    (eta:=fun n : ℕ => (n:ℝ)+2) (y:=fun _ => 3)
    (by fun_prop) measurable_const (by intro n;positivity)
  refine ⟨K,hK,fun n => ?_⟩
  have he : 1+((n:ℝ)+2)=(n:ℝ)+3 := by ring
  have hn := h n
  rw [he] at hn
  exact ⟨hn.1,hn.2.1,hn.2.2.2.1,hn.2.2.2.2 2 (-3)⟩

abbrev E0 := EuclideanSpace ℝ (Fin 0)
theorem zero_dimension_variable_eta
    {S : Type*} [MeasurableSpace S] {eta : S → ℝ}
    (heta : Measurable eta) (hpos : ∀ s, 0<eta s) :
    ∃ K : Kernel S E0, IsMarkovKernel K ∧
      ∀ s, K s=Measure.dirac (0:E0) := by
  have hh : ∀ x v : E0, (1:ℝ)⁻¹*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ (fun _ : E0 => (7:ℝ))) x v v ∧
      fderiv ℝ (fderiv ℝ (fun _ : E0 => (7:ℝ))) x v v ≤ ‖v‖^2 := by
    intro x v;have hv : v=0 := Subsingleton.elim _ _;simp [hv]
  obtain ⟨p,hp,heq,hmin,hnexp,hG,hLip,K,hK,hKs,_hDomain⟩ :=
    full_range_proximal_gaussian_oracle (κ:=1) (by norm_num)
      contDiff_const hh heta (y:=fun _ => 0) measurable_const hpos
  refine ⟨K,hK,fun s => ?_⟩
  have hf : (fun z => gradient (fun _ : E0 => (7:ℝ)) (p s+Real.sqrt (eta s) • z))=
      fun _ : E0 => (0:E0) := by funext z;exact Subsingleton.elim _ _
  rw [hKs s,hf]
  simp

#print axioms full_range_proximal_gaussian_oracle
#print axioms quadratic_variable_eta
#print axioms quadratic_eta_one
#print axioms quadratic_unbounded_eta
#print axioms zero_dimension_variable_eta
end Tests.FullRangeProximalGaussianOracle
end
