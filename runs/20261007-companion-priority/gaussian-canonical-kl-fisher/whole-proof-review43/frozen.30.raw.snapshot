import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOSqrtDensity
import AutoSamplingTheory.TechnicalLemmas.InformationTheory.TiltedKL
import AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity
import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder

/-!
# Actual standardized RGO unique proximal point and canonical finite entropy

SPHMC arXiv:2609.06906v1 S3.E2/S4.Ex3 actual proximal point and S4.Ex8
standardized posterior, with omitted canonical entropy prerequisites before
FIRST S4.E6. The measurable family is an authored extension; Unit recovers
fixed parameters. Every positive eta is admitted. Canonical llr is identified
only almost everywhere for integrability and integrals, never differentiated.
Gaussian LSI/T2, weak Sobolev, W2, bias, algorithms and main results remain open.
-/

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGORelativeEntropy
open MeasureTheory InnerProductSpace ProbabilityTheory
open scoped RealInnerProductSpace NNReal
noncomputable section
set_option autoImplicit false
set_option backward.isDefEq.respectTransparency false

theorem standardized_rgo_unique_prox_and_finite_entropy
    {E S : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    [MeasurableSpace S] {V : E → ℝ} {κ : ℝ}
    (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, κ⁻¹*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v ∧
      fderiv ℝ (fderiv ℝ V) x v v ≤ ‖v‖^2)
    {eta : S → ℝ} {y : S → E} (heta : Measurable eta) (hy : Measurable y)
    (hpos : ∀ s, 0 < eta s) :
    ∃ p : S → E, Measurable p ∧
      (∀ s, p s+eta s • gradient V (p s)=y s) ∧
      (∀ s z, z+eta s • gradient V z=y s → z=p s) ∧
      let rho := fun s u => V (p s+Real.sqrt (eta s) • u)-V (p s)-
        Real.sqrt (eta s)*inner ℝ (gradient V (p s)) u
      let mu := (volume : Measure E).tilted (fun x => -V x)
      let R := fun s => mu.tilted (fun x => -‖x-y s‖^2/(2*eta s))
      let r := fun s => (R s).map (fun x => (Real.sqrt (eta s))⁻¹ • (x-p s))
      let gamma := stdGaussian E
      let Z := fun s => ∫ u, Real.exp (-rho s u) ∂gamma
      let q := fun s u => Real.exp (-rho s u)/Z s
      ∀ s, r s ≪ gamma ∧
        _root_.InformationTheory.klDiv (r s) gamma ≠ ⊤ ∧
        Integrable (MeasureTheory.llr (r s) gamma) (r s) ∧
        MeasureTheory.llr (r s) gamma =ᵐ[r s] (fun u => Real.log (q s u)) ∧
        Integrable (rho s) (r s) ∧
        (_root_.InformationTheory.klDiv (r s) gamma).toReal =
          (∫ u, q s u*Real.log (q s u) ∂gamma) ∧
        (_root_.InformationTheory.klDiv (r s) gamma).toReal =
          -(∫ u, rho s u ∂r s)-Real.log (Z s) := by
  obtain ⟨p,hpm,hstat,hdata⟩ :=
    StandardizedRGOSqrtDensity.standardized_rgo_sqrt_density_domain hκ hV hH heta hy hpos
  have hsc := AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity.strongConvexOn_univ_of_fderiv2_lower
    hV (fun x v => (hH x v).1)
  have hunique : ∀ s z, z+eta s • gradient V z=y s → z=p s := by
    intro s z hz
    have hm := AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder.gradient_inner_lower_bound_of_strongConvexOn
      hsc (fun w _ => (hV.differentiable (by norm_num) w).hasGradientAt)
      (x := p s) (y := z) (Set.mem_univ _) (Set.mem_univ _)
    have hg : 0 ≤ inner ℝ (gradient V z-gradient V (p s)) (z-p s) :=
      le_trans (mul_nonneg (inv_nonneg.mpr (by linarith : 0 ≤ κ)) (sq_nonneg _)) hm
    have hzero : z-p s+eta s • (gradient V z-gradient V (p s))=0 := by
      calc
        _=(z+eta s • gradient V z)-(p s+eta s • gradient V (p s)) := by module
        _=0 := by rw [hz,hstat s,sub_self]
    have hi := congrArg (fun w => inner ℝ w (z-p s)) hzero
    simp only [inner_add_left,inner_smul_left,real_inner_self_eq_norm_sq,
      inner_zero_left,starRingEnd_apply,star_trivial] at hi
    have hn : ‖z-p s‖=0 := by
      nlinarith [mul_nonneg (hpos s).le hg,norm_nonneg (z-p s)]
    exact sub_eq_zero.mp (norm_eq_zero.mp hn)
  let rho := fun s u => V (p s+Real.sqrt (eta s) • u)-V (p s)-
    Real.sqrt (eta s)*inner ℝ (gradient V (p s)) u
  let mu := (volume : Measure E).tilted (fun x => -V x)
  let R := fun s => mu.tilted (fun x => -‖x-y s‖^2/(2*eta s))
  let r := fun s => (R s).map (fun x => (Real.sqrt (eta s))⁻¹ • (x-p s))
  let gamma := stdGaussian E
  let Z := fun s => ∫ u, Real.exp (-rho s u) ∂gamma
  let q := fun s u => Real.exp (-rho s u)/Z s
  refine ⟨p,hpm,hstat,hunique,?_⟩
  change ∀ s, r s ≪ gamma ∧ _
  change ∀ s, 0 < Z s ∧ Z s ≤ 1 ∧ _ at hdata
  intro s
  obtain ⟨hZ,_hZone,hr,_hwith,hprob,_hfq,_hqone,_hf,_hflp,_hfglp,_hρlp,
    he,_hdf,_hdlog,_henergy⟩ := hdata s
  change r s=gamma.tilted (fun u => -rho s u) at hr
  change Integrable (fun u => q s u*Real.log (q s u)) gamma at he
  let _ : IsProbabilityMeasure (r s) := hprob
  have hmV : Measurable V := hV.continuous.measurable
  have hρm : Measurable (rho s) := by dsimp only [rho]; fun_prop
  have hfi : Integrable (fun u => Real.exp (-rho s u)) gamma := by
    by_contra h
    have hzero : Z s=0 := integral_undef h
    exact hZ.ne' hzero
  have hgi : Integrable (fun _ : E => Real.exp (0 : ℝ)) gamma := by
    simp only [Real.exp_zero]
    exact integrable_const _
  have hlog (u : E) : Real.log (q s u)= -rho s u-Real.log (Z s) := by
    dsimp only [q]
    rw [Real.log_div (Real.exp_ne_zero _) hZ.ne',Real.log_exp]
  have hw : Integrable (fun u => Real.exp (-rho s u) • Real.log (q s u)) gamma := by
    convert! he.const_mul (Z s) using 1
    funext u
    simp only [smul_eq_mul,q]
    field_simp [hZ.ne']
  have hlogi : Integrable (fun u => Real.log (q s u)) (r s) := by
    rw [hr]
    exact (integrable_tilted_iff hfi _).mpr hw
  have hρi : Integrable (rho s) (r s) := by
    convert! hlogi.neg.sub (integrable_const (Real.log (Z s))) using 1
    funext u
    change rho s u= -Real.log (q s u)-Real.log (Z s)
    rw [hlog]
    ring
  have hrep : (fun u : E => -rho s u-Real.log (∫ z,Real.exp (-rho s z) ∂gamma)-
      (0 : ℝ)+Real.log (∫ _ : E,Real.exp (0 : ℝ) ∂gamma))=
      (fun u => Real.log (q s u)) := by
    funext u
    simp only [Real.exp_zero,integral_const,smul_eq_mul,sub_zero]
    have hmass : gamma.real Set.univ=1 := by simp [Measure.real]
    rw [hmass,one_mul,Real.log_one,add_zero]
    exact (hlog u).symm
  have hzeroTilt : gamma.tilted (fun _ : E => (0 : ℝ))=gamma := by simp
  have hkl := AutoSamplingTheory.TechnicalLemmas.InformationTheory.TiltedKL.finite_klDiv_and_toReal_eq_integral_normalizedLogRatio
    gamma (fun u => -rho s u) (fun _ => 0) hρm.neg hfi hgi
    (by simpa only [hrep,← hr] using hlogi)
  have hkl' : _root_.InformationTheory.klDiv (r s) gamma ≠ ⊤ ∧
      (_root_.InformationTheory.klDiv (r s) gamma).toReal=
        ∫ u,Real.log (q s u) ∂r s := by
    simpa only [hzeroTilt,← hr,hrep] using hkl
  have hae := AutoSamplingTheory.TechnicalLemmas.InformationTheory.TiltedLogRatio.llr_tilted_tilted_ae
    gamma (fun u => -rho s u) (fun _ => 0) hρm.neg hfi hgi
  have hae' : MeasureTheory.llr (r s) gamma =ᵐ[r s] (fun u => Real.log (q s u)) := by
    simpa only [hzeroTilt,← hr,hrep] using hae
  have hac : r s ≪ gamma := by rw [hr]; exact tilted_absolutelyContinuous _ _
  have hwint : (∫ u,Real.log (q s u) ∂r s)=
      (∫ u,q s u*Real.log (q s u) ∂gamma) := by
    rw [hr,integral_tilted]
    rfl
  have hentropy : (∫ u,Real.log (q s u) ∂r s)=
      -(∫ u,rho s u ∂r s)-Real.log (Z s) := by
    calc
      _=(∫ u,-rho s u-Real.log (Z s) ∂r s) := integral_congr_ae (Filter.Eventually.of_forall hlog)
      _=_ := by
        have hn : Integrable (fun u : E => -rho s u) (r s) := hρi.neg
        have hc : Integrable (fun _ : E => Real.log (Z s)) (r s) := integrable_const _
        rw [integral_sub hn hc,integral_neg,integral_const]
        simp [Measure.real]
  exact ⟨hac,hkl'.1,hlogi.congr hae'.symm,hae',hρi,
    hkl'.2.trans hwint,hkl'.2.trans hentropy⟩

end
end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGORelativeEntropy
