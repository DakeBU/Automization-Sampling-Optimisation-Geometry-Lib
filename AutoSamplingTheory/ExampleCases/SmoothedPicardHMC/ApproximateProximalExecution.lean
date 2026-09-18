import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization
import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationFirstOrder
import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder
import Mathlib.Topology.MetricSpace.Contracting
import Mathlib.MeasureTheory.MeasurableSpace.Constructions
import Mathlib.MeasureTheory.Constructions.BorelSpace.Basic
import Mathlib.MeasureTheory.Constructions.BorelSpace.Order
import Mathlib.MeasureTheory.Constructions.BorelSpace.Metrizable
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

/-!
# Stopped gradient-only proximal queries

Work in progress for arXiv:2609.06906v1 Algorithm D.2 / Lemma D.3.
The residual test returns the current iterate, counting the final gradient
query. Exact-real comparisons are the oracle model, not floating-point code.
No expected run-wide cost or sampling accuracy is asserted.
-/

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ApproximateProximalExecution

open Filter Topology MeasureTheory InnerProductSpace
open scoped NNReal RealInnerProductSpace

private theorem geometric_certificate {c z t : ℝ} (hc : 0 < c) (hc1 : c < 1)
    (hz : 0 ≤ z) (ht : 0 < t) :
    z * c ^ Nat.ceil (Real.log (1+z/t) / (-Real.log c)) ≤ t := by
  have ha : 0 < -Real.log c := neg_pos.mpr (Real.log_neg hc hc1)
  have hp : 0 < 1+z/t := by positivity
  have hN := Nat.le_ceil (Real.log (1+z/t) / (-Real.log c))
  have hb := (div_le_iff₀ ha).mp hN
  have he : (Nat.ceil (Real.log (1+z/t) / (-Real.log c)) : ℝ) * Real.log c ≤
      -Real.log (1+z/t) := by nlinarith
  have he' := mul_le_mul_of_nonneg_left (Real.exp_le_exp.mpr he) hz
  rw [Real.exp_nat_mul, Real.exp_log hc, Real.exp_neg, Real.exp_log hp] at he'
  apply he'.trans
  rw [← div_eq_mul_inv]
  apply (div_le_iff₀ hp).mpr
  have hid : t*(1+z/t)=t+z := by field_simp
  rw [hid]
  linarith

section
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- Exact-real interpreter. Each nonempty fuel step asks for g(x) once;
the final successful test returns x, not the newly computed point. -/
noncomputable def proximalQuery (g : E → E) (eta eps : ℝ) (y : E) :
    ℕ → E → Option (E × ℕ)
  | 0, _ => none
  | n+1, x => by
    classical
    let z := y-eta • g x
    exact if ‖z-x‖ ≤ (1-eta)*eps then some (x,1)
      else (proximalQuery g eta eps y n z).map (fun r => (r.1,r.2+1))

private theorem run_first_stop (g : E → E) (eta eps : ℝ) (y : E) (n : ℕ) (x : E)
    (hs : ‖(fun z => y-eta • g z)^[n+1] x -
      (fun z => y-eta • g z)^[n] x‖ ≤ (1-eta)*eps)
    (hb : ∀ j < n, ¬ ‖(fun z => y-eta • g z)^[j+1] x -
      (fun z => y-eta • g z)^[j] x‖ ≤ (1-eta)*eps) :
    proximalQuery g eta eps y (n+1) x = some ((fun z => y-eta • g z)^[n] x,n+1) := by
  classical
  induction n generalizing x with
  | zero => simpa [proximalQuery] using hs
  | succ n ih =>
    have hzero := hb 0 (Nat.zero_lt_succ n)
    change ¬ ‖y-eta • g x-x‖ ≤ (1-eta)*eps at hzero
    have hsn : ‖(fun z => y-eta • g z)^[n+1] (y-eta • g x) -
        (fun z => y-eta • g z)^[n] (y-eta • g x)‖ ≤ (1-eta)*eps := by
      simpa only [← Function.iterate_succ_apply] using hs
    have hbn : ∀ j < n, ¬ ‖(fun z => y-eta • g z)^[j+1] (y-eta • g x) -
        (fun z => y-eta • g z)^[j] (y-eta • g x)‖ ≤ (1-eta)*eps := by
      intro j hj
      simpa only [← Function.iterate_succ_apply] using hb (j+1) (Nat.succ_lt_succ hj)
    rw [proximalQuery, if_neg hzero, ih _ hsn hbn]
    simp only [Option.map_some, ← Function.iterate_succ_apply]

private theorem stopped_contraction [CompleteSpace E] [MeasurableSpace E] [BorelSpace E]
    [SecondCountableTopology E] {g : E → E} (hg : LipschitzWith 1 g)
    {eta c eps : ℝ} (heta : 0 < eta) (hec : eta ≤ c) (hc : c < 1) (heps : 0 < eps) :
    let T := fun y x : E => y-eta • g x
    ∃ p : E → E, ∃ N : E → ℕ,
      Measurable p ∧ Measurable N ∧ Measurable (fun y => (T y)^[N y] y) ∧
      ∀ y, p y + eta • g (p y) = y ∧
        ‖(T y)^[N y+1] y-(T y)^[N y] y‖ ≤ (1-eta)*eps ∧
        (∀ j < N y, ¬ ‖(T y)^[j+1] y-(T y)^[j] y‖ ≤ (1-eta)*eps) ∧
        ‖(T y)^[N y] y-p y‖ ≤ eps ∧
        N y ≤ Nat.ceil (Real.log (1+‖g y‖/((1-c)*eps))/(-Real.log c)) ∧
        proximalQuery g eta eps y (N y+1) y = some ((T y)^[N y] y,N y+1) := by
  classical
  let T := fun y x : E => y-eta • g x
  have het : eta < 1 := hec.trans_lt hc
  have hcpos : 0 < c := heta.trans_le hec
  have hcontract (y : E) : ContractingWith ⟨eta,heta.le⟩ (T y) := by
    refine ⟨het, LipschitzWith.of_dist_le_mul fun x z => ?_⟩
    have h := hg.dist_le_mul z x
    simp only [NNReal.coe_one, one_mul, dist_eq_norm] at h
    have hid : T y x - T y z = eta • (g z-g x) := by dsimp [T]; module
    rw [dist_eq_norm, hid, norm_smul, Real.norm_eq_abs, abs_of_pos heta]
    change eta*‖g z-g x‖ ≤ eta*dist x z
    rw [dist_eq_norm]
    simpa only [norm_sub_rev z x] using mul_le_mul_of_nonneg_left h heta.le
  let p := fun y => (hcontract y).fixedPoint (T y)
  have hit (n : ℕ) : Measurable (fun y => (T y)^[n] y) := by
    induction n with
    | zero => change Measurable (fun y : E => y); exact measurable_id
    | succ n ih =>
      simp only [Function.iterate_succ_apply']
      exact measurable_id.sub ((hg.continuous.measurable.comp ih).const_smul eta)
  have hp : Measurable p := measurable_of_tendsto_metrizable hit
    (tendsto_pi_nhds.mpr fun y => (hcontract y).tendsto_iterate_fixedPoint y)
  let B := fun y => Nat.ceil (Real.log (1+‖g y‖/((1-c)*eps))/(-Real.log c))
  have hcert (y : E) : ‖(T y)^[B y+1] y-(T y)^[B y] y‖ ≤ (1-eta)*eps := by
    have hgeom := (hcontract y).toLipschitzWith.dist_iterate_succ_le_geometric y (B y)
    have hzero : dist y (T y y) = eta*‖g y‖ := by
      simp [T, norm_smul, abs_of_pos heta]
    rw [hzero, dist_eq_norm, norm_sub_rev] at hgeom
    have hfac : eta*‖g y‖ ≤ ‖g y‖ := by nlinarith [norm_nonneg (g y)]
    have hpow : eta ^ B y ≤ c ^ B y := pow_le_pow_left₀ heta.le hec _
    have hprod : eta*‖g y‖*eta^B y ≤ ‖g y‖*c^B y :=
      mul_le_mul hfac hpow (pow_nonneg heta.le _) (norm_nonneg _)
    have hscalar := geometric_certificate hcpos hc (norm_nonneg (g y))
      (mul_pos (sub_pos.mpr hc) heps)
    have hend : (1-c)*eps ≤ (1-eta)*eps := by nlinarith
    exact hgeom.trans (hprod.trans (hscalar.trans hend))
  have ht (y : E) : ∃ n : ℕ, ‖(T y)^[n+1] y-(T y)^[n] y‖ ≤ (1-eta)*eps :=
    ⟨B y,hcert y⟩
  let N := fun y => Nat.find (ht y)
  have hset (n : ℕ) : MeasurableSet {y : E | ‖(T y)^[n+1] y-(T y)^[n] y‖ ≤ (1-eta)*eps} :=
    measurableSet_le ((hit (n+1)).sub (hit n)).norm measurable_const
  refine ⟨p,N,hp,measurable_find ht hset,Measurable.find hit hset ht,fun y => ?_⟩
  have hfix : T y (p y) = p y := (hcontract y).fixedPoint_isFixedPt
  have hs := Nat.find_spec (ht y)
  have hb : ∀ j < N y, ¬ ‖(T y)^[j+1] y-(T y)^[j] y‖ ≤ (1-eta)*eps :=
    fun j hj => Nat.find_min (ht y) hj
  refine ⟨(sub_eq_iff_eq_add.mp hfix).symm,hs,hb,?_,Nat.find_min' (ht y) (hcert y),
    run_first_stop g eta eps y (N y) y hs hb⟩
  have hd := (hcontract y).aposteriori_dist_iterate_fixedPoint_le y (N y)
  rw [dist_eq_norm, dist_eq_norm] at hd
  change ‖(T y)^[N y] y-p y‖ ≤
    ‖(T y)^[N y] y-(T y)^[N y+1] y‖/(1-eta) at hd
  rw [norm_sub_rev ((T y)^[N y] y) ((T y)^[N y+1] y)] at hd
  exact hd.trans ((div_le_iff₀ (sub_pos.mpr het)).mpr (by simpa only [N, mul_comm] using hs))

private theorem count_bound {c z eps : ℝ} (hc : 0 < c) (hc1 : c < 1)
    (hz : 0 ≤ z) (heps : 0 < eps) {N : ℕ}
    (hN : N ≤ Nat.ceil (Real.log (1+z/((1-c)*eps))/(-Real.log c))) :
    (N : ℝ)+1 ≤ (2+(1+Real.log ((1-c)⁻¹))/(-Real.log c)) *
      (1+Real.log (1+z/eps)) := by
  have hd : 0 < 1-c := sub_pos.mpr hc1
  have ha : 0 < -Real.log c := neg_pos.mpr (Real.log_neg hc hc1)
  have hR : 0 ≤ z/eps := div_nonneg hz heps.le
  have hL : 0 ≤ Real.log (1+z/eps) := Real.log_nonneg (by linarith)
  have hb : 0 ≤ Real.log ((1-c)⁻¹) := Real.log_nonneg (by
    have hm := mul_nonneg (inv_nonneg.mpr hd.le) hc.le
    have hi := inv_mul_cancel₀ hd.ne'
    nlinarith)
  have harg : 1+z/((1-c)*eps) ≤ (1+z/eps)/(1-c) := by
    apply (le_div_iff₀ hd).mpr
    have hid : (1+z/((1-c)*eps))*(1-c)=1-c+z/eps := by field_simp
    rw [hid]
    linarith
  have hlog := Real.log_le_log (by positivity : 0 < 1+z/((1-c)*eps)) harg
  rw [Real.log_div (by positivity) (ne_of_gt hd)] at hlog
  have hlog' : Real.log (1+z/((1-c)*eps)) ≤
      Real.log (1+z/eps)+Real.log ((1-c)⁻¹) := by
    rw [Real.log_inv]
    linarith
  have hnon : 0 ≤ Real.log (1+z/((1-c)*eps))/(-Real.log c) :=
    div_nonneg (Real.log_nonneg (by
      have hh := div_nonneg hz (mul_pos hd heps).le
      linarith)) ha.le
  have hceil := Nat.ceil_lt_add_one hnon
  have hcast : (N : ℝ) ≤ (Nat.ceil (Real.log (1+z/((1-c)*eps))/(-Real.log c)) : ℝ) :=
    by exact_mod_cast hN
  have hfirst : (N : ℝ)+1 ≤
      (Real.log (1+z/eps)+Real.log ((1-c)⁻¹))/(-Real.log c)+2 := by
    have hh := (div_le_div_iff_of_pos_right ha).mpr hlog'
    linarith
  apply hfirst.trans
  have hid : (2+(1+Real.log ((1-c)⁻¹))/(-Real.log c)) * (1+Real.log (1+z/eps)) -
      ((Real.log (1+z/eps)+Real.log ((1-c)⁻¹))/(-Real.log c)+2) =
      (1+(2*(-Real.log c)+Real.log ((1-c)⁻¹))*Real.log (1+z/eps))/(-Real.log c) := by
    field_simp [ne_of_lt (Real.log_neg hc hc1)]
    ring
  apply sub_nonneg.mp
  rw [hid]
  positivity

end

section
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [CompleteSpace E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

/-- The actual first-residual-stopped gradient program returns an accurate
proximal point measurably, with logarithmic pointwise gradient work. The final
successful check costs one query. No expected work along a sampler is claimed. -/
theorem approximate_proximal_execution {V : E → ℝ} {κ : ℝ≥0}
    (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (κ : ℝ)⁻¹*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2)
    {eta c eps : ℝ} (heta : 0 < eta) (hec : eta ≤ c) (hc : c < 1) (heps : 0 < eps) :
    let T := fun y x : E => y-eta • gradient V x
    let F := fun y x => V x+eta⁻¹/2*‖x-y‖^2
    ∃ p : E → E, ∃ N : E → ℕ,
      Measurable p ∧ Measurable N ∧ Measurable (fun y => (T y)^[N y] y) ∧
      ∀ y, (p y+eta • gradient V (p y)=y) ∧
        (∀ z, F y (p y)+((κ : ℝ)⁻¹+eta⁻¹)/2*‖z-p y‖^2 ≤ F y z ∧
          (F y z ≤ F y (p y) ↔ z=p y)) ∧
        ‖(T y)^[N y+1] y-(T y)^[N y] y‖ ≤ (1-eta)*eps ∧
        (∀ j < N y, ¬ ‖(T y)^[j+1] y-(T y)^[j] y‖ ≤ (1-eta)*eps) ∧
        ‖(T y)^[N y] y-p y‖ ≤ eps ∧
        (N y : ℝ)+1 ≤ (2+(1+Real.log ((1-c)⁻¹))/(-Real.log c)) *
          (1+Real.log (1+‖gradient V y‖/eps)) ∧
        proximalQuery (gradient V) eta eps y (N y+1) y = some ((T y)^[N y] y,N y+1) := by
  have hκpos : 0 < (κ : ℝ) := lt_of_lt_of_le zero_lt_one (by exact_mod_cast hκ)
  have hH' : ∀ x v : E, ((κ⁻¹ : ℝ≥0) : ℝ)*‖v‖^2 ≤
      (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (1 : ℝ≥0)*‖v‖^2 := by
    simpa only [NNReal.coe_inv, NNReal.coe_one, one_mul] using hH
  have hr := TechnicalLemmas.Analysis.QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic
    (r := 0) hV hH' (0 : E)
  have hg : LipschitzWith 1 (gradient V) := by simpa using hr.2
  have hvconv : ConvexOn ℝ Set.univ V := by
    have hs : StrongConvexOn Set.univ ((κ : ℝ)⁻¹) V := by simpa using hr.1
    exact hs.convexOn (fun r => by positivity)
  obtain ⟨p,N,hp,hN,ho,hall⟩ := stopped_contraction hg heta hec hc heps
  refine ⟨p,N,hp,hN,ho,fun y => ?_⟩
  obtain ⟨heq,hs,hbefore,herr,hcap,hrun⟩ := hall y
  refine ⟨heq,?_,hs,hbefore,herr,count_bound (heta.trans_le hec) hc
    (norm_nonneg _) heps hcap,hrun⟩
  let F := fun x => V x+eta⁻¹/2*‖x-y‖^2
  have hdiff := hV.differentiable (by norm_num)
  have hdata := TechnicalLemmas.Analysis.QuadraticRegularizationFirstOrder.curvature_gradient_and_smoothness
    hdiff hvconv (δ := Real.toNNReal eta⁻¹) hg y
  have hgrad (x : E) : gradient F x = gradient V x+eta⁻¹ • (x-y) := by
    simpa only [Real.coe_toNNReal _ (inv_nonneg.mpr heta.le)] using hdata.2.2.1 x
  have hFd : Differentiable ℝ F := by
    simpa only [Real.coe_toNNReal _ (inv_nonneg.mpr heta.le)] using hdata.1
  have hz : gradient F (p y)=0 := by
    rw [hgrad]
    have hsub : p y-y=-(eta • gradient V (p y)) := by
      calc
        p y-y = p y-(p y+eta • gradient V (p y)) :=
          congrArg (fun t => p y-t) heq.symm
        _ = _ := by abel
    rw [hsub,smul_neg,smul_smul,inv_mul_cancel₀ heta.ne',one_smul,add_neg_cancel]
  have hsc : StrongConvexOn Set.univ ((κ : ℝ)⁻¹+eta⁻¹) F := by
    have hh := TechnicalLemmas.Analysis.QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic
      (r := Real.toNNReal eta⁻¹) hV hH' y
    simpa only [NNReal.coe_add, NNReal.coe_inv, Real.coe_toNNReal _ (inv_nonneg.mpr heta.le)] using hh.1
  intro z
  have hb := TechnicalLemmas.Analysis.StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn
    hsc (fun x _ => (hFd x).hasGradientAt) (x := p y) (y := z) (Set.mem_univ _) (Set.mem_univ _)
  rw [hz,inner_zero_left,add_zero] at hb
  refine ⟨hb,⟨fun hle => ?_,fun he => by rw [he]⟩⟩
  have ha : 0 < ((κ : ℝ)⁻¹+eta⁻¹)/2 := by positivity
  have hn : ‖z-p y‖^2 ≤ 0 := by
    change F z ≤ F (p y) at hle
    have hnonpos : (((κ : ℝ)⁻¹+eta⁻¹)/2)*‖z-p y‖^2 ≤ 0 := by linarith
    exact le_of_not_gt (fun hn => (not_lt_of_ge hnonpos) (mul_pos ha hn))
  exact sub_eq_zero.mp (norm_eq_zero.mp (sq_eq_zero_iff.mp (le_antisymm hn (sq_nonneg _))))

end

end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ApproximateProximalExecution
