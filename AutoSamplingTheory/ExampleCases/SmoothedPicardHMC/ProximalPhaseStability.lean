import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ImplementedPhaseKernel
import AutoSamplingTheory.TechnicalLemmas.Analysis.MonotoneProximalMap
import AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoMomentum
import AutoSamplingTheory.TechnicalLemmas.Measure.Transport
import Mathlib.Analysis.SpecialFunctions.Pow.NNReal

/-! Source D1/D2: same-Gaussian comparison of the genuine exact-proximal and
approximate-proximal stochastic-gradient phases. The phase-space cost below is
Euclidean sqrt(||DX||^2+||DP||^2), not the default product max norm.
No deterministic smoothed-force identification or repeated-phase claim. -/
noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped BigOperators NNReal ENNReal
namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ProximalPhaseStability

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

private def phaseMap {J : ℕ} (g f : E → E) (eta h : ℝ) (t : Fin J → ℝ)
    (omega : Fin J → Fin J → ℝ) (pw bw : Fin J → ℝ)
    (w : (E × E) × ((E × E) × ((Fin J → E) × (Fin J → E)))) : E × E :=
  let a := Real.exp (-h/2)
  let sigma := Real.sqrt (1-Real.exp (-h))
  let P0 := a • w.1.2 + sigma • w.2.1.1
  let Y0 := fun i => w.1.1 + t i • P0
  let Z0 := fun j => g (f (Y0 j) + Real.sqrt eta • w.2.2.1 j)
  let Y1 := fun i => Y0 i - ∑ j, omega i j • Z0 j
  let Z1 := fun j => g (f (Y1 j) + Real.sqrt eta • w.2.2.2 j)
  (w.1.1 + h • P0 - ∑ j, pw j • Z1 j,
    a • (P0 - ∑ j, bw j • Z1 j) + sigma • w.2.1.2)

private theorem weighted_difference_le {J : ℕ} (a : Fin J → ℝ)
    (x y : Fin J → E) {D : ℝ} (hxy : ∀ j, ‖x j-y j‖ ≤ D) :
    ‖(∑ j, a j • x j)-(∑ j, a j • y j)‖ ≤ (∑ j, |a j|)*D := by
  have he : (∑ j, a j • x j)-(∑ j, a j • y j) = ∑ j, a j • (x j-y j) := by
    simp only [smul_sub,Finset.sum_sub_distrib]
  rw [he]
  calc
    _ ≤ ∑ j, ‖a j • (x j-y j)‖ := norm_sum_le _ _
    _ = ∑ j, |a j| *‖x j-y j‖ := by simp only [norm_smul,Real.norm_eq_abs]
    _ ≤ ∑ j, |a j| *D := by
      apply Finset.sum_le_sum
      intro j _
      exact mul_le_mul_of_nonneg_left (hxy j) (abs_nonneg _)
    _ = _ := (Finset.sum_mul _ _ _).symm

private theorem phase_displacement_le {J : ℕ} {g p r : E → E}
    (hg : LipschitzWith 1 g) (hp : LipschitzWith 1 p)
    {delta h Lambda : ℝ} (hd : 0 ≤ delta) (hh : 0 < h) (hL : 1 ≤ Lambda)
    (hstep : h^2*Lambda ≤ 1) (herr : ∀ y, ‖r y-p y‖ ≤ delta)
    (eta : ℝ) (t : Fin J → ℝ) (omega : Fin J → Fin J → ℝ)
    (pw bw : Fin J → ℝ)
    (hrow : ∀ i, (∑ j, |omega i j|) ≤ h^2/2*Lambda)
    (hpw : (∑ j, |pw j|) ≤ h^2/2*Lambda)
    (hbw : (∑ j, |bw j|) ≤ h*Lambda)
    (w : (E × E) × ((E × E) × ((Fin J → E) × (Fin J → E)))) :
    Real.sqrt (‖(phaseMap g r eta h t omega pw bw w).1-
      (phaseMap g p eta h t omega pw bw w).1‖^2 +
      ‖(phaseMap g r eta h t omega pw bw w).2-
        (phaseMap g p eta h t omega pw bw w).2‖^2) ≤ 3*h*Lambda*delta := by
  classical
  let S := h^2/2*Lambda
  let B := h*Lambda
  let a := Real.exp (-h/2)
  let sigma := Real.sqrt (1-Real.exp (-h))
  let P0 := a • w.1.2 + sigma • w.2.1.1
  let Y0 := fun i => w.1.1 + t i • P0
  let Z0 := fun (f : E → E) (j : Fin J) => g (f (Y0 j) + Real.sqrt eta • w.2.2.1 j)
  let Y1 := fun (f : E → E) (i : Fin J) => Y0 i - ∑ j, omega i j • Z0 f j
  let Z1 := fun (f : E → E) (j : Fin J) => g (f (Y1 f j) + Real.sqrt eta • w.2.2.2 j)
  have hg' (x y : E) : ‖g x-g y‖ ≤ ‖x-y‖ := by
    simpa only [NNReal.coe_one,one_mul,dist_eq_norm] using hg.dist_le_mul x y
  have hp' (x y : E) : ‖p x-p y‖ ≤ ‖x-y‖ := by
    simpa only [NNReal.coe_one,one_mul,dist_eq_norm] using hp.dist_le_mul x y
  have hz0 (j : Fin J) : ‖Z0 r j-Z0 p j‖ ≤ delta := by
    have hhg := hg' (r (Y0 j)+Real.sqrt eta • w.2.2.1 j)
      (p (Y0 j)+Real.sqrt eta • w.2.2.1 j)
    simp only [add_sub_add_right_eq_sub] at hhg
    exact hhg.trans (herr (Y0 j))
  have hy1 (i : Fin J) : ‖Y1 r i-Y1 p i‖ ≤ S*delta := by
    have he : Y1 r i-Y1 p i = -((∑ j, omega i j • Z0 r j)-(∑ j, omega i j • Z0 p j)) := by
      dsimp only [Y1]
      abel
    rw [he,norm_neg]
    exact (weighted_difference_le (omega i) (Z0 r) (Z0 p) hz0).trans
      (mul_le_mul_of_nonneg_right (hrow i) hd)
  have hz1 (j : Fin J) : ‖Z1 r j-Z1 p j‖ ≤ (1+S)*delta := by
    calc
      _ ≤ ‖r (Y1 r j)-p (Y1 p j)‖ := by
        simpa only [Z1,add_sub_add_right_eq_sub] using
          hg' (r (Y1 r j)+Real.sqrt eta • w.2.2.2 j)
            (p (Y1 p j)+Real.sqrt eta • w.2.2.2 j)
      _ ≤ ‖r (Y1 r j)-p (Y1 r j)‖ + ‖p (Y1 r j)-p (Y1 p j)‖ := by
        simpa only [dist_eq_norm] using
          dist_triangle (r (Y1 r j)) (p (Y1 r j)) (p (Y1 p j))
      _ ≤ delta+S*delta := add_le_add (herr _) ((hp' _ _).trans (hy1 j))
      _ = _ := by ring
  have hS : 0 ≤ S := mul_nonneg (by positivity) (by linarith only [hL])
  have hD : 0 ≤ (1+S)*delta := mul_nonneg (by linarith only [hS]) hd
  have hx : ‖(phaseMap g r eta h t omega pw bw w).1-
      (phaseMap g p eta h t omega pw bw w).1‖ ≤ S*((1+S)*delta) := by
    have he : (phaseMap g r eta h t omega pw bw w).1-
        (phaseMap g p eta h t omega pw bw w).1 =
        -((∑ j, pw j • Z1 r j)-(∑ j, pw j • Z1 p j)) := by
      change (w.1.1+h • P0-∑ j, pw j • Z1 r j)-
        (w.1.1+h • P0-∑ j, pw j • Z1 p j) = _
      abel
    rw [he,norm_neg]
    exact (weighted_difference_le pw (Z1 r) (Z1 p) hz1).trans
      (mul_le_mul_of_nonneg_right hpw hD)
  have ha : 0 ≤ a := (Real.exp_pos _).le
  have hm : ‖(phaseMap g r eta h t omega pw bw w).2-
      (phaseMap g p eta h t omega pw bw w).2‖ ≤ a*(B*((1+S)*delta)) := by
    have he : (phaseMap g r eta h t omega pw bw w).2-
        (phaseMap g p eta h t omega pw bw w).2 =
        -(a • ((∑ j, bw j • Z1 r j)-(∑ j, bw j • Z1 p j))) := by
      change (a • (P0-∑ j, bw j • Z1 r j)+sigma • w.2.1.2)-
        (a • (P0-∑ j, bw j • Z1 p j)+sigma • w.2.1.2) = _
      module
    rw [he,norm_neg,norm_smul,Real.norm_eq_abs,abs_of_nonneg ha]
    exact mul_le_mul_of_nonneg_left ((weighted_difference_le bw (Z1 r) (Z1 p) hz1).trans
      (mul_le_mul_of_nonneg_right hbw hD)) ha
  have hh1 : h ≤ 1 := by
    have hprod : h^2 ≤ h^2*Lambda := by nlinarith only [mul_nonneg (sq_nonneg h) (by linarith only [hL] : 0 ≤ Lambda-1)]
    nlinarith only [hprod,hstep,hh]
  have hB : 0 ≤ B := mul_nonneg hh.le (by linarith only [hL])
  have hShalf : S ≤ 1/2 := by dsimp [S];nlinarith only [hstep]
  have hSB : S ≤ 1/2*B := by
    dsimp [S,B]
    nlinarith only [mul_nonneg (by nlinarith only [hh.le,hh1] : 0 ≤ h-h^2) (by linarith only [hL] : 0 ≤ Lambda)]
  have ha1 : a ≤ 1 := Real.exp_le_one_iff.mpr (by linarith only [hh])
  have hcoef : S+a*B ≤ 3/2*B := by nlinarith only [hSB,mul_le_mul_of_nonneg_right ha1 hB]
  have htotal : S*((1+S)*delta)+a*(B*((1+S)*delta)) ≤ 3*h*Lambda*delta := by
    calc
      _ = (S+a*B)*(1+S)*delta := by ring
      _ ≤ (3/2*B)*(3/2)*delta := by
        apply mul_le_mul_of_nonneg_right _ hd
        exact mul_le_mul hcoef (by linarith only [hShalf] : 1+S ≤ 3/2)
          (by linarith only [hS] : 0 ≤ 1+S) (mul_nonneg (by norm_num) hB)
      _ ≤ 3*B*delta := by nlinarith only [mul_nonneg hB hd]
      _ = _ := by dsimp [B];ring
  refine (Real.sqrt_le_iff.mpr ⟨add_nonneg (norm_nonneg _) (norm_nonneg _),?_⟩).trans
    ((add_le_add hx hm).trans htotal)
  nlinarith only [mul_nonneg (norm_nonneg ((phaseMap g r eta h t omega pw bw w).1-
    (phaseMap g p eta h t omega pw bw w).1))
    (norm_nonneg ((phaseMap g r eta h t omega pw bw w).2-
      (phaseMap g p eta h t omega pw bw w).2))]

variable [CompleteSpace E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

omit [CompleteSpace E] in
private theorem measurable_phase {J : ℕ} {g f : E → E}
    (hg : Measurable g) (hf : Measurable f) (eta h : ℝ)
    (t : Fin J → ℝ) (omega : Fin J → Fin J → ℝ) (pw bw : Fin J → ℝ) :
    Measurable (phaseMap g f eta h t omega pw bw) := by
  change Measurable (fun w => phaseMap g f eta h t omega pw bw w)
  dsimp only [phaseMap]
  fun_prop

omit [CompleteSpace E] [BorelSpace E] in
private theorem kernel_from_phase {J : ℕ}
    (γ : Measure ((E × E) × ((Fin J → E) × (Fin J → E))))
    [IsProbabilityMeasure γ]
    {Φ : (E × E) × ((E × E) × ((Fin J → E) × (Fin J → E))) → E × E}
    (hΦ : Measurable Φ) :
    ∃ K : Kernel (E × E) (E × E), IsMarkovKernel K ∧
      ∀ s, K s = γ.map (fun z => Φ (s,z)) := by
  let K := (Kernel.id ×ₖ Kernel.const (E × E) γ).map Φ
  refine ⟨K, Kernel.IsMarkovKernel.map _ hΦ, fun s => ?_⟩
  dsimp only [K]
  rw [Kernel.map_apply _ hΦ, Kernel.prod_apply, Kernel.id_apply, Kernel.const_apply,
    Measure.dirac_prod, Measure.map_map hΦ (by fun_prop)]
  rfl

omit [CompleteSpace E] in
private theorem euclidean_transport_bound {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ] {f g : Ω → E × E}
    (hf : Measurable f) (hg : Measurable g) {A : ℝ}
    (hfg : ∀ w, Real.sqrt (‖(f w).1-(g w).1‖^2+‖(f w).2-(g w).2‖^2) ≤ A)
    {rho : ℝ} (hrho : 1 ≤ rho) :
    (TechnicalLemmas.Measure.Transport.transportCost
      (fun z : (E × E) × (E × E) =>
        (ENNReal.ofReal (Real.sqrt (‖z.1.1-z.2.1‖^2+‖z.1.2-z.2.2‖^2)))^rho)
      (μ.map f) (μ.map g))^(rho⁻¹) ≤ ENNReal.ofReal A := by
  let π := μ.map (fun w => (f w,g w))
  have hπ : TechnicalLemmas.Measure.Transport.IsCoupling π (μ.map f) (μ.map g) :=
    ⟨Measure.fst_map_prodMk hg, Measure.snd_map_prodMk hf⟩
  let cost := fun z : (E × E) × (E × E) =>
    (ENNReal.ofReal (Real.sqrt (‖z.1.1-z.2.1‖^2+‖z.1.2-z.2.2‖^2)))^rho
  have hm : Measurable cost := by
    dsimp only [cost]
    exact ENNReal.continuous_rpow_const.measurable.comp (by fun_prop)
  have hb : TechnicalLemmas.Measure.Transport.transportCost cost (μ.map f) (μ.map g) ≤
      (ENNReal.ofReal A)^rho := by
    calc
      _ ≤ ∫⁻ z, cost z ∂π :=
        TechnicalLemmas.Measure.Transport.transportCost_le_lintegral_of_isCoupling
          cost _ _ π hπ
      _ = ∫⁻ w, cost (f w,g w) ∂μ := lintegral_map hm (hf.prodMk hg)
      _ ≤ ∫⁻ _w, (ENNReal.ofReal A)^rho ∂μ := by
        apply lintegral_mono
        intro w
        exact ENNReal.rpow_le_rpow (ENNReal.ofReal_le_ofReal (hfg w)) (by linarith)
      _ = _ := by simp
  have hp : 0 < rho := by linarith
  have hb' := ENNReal.rpow_le_rpow hb (inv_nonneg.mpr hp.le)
  simpa only [← ENNReal.rpow_mul,mul_inv_cancel₀ (ne_of_gt hp),ENNReal.rpow_one] using hb'


/-- Appendix D1/D2 for the genuine source-coefficient two-layer phase, with
explicit constant 3 and the Euclidean phase-space transport cost. The exact
proximal map and stopped query program are constructed for the full range
0<eta<1. Every measurable uniformly accurate oracle (including delta=0) has
an actual Markov kernel and the all-finite-q coupling bound. No repeated-phase,
deterministic smoothed-force, invariant-law, or expected-work claim is made. -/
theorem source_phase_proximal_stability {V : E → ℝ} {κ : ℝ≥0}
    (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (κ : ℝ)⁻¹ * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖ ^ 2)
    {eta eps : ℝ} (heta : 0 < eta) (heta1 : eta < 1) (heps : 0 < eps)
    {J : ℕ} (hJ : 2 ≤ J) {h : ℝ} (hh : 0 < h) :
    let t := fun i : Fin J => h/2*(1-Real.cos ((i : ℝ)/(J-1 : ℝ)*Real.pi))
    let ell := fun j : Fin J => Lagrange.basis Finset.univ t j
    let Lambda := sSup ((fun s : ℝ => ∑ j : Fin J, |(ell j).eval s|) '' Set.Icc 0 h)
    let omega := fun i j : Fin J => ∫ s in 0..t i, (t i-s)*(ell j).eval s
    let pw := omega ⟨J-1,by omega⟩
    let bw := fun j : Fin J => ∫ s in 0..h, (ell j).eval s
    h^2*Lambda ≤ 1 →
    ∃ p q : E → E, ∃ N : E → ℕ,
      Measurable p ∧ Measurable q ∧ Measurable N ∧
      (∀ y, p y + eta • gradient V (p y) = y ∧ ‖q y-p y‖ ≤ eps ∧
        ApproximateProximalExecution.proximalQuery (gradient V) eta eps y (N y+1) y =
          some (q y,N y+1)) ∧ LipschitzWith 1 p ∧
      let γ := ((stdGaussian E).prod (stdGaussian E)).prod
        ((Measure.pi (fun _ : Fin J => stdGaussian E)).prod
          (Measure.pi (fun _ : Fin J => stdGaussian E)))
      let Φ := fun (f : E → E)
          (w : (E × E) × ((E × E) × ((Fin J → E) × (Fin J → E)))) =>
        let a := Real.exp (-h/2)
        let sigma := Real.sqrt (1-Real.exp (-h))
        let P0 := a • w.1.2 + sigma • w.2.1.1
        let Y0 := fun i => w.1.1+t i • P0
        let Z0 := fun j => gradient V (f (Y0 j)+Real.sqrt eta • w.2.2.1 j)
        let Y1 := fun i => Y0 i-∑ j, omega i j • Z0 j
        let Z1 := fun j => gradient V (f (Y1 j)+Real.sqrt eta • w.2.2.2 j)
        (w.1.1+h • P0-∑ j, pw j • Z1 j,
          a • (P0-∑ j, bw j • Z1 j)+sigma • w.2.1.2)
      let W := fun (rho : ℝ) (μ ν : Measure (E × E)) =>
        (TechnicalLemmas.Measure.Transport.transportCost
          (fun z : (E × E) × (E × E) =>
            (ENNReal.ofReal (Real.sqrt (‖z.1.1-z.2.1‖^2+‖z.1.2-z.2.2‖^2)))^rho)
          μ ν)^(rho⁻¹)
      ∃ Kp Kq : Kernel (E × E) (E × E),
        IsMarkovKernel Kp ∧ IsMarkovKernel Kq ∧
        (∀ s, Kp s = γ.map (fun z => Φ p (s,z))) ∧
        (∀ s, Kq s = γ.map (fun z => Φ q (s,z))) ∧
        (∀ s rho, 1 ≤ rho → W rho (Kq s) (Kp s) ≤ ENNReal.ofReal (3*h*Lambda*eps)) ∧
        (∀ (r : E → E), Measurable r → ∀ delta : ℝ, 0 ≤ delta →
          (∀ y, ‖r y-p y‖ ≤ delta) →
          ∃ Kr : Kernel (E × E) (E × E), IsMarkovKernel Kr ∧
            (∀ s, Kr s = γ.map (fun z => Φ r (s,z))) ∧
            ∀ s rho, 1 ≤ rho → W rho (Kr s) (Kp s) ≤
              ENNReal.ofReal (3*h*Lambda*delta)) := by
  classical
  dsimp only
  intro hstep
  let t := fun i : Fin J => h/2*(1-Real.cos ((i : ℝ)/(J-1 : ℝ)*Real.pi))
  let ell := fun j : Fin J => Lagrange.basis Finset.univ t j
  let Lambda := sSup ((fun s : ℝ => ∑ j : Fin J, |(ell j).eval s|) '' Set.Icc 0 h)
  let omega := fun i j : Fin J => ∫ s in 0..t i, (t i-s)*(ell j).eval s
  let pw := omega ⟨J-1,by omega⟩
  let bw := fun j : Fin J => ∫ s in 0..h, (ell j).eval s
  obtain ⟨p,q,N,hp,hq,hN,hall,_,hΦq,Kq,hKq,hKqpush⟩ :=
    ImplementedPhaseKernel.implemented_phase_kernel hκ hV hH heta
      (le_refl eta) heta1 heps h hh.le t omega pw bw
  have hg : Measurable (gradient V) := by
    unfold gradient
    exact ((InnerProductSpace.toDual ℝ E).symm.continuous.comp
      (hV.continuous_fderiv (by norm_num))).measurable
  have hH' : ∀ x v : E, ((κ⁻¹ : ℝ≥0) : ℝ)*‖v‖^2 ≤
      (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (1 : ℝ≥0)*‖v‖^2 := by
    simpa only [NNReal.coe_inv,NNReal.coe_one,one_mul] using hH
  have hreg :=
    TechnicalLemmas.Analysis.QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic
      (r := 0) hV hH' (0 : E)
  have hLip : LipschitzWith 1 (gradient V) := by simpa using hreg.2
  have hsc : StrongConvexOn Set.univ ((κ : ℝ)⁻¹) V := by simpa using hreg.1
  have hmono (x y : E) : 0 ≤ inner ℝ (gradient V x-gradient V y) (x-y) := by
    have hb :=
      TechnicalLemmas.Analysis.StrongConvexFirstOrder.gradient_inner_lower_bound_of_strongConvexOn hsc
        (fun z _ => (hV.differentiable (by norm_num) z).hasGradientAt)
        (x := y) (y := x) (Set.mem_univ _) (Set.mem_univ _)
    exact (mul_nonneg (inv_nonneg.mpr (NNReal.coe_nonneg κ)) (sq_nonneg _)).trans hb
  have hpLip := TechnicalLemmas.Analysis.MonotoneProximalMap.nonexpansive_of_monotone_optimality
    heta.le hmono (fun y => (hall y).1)
  have hcoeff := TechnicalLemmas.Analysis.ChebyshevLobattoQuadrature.chebyshev_lobatto_coefficients hJ hh
  have hL : 1 ≤ Lambda := hcoeff.2.2.2.2.2.1
  have hrow : ∀ i, (∑ j, |omega i j|) ≤ h^2/2*Lambda := fun i =>
    (hcoeff.2.2.2.2.2.2.1 i).2
  have hpw : (∑ j, |pw j|) ≤ h^2/2*Lambda := hrow _
  have hbw : (∑ j, |bw j|) ≤ h*Lambda :=
    TechnicalLemmas.Analysis.ChebyshevLobattoMomentum.momentum_absolute_sum_le hJ hh
  let γ := ((stdGaussian E).prod (stdGaussian E)).prod
    ((Measure.pi (fun _ : Fin J => stdGaussian E)).prod
      (Measure.pi (fun _ : Fin J => stdGaussian E)))
  let Φ := fun f => phaseMap (gradient V) f eta h t omega pw bw
  have hΦ (f : E → E) (hf : Measurable f) : Measurable (Φ f) :=
    measurable_phase hg hf eta h t omega pw bw
  obtain ⟨Kp,hKp,hKppush⟩ := kernel_from_phase γ (hΦ p hp)
  refine ⟨p,q,N,hp,hq,hN,hall,hpLip,Kp,Kq,hKp,hKq,hKppush,hKqpush,?_,?_⟩
  · intro state rho hrho
    rw [hKqpush state,hKppush state]
    apply euclidean_transport_bound γ ((hΦ q hq).comp (by fun_prop))
      ((hΦ p hp).comp (by fun_prop)) _ hrho
    intro z
    exact phase_displacement_le hLip hpLip heps.le hh hL hstep
      (fun y => (hall y).2.1) eta t omega pw bw hrow hpw hbw (state,z)
  · intro r hr delta hd herr
    obtain ⟨Kr,hKr,hKrpush⟩ := kernel_from_phase γ (hΦ r hr)
    refine ⟨Kr,hKr,hKrpush,fun state rho hrho => ?_⟩
    rw [hKrpush state,hKppush state]
    apply euclidean_transport_bound γ ((hΦ r hr).comp (by fun_prop))
      ((hΦ p hp).comp (by fun_prop)) _ hrho
    intro z
    exact phase_displacement_le hLip hpLip hd hh hL hstep herr
      eta t omega pw bw hrow hpw hbw (state,z)

end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ProximalPhaseStability
