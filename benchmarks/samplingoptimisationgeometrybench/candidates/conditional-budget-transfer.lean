import Mathlib.Probability.Martingale.Convergence
import Mathlib.Probability.Moments.Variance
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap
import Mathlib.MeasureTheory.Function.LpSeminorm.LpNorm
import Mathlib.MeasureTheory.Measure.Real
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.MeasureTheory.Function.ConditionalExpectation.PullOut

/-!
# From conditional likelihood budgets to an unbounded real work bound

Trusted candidate for the positive side of the public `sogb-035` exercise.
The generic probability-space proof verifies predictable normalization of
the squared likelihoods, extends compatible prefix integrals to the full
law, and transfers real L² observables with the variance factor in the exercise.
The concrete finite-prefix filtration uses Mathlib's finite-coordinate
construction with the empty prefix at time zero.

This file assumes the exact conditional second-moment and prefix integral
identities. It does not derive them from the exercise's binary conditional
tables or construct the raw likelihood-ratio process. Work is represented
here by a real-valued L² function; the full exercise's a.e. choice of a
finite representative for an extended-valued charge is not built here.
Absolute continuity implies null-event transfer; it does not construct the
stopping rule. No aligned task, admission, native verifier result, model
score, Registry leaf or paper result follows from this candidate.
-/

namespace SamplingOptimisationGeometryBench.ConditionalBudgetTransfer
open MeasureTheory Set Filter
open scoped BigOperators ENNReal NNReal Topology

private theorem uniformIntegrable_one_of_two_bound {Ω : Type*} [MeasurableSpace Ω]
    {P : Measure Ω} [IsProbabilityMeasure P] {X : ℕ → Ω → ℝ} {R : ℝ≥0}
    (hX : ∀ n, AEStronglyMeasurable (X n) P)
    (hR : ∀ n, eLpNorm (X n) 2 P ≤ R) : UniformIntegrable X 1 P := by
  have hL1 (n : ℕ) : eLpNorm (X n) 1 P ≤ R :=
    (eLpNorm_le_eLpNorm_of_exponent_le (by norm_num : (1 : ℝ≥0∞) ≤ 2) (hX n)).trans (hR n)
  refine ⟨hX, ?_, ⟨R, hL1⟩⟩
  intro ε hε
  let r := ε / ((R : ℝ) + 1)
  have hd : 0 < (R : ℝ) + 1 := by positivity
  have hr : 0 < r := div_pos hε hd
  refine ⟨r ^ 2, sq_pos_of_pos hr, ?_⟩
  intro n s hs hsmall
  rw [eLpNorm_indicator_eq_eLpNorm_restrict hs]
  have hHolder := eLpNorm_le_eLpNorm_mul_rpow_measure_univ
    (by norm_num : (1 : ℝ≥0∞) ≤ 2) ((hX n).restrict (s := s))
  have hexp : 1 / (1 : ℝ≥0∞).toReal - 1 / (2 : ℝ≥0∞).toReal = (1 / 2 : ℝ) := by
    norm_num
  rw [hexp, Measure.restrict_apply MeasurableSet.univ, univ_inter] at hHolder
  have hpow : (ENNReal.ofReal (r ^ 2)) ^ (1 / 2 : ℝ) = ENNReal.ofReal r := by
    rw [ENNReal.ofReal_pow hr.le, ← ENNReal.rpow_natCast, ← ENNReal.rpow_mul]
    norm_num
  calc
    _ ≤ eLpNorm (X n) 2 (P.restrict s) * P s ^ (1 / 2 : ℝ) := hHolder
    _ ≤ (R : ℝ≥0∞) * ENNReal.ofReal r := mul_le_mul'
      ((eLpNorm_restrict_le (X n) 2 P s).trans (hR n))
      ((ENNReal.rpow_le_rpow hsmall (by norm_num)).trans_eq hpow)
    _ = ENNReal.ofReal ((R : ℝ) * r) := by
      rw [ENNReal.ofReal_mul R.coe_nonneg, ENNReal.ofReal_coe_nnreal]
    _ ≤ ENNReal.ofReal ε := by
      apply ENNReal.ofReal_le_ofReal
      have hm : ((R : ℝ) + 1) * r = ε := by
        dsimp [r]
        field_simp
      nlinarith [hr.le]

/-- From the finite-stage density identities on a generating filtration, produce
the actual full-space density. No global absolute continuity is assumed. -/
theorem exists_full_density_of_prefix_integrals {Ω : Type*} [m : MeasurableSpace Ω]
    (P Q : Measure Ω) [IsProbabilityMeasure P] [IsProbabilityMeasure Q]
    (ℱ : Filtration ℕ m) (hgen : (⨆ n, ℱ n) = m)
    (X : ℕ → Ω → ℝ) (hX : StronglyAdapted ℱ X)
    (hnonneg : ∀ n, 0 ≤ᵐ[P] X n) (R : ℝ≥0)
    (hR : ∀ n, eLpNorm (X n) 2 P ≤ R)
    (hQ : ∀ n s, MeasurableSet[ℱ n] s → (∫ x in s, X n x ∂P) = Q.real s) :
    ∃ L : Ω → ℝ, StronglyMeasurable L ∧ 0 ≤ᵐ[P] L ∧ MemLp L 2 P ∧
      (∫ x, (L x)^2 ∂P) ≤ (R : ℝ)^2 ∧ (∫ x, L x ∂P) = 1 ∧
      Q = P.withDensity (fun x => ENNReal.ofReal (L x)) ∧ Q ≪ P := by
  have hXm (n : ℕ) : AEStronglyMeasurable (X n) P :=
    ((hX n).mono (ℱ.le n)).aestronglyMeasurable
  have hXi (n : ℕ) : Integrable (X n) P :=
    (show MemLp (X n) 2 P from ⟨hXm n, (hR n).trans_lt ENNReal.coe_lt_top⟩).integrable
      (by norm_num)
  have hM : Martingale X ℱ P := martingale_of_setIntegral_eq_succ hX hXi
    (fun n s hs => (hQ n s hs).trans (hQ (n + 1) s (ℱ.mono (Nat.le_succ n) s hs)).symm)
  let L := ℱ.limitProcess X P
  have hL : MemLp L 2 P := hM.submartingale.memLp_limitProcess hR
  have hLi : Integrable L P := hL.integrable (by norm_num)
  have hUi := uniformIntegrable_one_of_two_bound hXm hR
  have ht := hM.submartingale.ae_tendsto_limitProcess_of_uniformIntegrable hUi
  have hLnn : 0 ≤ᵐ[P] L := by
    filter_upwards [ht, ae_all_iff.2 hnonneg] with x hx hxnn
    exact ge_of_tendsto' hx hxnn
  have hLbd : eLpNorm L 2 P ≤ R := Lp.eLpNorm_le_of_ae_tendsto
    (Eventually.of_forall hR) hXm ht
  have hLp : lpNorm L 2 P ≤ (R : ℝ) := by
    rw [← toReal_eLpNorm hL.1]
    exact_mod_cast ENNReal.toReal_mono ENNReal.coe_ne_top hLbd
  have hsqrt : lpNorm L 2 P = Real.sqrt (∫ x, (L x)^2 ∂P) := by
    rw [lpNorm_eq_integral_norm_rpow_toReal (by norm_num) (by simp) hL.1, Real.sqrt_eq_rpow]
    norm_num [Real.rpow_two]
  have hLsq : (∫ x, (L x)^2 ∂P) ≤ (R : ℝ)^2 := by
    rw [hsqrt] at hLp
    have hi : 0 ≤ ∫ x, (L x)^2 ∂P := integral_nonneg fun _ => sq_nonneg _
    simpa only [Real.sq_sqrt hi] using
      (sq_le_sq₀ (Real.sqrt_nonneg _) R.coe_nonneg).2 hLp
  have hprefix (n : ℕ) (s : Set Ω) (hs : MeasurableSet[ℱ n] s) :
      (∫ x in s, L x ∂P) = Q.real s := by
    calc
      _ = ∫ x in s, (P[L | ℱ n]) x ∂P := (setIntegral_condExp (ℱ.le n) hLi hs).symm
      _ = ∫ x in s, X n x ∂P := setIntegral_congr_ae (ℱ.le n s hs)
        ((hM.ae_eq_condExp_limitProcess hUi n).mono fun _ hx _ => hx.symm)
      _ = _ := hQ n s hs
  have hmass : (∫ x, L x ∂P) = 1 := by
    simpa [measureReal_def] using hprefix 0 Set.univ MeasurableSet.univ
  let D := P.withDensity (fun x => ENNReal.ofReal (L x))
  have hDp (n : ℕ) (s : Set Ω) (hs : MeasurableSet[ℱ n] s) : Q s = D s := by
    change _ = (P.withDensity fun x => ENNReal.ofReal (L x)) s
    rw [withDensity_apply _ (ℱ.le n s hs),
      ← ofReal_integral_eq_lintegral_ofReal hLi.restrict (ae_restrict_of_ae hLnn),
      hprefix n s hs, ofReal_measureReal]
  let C : Set (Set Ω) := ⋃ n, {s | MeasurableSet[ℱ n] s}
  have hCD : m = MeasurableSpace.generateFrom C :=
    hgen.symm.trans (MeasurableSpace.generateFrom_iUnion_measurableSet _).symm
  have hCpi : IsPiSystem C :=
    isPiSystem_iUnion_of_monotone _ (fun n => (ℱ n).isPiSystem_measurableSet)
      (fun _ _ h => ℱ.mono h)
  have hQD : Q = D := ext_of_generate_finite C hCD hCpi
    (fun s hs => by
      obtain ⟨n, hn⟩ := Set.mem_iUnion.mp hs
      exact hDp n s hn) (hDp 0 Set.univ MeasurableSet.univ)
  refine ⟨L, Filtration.stronglyMeasurable_limit_process', hLnn, hL, hLsq,
    hmass, hQD, ?_⟩
  rw [hQD]
  exact withDensity_absolutelyContinuous P _

open ProbabilityTheory

/-- A normalized nonnegative L² density transfers the mean of every real L²
observable, even if the observable is not bounded. -/
theorem abs_integral_sub_le_of_square_integrable_density {Ω : Type*} [MeasurableSpace Ω]
    (P Q : Measure Ω) [IsProbabilityMeasure P]
    {L W : Ω → ℝ} (hLm : Measurable L) (hnn : 0 ≤ᵐ[P] L)
    (hL : MemLp L 2 P) (hW : MemLp W 2 P) (hmean : (∫ x, L x ∂P) = 1)
    (hQ : Q = P.withDensity (fun x => ENNReal.ofReal (L x))) :
    Integrable W Q ∧ |(∫ x, W x ∂Q) - (∫ x, W x ∂P)| ≤
      Real.sqrt (variance L P * variance W P) := by
  have hm : Measurable (fun x => ENNReal.ofReal (L x)) :=
    ENNReal.measurable_ofReal.comp hLm
  have hfinite : ∀ᵐ x ∂P, ENNReal.ofReal (L x) < ∞ :=
    Eventually.of_forall fun _ => ENNReal.ofReal_lt_top
  have heq : (fun x => (ENNReal.ofReal (L x)).toReal • W x) =ᵐ[P]
      fun x => L x * W x := by
    filter_upwards [hnn] with x hx
    simp [ENNReal.toReal_ofReal hx, smul_eq_mul]
  have hWQ : Integrable W Q := by
    rw [hQ, integrable_withDensity_iff_integrable_smul' hm hfinite]
    exact (hL.integrable_mul hW).congr heq.symm
  refine ⟨hWQ, ?_⟩
  have hd : (∫ x, W x ∂Q) = ∫ x, L x * W x ∂P := by
    rw [hQ, integral_withDensity_eq_integral_toReal_smul hm hfinite]
    exact integral_congr_ae heq
  have hc : (∫ x, W x ∂Q) - (∫ x, W x ∂P) = covariance L W P := by
    rw [covariance_eq_sub hL hW, hmean, one_mul, hd]
    rfl
  rw [hc, covariance]
  let f : Ω → ℝ := fun x => L x - ∫ y, L y ∂P
  let g : Ω → ℝ := fun x => W x - ∫ y, W y ∂P
  change |∫ x, f x * g x ∂P| ≤ _
  have hf : MemLp f 2 P := hL.sub (memLp_const _)
  have hg : MemLp g 2 P := hW.sub (memLp_const _)
  have hCS := integral_mul_norm_le_Lp_mul_Lq (μ := P) Real.HolderConjugate.two_two
    (show MemLp f (ENNReal.ofReal 2) P by norm_num; exact hf)
    (show MemLp g (ENNReal.ofReal 2) P by norm_num; exact hg)
  have hCS' : (∫ x, ‖f x‖ * ‖g x‖ ∂P) ≤
      Real.sqrt (variance L P) * Real.sqrt (variance W P) := by
    rw [variance_eq_integral hL.aemeasurable, variance_eq_integral hW.aemeasurable,
      Real.sqrt_eq_rpow, Real.sqrt_eq_rpow]
    simpa [f, g, Real.rpow_two] using hCS
  calc
    _ ≤ ∫ x, ‖f x * g x‖ ∂P := by
      simpa only [Real.norm_eq_abs] using (norm_integral_le_integral_norm
        (μ := P) (fun x => f x * g x))
    _ ≤ Real.sqrt (variance L P) * Real.sqrt (variance W P) := by
      simpa only [norm_mul] using hCS'
    _ = _ := (Real.sqrt_mul (variance_nonneg L P) _).symm

/-- The consumer checks the exact exponential constant; the proof of the
prefix norm bound from the pathwise budget remains a separate obligation. -/
theorem work_bound_of_prefix_norm {Ω : Type*} [m : MeasurableSpace Ω]
    (P Q : Measure Ω) [IsProbabilityMeasure P] [IsProbabilityMeasure Q]
    (ℱ : Filtration ℕ m) (hgen : (⨆ n, ℱ n) = m)
    (X : ℕ → Ω → ℝ) (hX : StronglyAdapted ℱ X)
    (hnn : ∀ n, 0 ≤ᵐ[P] X n) (B : ℝ)
    (hB : ∀ n, eLpNorm (X n) 2 P ≤ ENNReal.ofReal (Real.exp (B / 2)))
    (hQ : ∀ n s, MeasurableSet[ℱ n] s → (∫ x in s, X n x ∂P) = Q.real s)
    (W : Ω → ℝ) (hW : MemLp W 2 P) :
    Q ≪ P ∧ Integrable W Q ∧
      |(∫ x, W x ∂Q) - (∫ x, W x ∂P)| ≤ Real.sqrt ((Real.exp B - 1) * variance W P) := by
  let R : ℝ≥0 := ⟨Real.exp (B / 2), (Real.exp_pos _).le⟩
  have hRe : (R : ℝ≥0∞) = ENNReal.ofReal (Real.exp (B / 2)) :=
    (ENNReal.ofReal_eq_coe_nnreal (Real.exp_pos _).le).symm
  have hR (n : ℕ) : eLpNorm (X n) 2 P ≤ R := by
    simpa only [hRe] using hB n
  obtain ⟨L, hLm, hLnn, hL, hLsq, hLmean, hQD, hQP⟩ :=
    exists_full_density_of_prefix_integrals P Q ℱ hgen X hX hnn R hR hQ
  obtain ⟨hWQ, hcost⟩ := abs_integral_sub_le_of_square_integrable_density
    P Q hLm.measurable hLnn hL hW hLmean hQD
  have hexp : (R : ℝ)^2 = Real.exp B := by
    change (Real.exp (B / 2))^2 = Real.exp B
    rw [pow_two, ← Real.exp_add]
    congr 1
    ring
  have hvar : variance L P ≤ Real.exp B - 1 := by
    rw [variance_eq_sub hL, hLmean, one_pow]
    exact sub_le_sub_right (hLsq.trans_eq hexp) 1
  exact ⟨hQP, hWQ, hcost.trans (Real.sqrt_le_sqrt
    (mul_le_mul_of_nonneg_right hvar (variance_nonneg W P)))⟩

/-- Stage n sees exactly coordinates 0 through n−1, including the empty history
at stage zero. This uses Mathlib's existing finite-coordinate filtration. -/
def historyFiltration (β : ℕ → Type*) [∀ i, MeasurableSpace (β i)] :
    Filtration ℕ (MeasurableSpace.pi (X := β)) where
  seq n := (Filtration.piFinset (X := β)) (Finset.range n)
  mono' _ _ h := (Filtration.piFinset (X := β)).mono (Finset.range_mono h)
  le' n := (Filtration.piFinset (X := β)).le (Finset.range n)

theorem iSup_historyFiltration (β : ℕ → Type*) [∀ i, MeasurableSpace (β i)] :
    (⨆ n, historyFiltration β n) = MeasurableSpace.pi (X := β) := by
  refine le_antisymm (iSup_le (historyFiltration β).le) ?_
  change (⨆ i, MeasurableSpace.comap (fun x : (j : ℕ) → β j => x i) inferInstance) ≤ _
  refine iSup_le fun i => ?_
  apply le_trans ?_ (le_iSup (fun n => historyFiltration β n) (i + 1))
  change _ ≤ (Filtration.piFinset (X := β)) (Finset.range (i + 1))
  let j : (Finset.range (i + 1) : Set ℕ) := ⟨i, Finset.mem_range.2 (Nat.lt_succ_self i)⟩
  have hj : Measurable (fun y : (a : (Finset.range (i + 1) : Set ℕ)) → β a => y j) :=
    measurable_pi_apply j
  rw [Filtration.piFinset_eq_comap_restrict]
  have hle := MeasurableSpace.comap_mono
    (g := (Finset.range (i + 1) : Set ℕ).domRestrict) hj.comap_le
  rw [MeasurableSpace.comap_comp] at hle
  exact hle

/-- Predictably normalize the squared process, preserving its expectation.
The conditional second-moment identity is an input; no likelihood ratios
or identities for binary tables are constructed here. -/
theorem integral_sq_le_exp_of_pathwise_conditional_budget {Ω : Type*} [m : MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P] (ℱ : Filtration ℕ m)
    (X η : ℕ → Ω → ℝ) (hη : StronglyAdapted ℱ η) (hη₀ : ∀ n x, 0 ≤ η n x)
    (hXi : ∀ n, Integrable (fun x => X n x ^ 2) P)
    (hinit : X 0 =ᵐ[P] 1)
    (hcond : ∀ n, P[(fun x => X (n+1) x ^ 2) | ℱ n] =ᵐ[P]
      fun x => X n x ^ 2 * (1 + η n x))
    (B : ℝ) (hB : ∀ n, ∀ᵐ x ∂P, ∑ k ∈ Finset.range n, η k x ≤ B) :
    ∀ n, (∫ x, X n x ^ 2 ∂P) ≤ Real.exp B := by
  let A : ℕ → Ω → ℝ := fun n x => ∏ k ∈ Finset.range n, (1 + η k x)
  have hA (n : ℕ) (x : Ω) : 1 ≤ A n x :=
    Finset.one_le_prod fun k _ => le_add_of_nonneg_right (hη₀ k x)
  have hAp (n : ℕ) (x : Ω) : 0 < A n x := zero_lt_one.trans_le (hA n x)
  have hAs (n : ℕ) (x : Ω) : A (n+1) x = A n x * (1 + η n x) :=
    Finset.prod_range_succ (fun k => 1 + η k x) n
  have hAm (n k : ℕ) (hk : k ≤ n+1) : StronglyMeasurable[ℱ n] (A k) := by
    have hm (i : ℕ) (hi : i ∈ Finset.range k) :
        Measurable[ℱ n] (fun x => 1 + η i x) :=
      measurable_const.add ((hη i).mono
        (ℱ.mono (Nat.lt_succ_iff.mp ((Finset.mem_range.mp hi).trans_le hk)))).measurable
    exact (Finset.measurable_fun_prod _ hm).stronglyMeasurable
  let Y : ℕ → Ω → ℝ := fun n x => (A n x)⁻¹ * X n x ^ 2
  have hY₀ (n : ℕ) (x : Ω) : 0 ≤ Y n x :=
    mul_nonneg (inv_nonneg.mpr (hAp n x).le) (sq_nonneg _)
  have hY (n : ℕ) : Integrable (Y n) P := by
    refine (hXi n).mono
      ((((hAm n n (Nat.le_succ n)).mono (ℱ.le n)).inv₀).aestronglyMeasurable.mul
        (hXi n).aestronglyMeasurable) (Eventually.of_forall fun x => ?_)
    rw [Real.norm_of_nonneg (hY₀ n x), Real.norm_of_nonneg (sq_nonneg _)]
    exact mul_le_of_le_one_left (sq_nonneg _) (inv_le_one_of_one_le₀ (hA n x))
  have hnorm (n : ℕ) : P[Y (n+1) | ℱ n] =ᵐ[P] Y n := by
    refine (condExp_mul_of_stronglyMeasurable_left ((hAm n (n+1) le_rfl).inv₀)
      (hY (n+1)) (hXi (n+1))).trans ?_
    filter_upwards [hcond n] with x hx
    change (A (n+1) x)⁻¹ * (P[(fun y => X (n+1) y ^ 2) | ℱ n]) x =
      (A n x)⁻¹ * X n x ^ 2
    rw [hx, hAs]
    have h1 : 0 < 1 + η n x := one_pos.trans_le (le_add_of_nonneg_right (hη₀ n x))
    field_simp [(hAp n x).ne', h1.ne']
  have hmean (n : ℕ) : (∫ x, Y n x ∂P) = 1 := by
    induction n with
    | zero =>
      calc
        _ = ∫ _x : Ω, (1 : ℝ) ∂P := by
          apply integral_congr_ae
          filter_upwards [hinit] with x hx
          change X 0 x = 1 at hx
          simp [Y, A, hx]
        _ = 1 := by simp
    | succ n ih =>
      calc
        _ = ∫ x, (P[Y (n+1) | ℱ n]) x ∂P := (integral_condExp (ℱ.le n)).symm
        _ = ∫ x, Y n x ∂P := integral_congr_ae (hnorm n)
        _ = 1 := ih
  intro n
  have hb : ∀ᵐ x ∂P, X n x ^ 2 ≤ Y n x * Real.exp B := by
    filter_upwards [hB n] with x hx
    have hu : A n x ≤ Real.exp B := (Real.prod_one_add_le_exp_sum _ fun k => hη₀ k x).trans
      (Real.exp_le_exp.mpr hx)
    calc
      _ = Y n x * A n x := by
        dsimp [Y]
        field_simp [(hAp n x).ne']
      _ ≤ Y n x * Real.exp B := mul_le_mul_of_nonneg_left hu (hY₀ n x)
  have hh := integral_mono_ae (hXi n) ((hY n).mul_const (Real.exp B)) hb
  simpa only [integral_mul_const, hmean n, one_mul] using hh

/-- Conditional identities and the pathwise budget imply the exact real work
bound, with no assumption that the implemented law already integrates it. -/
theorem work_bound_of_conditional_budget {Ω : Type*} [m : MeasurableSpace Ω]
    (P Q : Measure Ω) [IsProbabilityMeasure P] [IsProbabilityMeasure Q]
    (ℱ : Filtration ℕ m) (hgen : (⨆ n, ℱ n) = m)
    (X η : ℕ → Ω → ℝ) (hX : StronglyAdapted ℱ X)
    (hnn : ∀ n, 0 ≤ᵐ[P] X n) (hη : StronglyAdapted ℱ η) (hη₀ : ∀ n x, 0 ≤ η n x)
    (hXi : ∀ n, Integrable (fun x => X n x ^ 2) P) (hinit : X 0 =ᵐ[P] 1)
    (hcond : ∀ n, P[(fun x => X (n+1) x ^ 2) | ℱ n] =ᵐ[P]
      fun x => X n x ^ 2 * (1 + η n x))
    (B : ℝ) (hB : ∀ n, ∀ᵐ x ∂P, ∑ k ∈ Finset.range n, η k x ≤ B)
    (hQ : ∀ n s, MeasurableSet[ℱ n] s → (∫ x in s, X n x ∂P) = Q.real s)
    (W : Ω → ℝ) (hW : MemLp W 2 P) :
    Q ≪ P ∧ Integrable W Q ∧
      |(∫ x, W x ∂Q) - (∫ x, W x ∂P)| ≤ Real.sqrt ((Real.exp B - 1) * variance W P) := by
  have hS := integral_sq_le_exp_of_pathwise_conditional_budget P ℱ X η hη hη₀ hXi
    hinit hcond B hB
  refine work_bound_of_prefix_norm P Q ℱ hgen X hX hnn B ?_ hQ W hW
  intro n
  have hm : AEStronglyMeasurable (X n) P := ((hX n).mono (ℱ.le n)).aestronglyMeasurable
  have hf : MemLp (X n) 2 P := (memLp_two_iff_integrable_sq hm).2 (hXi n)
  have heq : lpNorm (X n) 2 P = Real.sqrt (∫ x, (X n x)^2 ∂P) := by
    rw [lpNorm_eq_integral_norm_rpow_toReal (by norm_num) (by simp) hm, Real.sqrt_eq_rpow]
    norm_num [Real.rpow_two]
  rw [← ofReal_lpNorm hf, heq]
  apply ENNReal.ofReal_le_ofReal
  refine (Real.sqrt_le_sqrt (hS n)).trans_eq ?_
  rw [Real.sqrt_eq_rpow, ← Real.exp_mul]
  congr 1
  ring

/--
info: 'SamplingOptimisationGeometryBench.ConditionalBudgetTransfer.exists_full_density_of_prefix_integrals' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs (whitespace := lax) in
#print axioms exists_full_density_of_prefix_integrals

/--
info: 'SamplingOptimisationGeometryBench.ConditionalBudgetTransfer.abs_integral_sub_le_of_square_integrable_density' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs (whitespace := lax) in
#print axioms abs_integral_sub_le_of_square_integrable_density

/--
info: 'SamplingOptimisationGeometryBench.ConditionalBudgetTransfer.work_bound_of_prefix_norm' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs (whitespace := lax) in
#print axioms work_bound_of_prefix_norm

/--
info: 'SamplingOptimisationGeometryBench.ConditionalBudgetTransfer.iSup_historyFiltration' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs (whitespace := lax) in
#print axioms iSup_historyFiltration

/--
info: 'SamplingOptimisationGeometryBench.ConditionalBudgetTransfer.integral_sq_le_exp_of_pathwise_conditional_budget' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs (whitespace := lax) in
#print axioms integral_sq_le_exp_of_pathwise_conditional_budget

/--
info: 'SamplingOptimisationGeometryBench.ConditionalBudgetTransfer.work_bound_of_conditional_budget' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs (whitespace := lax) in
#print axioms work_bound_of_conditional_budget

end SamplingOptimisationGeometryBench.ConditionalBudgetTransfer
