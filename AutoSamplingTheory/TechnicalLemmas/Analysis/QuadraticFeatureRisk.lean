import Mathlib.Algebra.BigOperators.Group.Finset.Piecewise
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Measure.Prod
import Mathlib.Tactic.GCongr
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
# Quadratic feature risks, empirical laws and replacement budgets

This module collects real Hilbert-space squared-loss calculus and its literal
scalar-integral realizations. Finite empirical laws retain repeated atoms.
The joint-data result uses the true input marginal, proves the actual potential
pairing, and obtains the exact predictor-square remainder and positive budget.

The integral-mean theorem is a separate reusable interface: its feature is
Bochner integrable under both measures. Its affine Hilbert derivative is not
by itself a first variation along a probability-measure segment. The finite
empirical theorem does not require global measurability in the parameter;
non-atomic parameter-law averaging needs a separate measurability argument.
-/

open MeasureTheory
open scoped ENNReal InnerProductSpace

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticFeatureRisk

theorem empirical_squared_feature_risk_derivatives
    {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    {N : ℕ} (hN : 0 < N) (lambda : ℝ)
    {phi : ℝ → H} {v a y : H} {t : ℝ} (hphi : HasDerivAt phi v t) :
    HasDerivAt (fun s => ‖(N : ℝ)⁻¹ • (a + phi s) - y‖ ^ 2)
      ((2 / (N : ℝ)) * ⟪(N : ℝ)⁻¹ • (a + phi t) - y, v⟫_ℝ) t ∧
    HasDerivAt (fun s => ((N : ℝ) / lambda) * ‖(N : ℝ)⁻¹ • (a + phi s) - y‖ ^ 2)
      ((2 / lambda) * ⟪(N : ℝ)⁻¹ • (a + phi t) - y, v⟫_ℝ) t := by
  have hNr : (N : ℝ) ≠ 0 := by exact_mod_cast hN.ne'
  have hsum : HasDerivAt (fun s => a + phi s) v t := hphi.const_add a
  have hmean : HasDerivAt (fun s => (N : ℝ)⁻¹ • (a + phi s)) ((N : ℝ)⁻¹ • v) t :=
    HasDerivAt.const_smul (N : ℝ)⁻¹ hsum
  have hcurve : HasDerivAt (fun s => (N : ℝ)⁻¹ • (a + phi s) - y) ((N : ℝ)⁻¹ • v) t :=
    hmean.sub_const y
  have hsq : HasDerivAt (fun s => ‖(N : ℝ)⁻¹ • (a + phi s) - y‖ ^ 2)
      ((2 / (N : ℝ)) * ⟪(N : ℝ)⁻¹ • (a + phi t) - y, v⟫_ℝ) t := by
    simpa only [real_inner_smul_right, div_eq_mul_inv, mul_assoc] using hcurve.norm_sq
  have hcancel : ((N : ℝ) / lambda) *
        ((2 / (N : ℝ)) * ⟪(N : ℝ)⁻¹ • (a + phi t) - y, v⟫_ℝ) =
      (2 / lambda) * ⟪(N : ℝ)⁻¹ • (a + phi t) - y, v⟫_ℝ := by
    simp only [div_eq_mul_inv]
    calc
      (N : ℝ) * lambda⁻¹ * (2 * (N : ℝ)⁻¹ * ⟪(N : ℝ)⁻¹ • (a + phi t) - y, v⟫_ℝ) =
          ((N : ℝ) * (N : ℝ)⁻¹) *
            (2 * lambda⁻¹ * ⟪(N : ℝ)⁻¹ • (a + phi t) - y, v⟫_ℝ) := by ring
      _ = 2 * lambda⁻¹ * ⟪(N : ℝ)⁻¹ • (a + phi t) - y, v⟫_ℝ := by
        rw [mul_inv_cancel₀ hNr, one_mul]
  have hscaled := HasDerivAt.const_mul ((N : ℝ) / lambda) hsq
  rw [hcancel] at hscaled
  exact ⟨hsq, hscaled⟩

theorem empirical_squared_risk_eq_L2_norm
    {Omega : Type*} [MeasurableSpace Omega] (mu : Measure Omega) (N : ℕ)
    (feature : Fin N → Omega → ℝ) (label : Omega → ℝ)
    (hfeature : ∀ i, MemLp (feature i) 2 mu) (hlabel : MemLp label 2 mu) :
    Integrable (fun omega => ((N : ℝ)⁻¹ * ∑ i, feature i omega - label omega) ^ 2) mu ∧
    (∫ omega, ((N : ℝ)⁻¹ * ∑ i, feature i omega - label omega) ^ 2 ∂mu) =
      ‖(N : ℝ)⁻¹ • ∑ i, (hfeature i).toLp (feature i) - hlabel.toLp label‖ ^ 2 := by
  classical
  let z : Lp ℝ 2 mu :=
    (N : ℝ)⁻¹ • ∑ i, (hfeature i).toLp (feature i) - hlabel.toLp label
  have hres : MemLp (fun omega => (N : ℝ)⁻¹ * ∑ i, feature i omega - label omega) 2 mu := by
    have hs := memLp_finsetSum Finset.univ (fun i _ => hfeature i)
    exact (hs.const_smul (N : ℝ)⁻¹).sub hlabel
  refine ⟨hres.integrable_sq, ?_⟩
  have hz : (fun omega => z omega) =ᵐ[mu]
      (fun omega => (N : ℝ)⁻¹ * ∑ i, feature i omega - label omega) := by
    filter_upwards [Lp.coeFn_sub ((N : ℝ)⁻¹ • ∑ i, (hfeature i).toLp (feature i))
        (hlabel.toLp label),
      Lp.coeFn_smul (N : ℝ)⁻¹ (∑ i, (hfeature i).toLp (feature i)),
      Lp.coeFn_fun_finsetSum Finset.univ (fun i => (hfeature i).toLp (feature i)),
      ae_all_iff.2 (fun i => (hfeature i).coeFn_toLp), hlabel.coeFn_toLp]
      with omega hsub hsmul hsum hf hy
    change (((N : ℝ)⁻¹ • ∑ i, (hfeature i).toLp (feature i) - hlabel.toLp label) omega) = _
    simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul] at hsub hsmul
    rw [hsub, hsmul, hsum, hy]
    simp only [hf]
  change (∫ omega, ((N : ℝ)⁻¹ * ∑ i, feature i omega - label omega) ^ 2 ∂mu) = ‖z‖ ^ 2
  rw [← real_inner_self_eq_norm_sq, L2.inner_def]
  symm
  apply integral_congr_ae
  filter_upwards [hz] with omega homega
  simp only [homega, real_inner_self_eq_norm_sq, Real.norm_eq_abs, sq_abs]

theorem empirical_law_squared_risk_eq_L2_norm
    {W Omega : Type*} [MeasurableSpace W] [MeasurableSingletonClass W]
    [MeasurableSpace Omega] (P : Measure Omega) {N : ℕ} (hN : 0 < N)
    (w : Fin N → W) (K : W → Omega → ℝ) (label : Omega → ℝ)
    (hfeature : ∀ i, MemLp (K (w i)) 2 P) (hlabel : MemLp label 2 P) :
    let rho : Measure W := (N : ℝ≥0∞)⁻¹ • ∑ i, Measure.dirac (w i)
    IsProbabilityMeasure rho ∧
    Integrable (fun omega => ((∫ q, K q omega ∂rho) - label omega) ^ 2) P ∧
    (∫ omega, ((∫ q, K q omega ∂rho) - label omega) ^ 2 ∂P) =
      ‖(N : ℝ)⁻¹ • ∑ i, (hfeature i).toLp (K (w i)) - hlabel.toLp label‖ ^ 2 := by
  classical
  dsimp only
  let rho : Measure W := (N : ℝ≥0∞)⁻¹ • ∑ i, Measure.dirac (w i)
  have hprob : IsProbabilityMeasure rho := by
    constructor
    simpa [rho, Measure.smul_apply] using
      ENNReal.inv_mul_cancel (show (N : ℝ≥0∞) ≠ 0 by exact_mod_cast hN.ne') (by simp)
  have hpred : ∀ omega, (∫ q, K q omega ∂rho) = (N : ℝ)⁻¹ * ∑ i, K (w i) omega := by
    intro omega
    change (∫ q, K q omega ∂((N : ℝ≥0∞)⁻¹ • ∑ i, Measure.dirac (w i))) = _
    rw [integral_smul_measure]
    rw [integral_finsetSum_measure (fun i _ => integrable_dirac (by simp))]
    simp [smul_eq_mul]
  have hbase := empirical_squared_risk_eq_L2_norm P N
    (fun i => K (w i)) label hfeature hlabel
  refine ⟨hprob, ?_, ?_⟩
  · change Integrable (fun omega => ((∫ q, K q omega ∂rho) - label omega) ^ 2) P
    simpa only [hpred] using hbase.1
  · change (∫ omega, ((∫ q, K q omega ∂rho) - label omega) ^ 2 ∂P) = _
    simpa only [hpred] using hbase.2

theorem empirical_squared_loss_replacement
    {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    {N : ℕ} (hN : 0 < N) (feature : Fin N → H) (i : Fin N)
    (replacement label : H) (b : ℝ)
    (hold : ‖feature i‖ ≤ b) (hnew : ‖replacement‖ ≤ b) :
    let m : H := (N : ℝ)⁻¹ • ∑ j, feature j
    let mNew : H := (N : ℝ)⁻¹ • ∑ j, Function.update feature i replacement j
    (‖mNew - label‖ ^ 2 - ‖m - label‖ ^ 2 -
      2 * ⟪m - label, mNew - m⟫_ℝ = ‖mNew - m‖ ^ 2) ∧
    ‖mNew - m‖ ^ 2 ≤ 4 * b ^ 2 / (N : ℝ) ^ 2 := by
  classical
  dsimp only
  let m : H := (N : ℝ)⁻¹ • ∑ j, feature j
  let mNew : H := (N : ℝ)⁻¹ • ∑ j, Function.update feature i replacement j
  change (‖mNew - label‖ ^ 2 - ‖m - label‖ ^ 2 -
      2 * ⟪m - label, mNew - m⟫_ℝ = ‖mNew - m‖ ^ 2) ∧ _
  have hsum : (∑ j, Function.update feature i replacement j) - ∑ j, feature j =
      replacement - feature i := by
    rw [← Finset.sum_sub_distrib, Finset.sum_eq_single i]
    · simp
    · intro j _ hji
      simp [Function.update_of_ne hji]
    · simp
  have hmean : mNew - m = (N : ℝ)⁻¹ • (replacement - feature i) := by
    dsimp only [mNew, m]
    rw [← smul_sub, hsum]
  have hb : 0 ≤ b := (norm_nonneg (feature i)).trans hold
  have hinv : 0 ≤ (N : ℝ)⁻¹ := (inv_pos.mpr (show (0 : ℝ) < N by exact_mod_cast hN)).le
  have hsmall : ‖mNew - m‖ ≤ (N : ℝ)⁻¹ * (2 * b) := by
    rw [hmean, norm_smul, Real.norm_eq_abs, abs_of_nonneg hinv]
    apply mul_le_mul_of_nonneg_left _ hinv
    calc
      ‖replacement - feature i‖ ≤ ‖replacement‖ + ‖feature i‖ := norm_sub_le _ _
      _ ≤ b + b := add_le_add hnew hold
      _ = 2 * b := by ring
  constructor
  · have hsplit : mNew - label = (m - label) + (mNew - m) := by abel
    rw [hsplit, norm_add_sq_real]
    ring
  · calc
      ‖mNew - m‖ ^ 2 ≤ ((N : ℝ)⁻¹ * (2 * b)) ^ 2 := by gcongr
      _ = 4 * b ^ 2 / (N : ℝ) ^ 2 := by
        simp only [div_eq_mul_inv]
        ring

theorem quadratic_feature_mean_calculus
    {W H : Type*} [MeasurableSpace W]
    [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    (μ ν : Measure W) (feature : W → H) (label : H)
    (hμ : Integrable feature μ) (hν : Integrable feature ν) :
    let m : H := ∫ w, feature w ∂μ
    let n : H := ∫ w, feature w ∂ν
    let potential : W → ℝ := fun w => 2 * ⟪m - label, feature w⟫_ℝ
    Integrable potential μ ∧ Integrable potential ν ∧
    ((∫ w, potential w ∂ν) - (∫ w, potential w ∂μ) =
      2 * ⟪m - label, n - m⟫_ℝ) ∧
    (‖n - label‖ ^ 2 - ‖m - label‖ ^ 2 -
      ((∫ w, potential w ∂ν) - (∫ w, potential w ∂μ)) = ‖n - m‖ ^ 2) ∧
    (‖m - label‖ ^ 2 + ((∫ w, potential w ∂ν) - (∫ w, potential w ∂μ)) ≤
      ‖n - label‖ ^ 2) ∧
    HasDerivAt (fun t : ℝ => ‖m + t • (n - m) - label‖ ^ 2)
      ((∫ w, potential w ∂ν) - (∫ w, potential w ∂μ)) 0 := by
  dsimp only
  let m : H := ∫ w, feature w ∂μ
  let n : H := ∫ w, feature w ∂ν
  let potential : W → ℝ := fun w => 2 * ⟪m - label, feature w⟫_ℝ
  change Integrable potential μ ∧ Integrable potential ν ∧ _
  have hpotμ : Integrable potential μ :=
    (Integrable.const_inner (m - label) hμ).const_mul 2
  have hpotν : Integrable potential ν :=
    (Integrable.const_inner (m - label) hν).const_mul 2
  have hpμ : (∫ w, potential w ∂μ) = 2 * ⟪m - label, m⟫_ℝ := by
    dsimp only [potential, m]
    rw [integral_const_mul, integral_inner hμ]
  have hpν : (∫ w, potential w ∂ν) = 2 * ⟪m - label, n⟫_ℝ := by
    dsimp only [potential, n]
    rw [integral_const_mul, integral_inner hν]
  have hpair : (∫ w, potential w ∂ν) - (∫ w, potential w ∂μ) =
      2 * ⟪m - label, n - m⟫_ℝ := by
    rw [hpν, hpμ, inner_sub_right]
    ring
  have hbre : ‖n - label‖ ^ 2 - ‖m - label‖ ^ 2 -
      ((∫ w, potential w ∂ν) - (∫ w, potential w ∂μ)) = ‖n - m‖ ^ 2 := by
    rw [hpair]
    have hsplit : n - label = (m - label) + (n - m) := by abel
    rw [hsplit, norm_add_sq_real]
    ring
  refine ⟨hpotμ, hpotν, hpair, hbre, ?_, ?_⟩
  · linarith [sq_nonneg ‖n - m‖]
  · rw [hpair]
    have hcurve : HasDerivAt (fun t : ℝ => m + t • (n - m) - label) (n - m) 0 := by
      have hsmul : HasDerivAt (fun t : ℝ => t • (n - m)) (n - m) 0 := by
        simpa only [one_smul, id_eq] using (hasDerivAt_id (0 : ℝ)).smul_const (n - m)
      have hadd : HasDerivAt (fun t : ℝ => m + t • (n - m)) (n - m) 0 :=
        hsmul.const_add m
      exact hadd.sub_const label
    simpa only [zero_smul, add_zero] using hcurve.norm_sq

theorem joint_empirical_squared_risk_replacement
    {W X : Type*} [MeasurableSpace W] [MeasurableSingletonClass W]
    [MeasurableSpace X] (P : Measure (X × ℝ)) [IsProbabilityMeasure P]
    (K : W → X → ℝ) (b : ℝ) (hb : 0 < b)
    (hfeature : ∀ q, MemLp (K q) 2 (P.map Prod.fst))
    (hbound : ∀ q, ‖(hfeature q).toLp (K q)‖ ≤ b)
    (hlabel : MemLp (fun z : X × ℝ => z.2) 2 P)
    {N : ℕ} (hN : 0 < N) (w : Fin N → W) (i : Fin N) (u : W) :
    let rho : Measure W := (N : ℝ≥0∞)⁻¹ • ∑ j, Measure.dirac (w j)
    let rhoNew : Measure W :=
      (N : ℝ≥0∞)⁻¹ • ∑ j, Measure.dirac (Function.update w i u j)
    let predictor : Measure W → X → ℝ := fun law x => ∫ q, K q x ∂law
    let risk : Measure W → ℝ :=
      fun law => ∫ z, (predictor law z.1 - z.2) ^ 2 ∂P
    let potential : W → ℝ :=
      fun q => 2 * ∫ z, (predictor rho z.1 - z.2) * K q z.1 ∂P
    let pairing : ℝ := (∫ q, potential q ∂rhoNew) - (∫ q, potential q ∂rho)
    (0 < 4 * b ^ 2) ∧ IsProbabilityMeasure rho ∧ IsProbabilityMeasure rhoNew ∧
    Integrable (fun z : X × ℝ => (predictor rho z.1 - z.2) ^ 2) P ∧
    Integrable (fun z : X × ℝ => (predictor rhoNew z.1 - z.2) ^ 2) P ∧
    Integrable potential rho ∧ Integrable potential rhoNew ∧
    (pairing = (N : ℝ)⁻¹ * (potential u - potential (w i))) ∧
    (risk rhoNew - risk rho - pairing =
      ∫ x, (predictor rhoNew x - predictor rho x) ^ 2 ∂(P.map Prod.fst)) ∧
    (0 ≤ risk rhoNew - risk rho - pairing) ∧
    (risk rhoNew - risk rho - pairing ≤ 4 * b ^ 2 / (N : ℝ) ^ 2) := by
  classical
  dsimp only
  let rhoOf : (Fin N → W) → Measure W :=
    fun cfg => (N : ℝ≥0∞)⁻¹ • ∑ j, Measure.dirac (cfg j)
  let cfgNew := Function.update w i u
  let predictor : Measure W → X → ℝ := fun law x => ∫ q, K q x ∂law
  let risk : Measure W → ℝ := fun law => ∫ z, (predictor law z.1 - z.2) ^ 2 ∂P
  let potential : W → ℝ :=
    fun q => 2 * ∫ z, (predictor (rhoOf w) z.1 - z.2) * K q z.1 ∂P
  let pairing : ℝ := (∫ q, potential q ∂rhoOf cfgNew) - (∫ q, potential q ∂rhoOf w)
  change (0 < 4 * b ^ 2) ∧ IsProbabilityMeasure (rhoOf w) ∧
    IsProbabilityMeasure (rhoOf cfgNew) ∧ _
  have hmarg : MeasurePreserving (Prod.fst : X × ℝ → X) P (P.map Prod.fst) :=
    measurable_fst.measurePreserving P
  have hfeatureP (q : W) : MemLp (fun z : X × ℝ => K q z.1) 2 P :=
    (hfeature q).comp_measurePreserving hmarg
  let feature : W → Lp ℝ 2 P :=
    fun q => (hfeatureP q).toLp (fun z : X × ℝ => K q z.1)
  let label : Lp ℝ 2 P := hlabel.toLp (fun z : X × ℝ => z.2)
  let mean : (Fin N → W) → Lp ℝ 2 P :=
    fun cfg => (N : ℝ)⁻¹ • ∑ j, feature (cfg j)
  have hfeatureClass (q : W) : feature q =
      Lp.compMeasurePreserving Prod.fst hmarg ((hfeature q).toLp (K q)) := rfl
  have hnorm (q : W) : ‖feature q‖ ≤ b := by
    rw [hfeatureClass, Lp.norm_compMeasurePreserving]
    exact hbound q
  have hinv : (N : ℝ≥0∞)⁻¹ ≠ ∞ := by
    apply ENNReal.inv_ne_top.mpr
    exact_mod_cast hN.ne'
  have hInt (cfg : Fin N → W) (g : W → ℝ) :
      Integrable g (rhoOf cfg) := by
    apply Integrable.smul_measure (c := (N : ℝ≥0∞)⁻¹) _ hinv
    exact integrable_finsetSum_measure.mpr (fun j _ => integrable_dirac (by simp))
  have hEval (cfg : Fin N → W) (g : W → ℝ) :
      (∫ q, g q ∂rhoOf cfg) = (N : ℝ)⁻¹ * ∑ j, g (cfg j) := by
    dsimp only [rhoOf]
    rw [integral_smul_measure,
      integral_finsetSum_measure (fun j _ => integrable_dirac (by simp))]
    simp [smul_eq_mul]
  have hPred (cfg : Fin N → W) (x : X) :
      predictor (rhoOf cfg) x = (N : ℝ)⁻¹ * ∑ j, K (cfg j) x :=
    hEval cfg (fun q => K q x)
  have hBase (cfg : Fin N → W) :=
    empirical_law_squared_risk_eq_L2_norm P hN cfg
      (fun q z => K q z.1) (fun z => z.2) (fun j => hfeatureP (cfg j)) hlabel
  have hRisk (cfg : Fin N → W) : risk (rhoOf cfg) = ‖mean cfg - label‖ ^ 2 := by
    simpa only [risk, predictor, rhoOf, mean, feature, label] using (hBase cfg).2.2
  have hMean (cfg : Fin N → W) :
      (fun z => mean cfg z) =ᵐ[P] (fun z : X × ℝ => predictor (rhoOf cfg) z.1) := by
    filter_upwards [Lp.coeFn_smul (N : ℝ)⁻¹ (∑ j, feature (cfg j)),
      Lp.coeFn_fun_finsetSum Finset.univ (fun j => feature (cfg j)),
      ae_all_iff.2 (fun j => (hfeatureP (cfg j)).coeFn_toLp)]
      with z hsmul hsum hf
    change (((N : ℝ)⁻¹ • ∑ j, feature (cfg j)) z) = _
    simp only [Pi.smul_apply, smul_eq_mul] at hsmul
    rw [hsmul, hsum, hPred]
    congr 1
    apply Finset.sum_congr rfl
    intro j _
    exact hf j
  have hResidual : (fun z => (mean w - label) z) =ᵐ[P]
      (fun z : X × ℝ => predictor (rhoOf w) z.1 - z.2) := by
    filter_upwards [Lp.coeFn_sub (mean w) label, hMean w, hlabel.coeFn_toLp]
      with z hsub hm hy
    simp only [Pi.sub_apply] at hsub
    rw [hsub, hm, hy]
  have hPotential (q : W) : potential q = 2 * ⟪mean w - label, feature q⟫_ℝ := by
    dsimp only [potential]
    rw [L2.inner_def]
    congr 1
    apply integral_congr_ae
    filter_upwards [hResidual, (hfeatureP q).coeFn_toLp] with z hr hq
    change feature q z = K q z.1 at hq
    simp only [Real.inner_apply, hr, hq]
  have hPotMean (cfg : Fin N → W) :
      (∫ q, potential q ∂rhoOf cfg) = 2 * ⟪mean w - label, mean cfg⟫_ℝ := by
    rw [hEval]
    simp_rw [hPotential]
    dsimp only [mean]
    rw [real_inner_smul_right, inner_sum, ← Finset.mul_sum]
    ring
  have hPair : pairing = 2 * ⟪mean w - label, mean cfgNew - mean w⟫_ℝ := by
    dsimp only [pairing]
    rw [hPotMean, hPotMean, inner_sub_right]
    ring
  have hUpdate : (fun j => feature (cfgNew j)) =
      Function.update (fun j => feature (w j)) i (feature u) := by
    funext j
    by_cases hji : j = i
    · subst j
      simp [cfgNew]
    · simp [cfgNew, Function.update_of_ne hji]
  have hBudget := empirical_squared_loss_replacement hN
    (fun j => feature (w j)) i (feature u) label b (hnorm (w i)) (hnorm u)
  change (‖(N : ℝ)⁻¹ • ∑ j, Function.update (fun j => feature (w j)) i (feature u) j - label‖ ^ 2 -
      ‖mean w - label‖ ^ 2 -
      2 * ⟪mean w - label,
        (N : ℝ)⁻¹ • ∑ j, Function.update (fun j => feature (w j)) i (feature u) j - mean w⟫_ℝ =
      ‖(N : ℝ)⁻¹ • ∑ j, Function.update (fun j => feature (w j)) i (feature u) j - mean w‖ ^ 2) ∧ _ at hBudget
  rw [← hUpdate] at hBudget
  change (‖mean cfgNew - label‖ ^ 2 - ‖mean w - label‖ ^ 2 -
      2 * ⟪mean w - label, mean cfgNew - mean w⟫_ℝ = ‖mean cfgNew - mean w‖ ^ 2) ∧
    ‖mean cfgNew - mean w‖ ^ 2 ≤ 4 * b ^ 2 / (N : ℝ) ^ 2 at hBudget
  have hBre : risk (rhoOf cfgNew) - risk (rhoOf w) - pairing =
      ‖mean cfgNew - mean w‖ ^ 2 := by
    rw [hRisk, hRisk, hPair]
    exact hBudget.1
  have hMeanDiff : (fun z => (mean cfgNew - mean w) z) =ᵐ[P]
      (fun z : X × ℝ => predictor (rhoOf cfgNew) z.1 - predictor (rhoOf w) z.1) := by
    filter_upwards [Lp.coeFn_sub (mean cfgNew) (mean w), hMean cfgNew, hMean w]
      with z hsub hn hm
    simp only [Pi.sub_apply] at hsub
    rw [hsub, hn, hm]
  have hPredLp (cfg : Fin N → W) : MemLp (predictor (rhoOf cfg)) 2 (P.map Prod.fst) := by
    have havg := (memLp_finsetSum Finset.univ (fun j _ => hfeature (cfg j))).const_smul (N : ℝ)⁻¹
    exact MemLp.ae_eq (Filter.Eventually.of_forall (fun x => (hPred cfg x).symm)) havg
  have hDiffLp := (hPredLp cfgNew).sub (hPredLp w)
  have hNormInt : ‖mean cfgNew - mean w‖ ^ 2 =
      ∫ x, (predictor (rhoOf cfgNew) x - predictor (rhoOf w) x) ^ 2 ∂(P.map Prod.fst) := by
    rw [← real_inner_self_eq_norm_sq, L2.inner_def]
    calc
      (∫ z, ⟪(mean cfgNew - mean w) z, (mean cfgNew - mean w) z⟫_ℝ ∂P) =
          ∫ z : X × ℝ, (predictor (rhoOf cfgNew) z.1 - predictor (rhoOf w) z.1) ^ 2 ∂P := by
        apply integral_congr_ae
        filter_upwards [hMeanDiff] with z hz
        simp only [Real.inner_apply, hz, pow_two]
      _ = _ := (integral_map measurable_fst.aemeasurable hDiffLp.integrable_sq.aestronglyMeasurable).symm
  have hPairUpdate : pairing = (N : ℝ)⁻¹ * (potential u - potential (w i)) := by
    dsimp only [pairing]
    rw [hEval, hEval, ← mul_sub, ← Finset.sum_sub_distrib, Finset.sum_eq_single i]
    · simp [cfgNew]
    · intro j _ hji
      simp [cfgNew, Function.update_of_ne hji]
    · simp
  refine ⟨mul_pos (by norm_num) (sq_pos_of_pos hb), (hBase w).1, (hBase cfgNew).1,
    (hBase w).2.1, (hBase cfgNew).2.1, hInt w potential, hInt cfgNew potential,
    hPairUpdate, ?_, ?_, ?_⟩
  · exact hBre.trans hNormInt
  · rw [hBre]
    exact sq_nonneg _
  · rw [hBre]
    exact hBudget.2

end AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticFeatureRisk
