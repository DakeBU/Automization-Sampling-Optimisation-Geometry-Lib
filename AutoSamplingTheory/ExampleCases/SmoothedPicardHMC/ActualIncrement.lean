import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.FirstOrderDifference
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PhaseMetric

/-!
# Actual synchronous numerical-phase increment
SPHMC arXiv:2609.06906v1 Lemma4.8, (4.16). Actual normalized C2
potential and genuine algorithm; actual f=V_eta producer remains separate.
-/
namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ActualIncrement
open Set MeasureTheory ProbabilityTheory
open scoped BigOperators InnerProductSpace
open PhaseMetric
noncomputable section
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [CompleteSpace E] [MeasurableSpace E] [BorelSpace E]
set_option backward.isDefEq.respectTransparency false
set_option maxHeartbeats 1000000 in
/-- The actual source synchronous increment, with explicit C=12 and
the same c=1/65536 step condition as the actual contraction. -/
theorem source_synchronous_increment {f : E → ℝ} {κ h : ℝ} {J : ℕ}
    (hκ : 1 ≤ κ) (hf : ContDiff ℝ 2 f)
    (hH : ∀ z v, (1 / (2 * κ)) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ f) z v) v ∧
      (fderiv ℝ (fderiv ℝ f) z v) v ≤ ‖v‖ ^ 2)
    (hJ : 2 ≤ J) (hh : 0 < h) :
    let t := fun i : Fin J => h/2*(1-Real.cos ((i : ℝ)/(J-1 : ℝ)*Real.pi))
    let ell := fun j : Fin J => Lagrange.basis Finset.univ t j
    let Λ := sSup ((fun s : ℝ => ∑ j : Fin J, |(ell j).eval s|) '' Icc 0 h)
    let ω := fun i j : Fin J => ∫ s in 0..t i, (t i-s)*(ell j).eval s
    let b := fun j : Fin J => ∫ s in 0..h, (ell j).eval s
    let c := fun j : Fin J => ∫ s in 0..h, (h-s)*(ell j).eval s
    h * Λ ≤ 1/(65536*κ) →
    let a := Real.exp (-h / 2)
    let sigma := Real.sqrt (1 - Real.exp (-h))
    let P0 := fun (z ζ : E × E) => a • z.2 + sigma • ζ.1
    let Y0 := fun (z ζ : E × E) j => z.1 + t j • P0 z ζ
    let Y1 := fun (z ζ : E × E) i => Y0 z ζ i - ∑ j, ω i j • gradient f (Y0 z ζ j)
    let Φ := fun w : (E × E) × (E × E) =>
      (w.1.1 + h • P0 w.1 w.2 - ∑ j, c j • gradient f (Y1 w.1 w.2 j),
        a • (P0 w.1 w.2 - ∑ j, b j • gradient f (Y1 w.1 w.2 j)) + sigma • w.2.2)
    ∀ z z' ζ : E × E,
      Real.sqrt (phaseQuadraticForm κ (((Φ (z,ζ)).1-(Φ (z',ζ)).1)-(z.1-z'.1),
        ((Φ (z,ζ)).2-(Φ (z',ζ)).2)-(z.2-z'.2))) ≤
      12*h*Real.sqrt (phaseQuadraticForm κ (z.1-z'.1,z.2-z'.2)) := by
  classical
  dsimp only
  let t := fun i : Fin J => h/2*(1-Real.cos ((i : ℝ)/(J-1 : ℝ)*Real.pi))
  let ell := fun j : Fin J => Lagrange.basis Finset.univ t j
  let Λ := sSup ((fun s : ℝ => ∑ j : Fin J, |(ell j).eval s|) '' Icc 0 h)
  let ω := fun i j : Fin J => ∫ s in 0..t i, (t i-s)*(ell j).eval s
  let b := fun j : Fin J => ∫ s in 0..h, (ell j).eval s
  let c := fun j : Fin J => ∫ s in 0..h, (h-s)*(ell j).eval s
  intro hstep
  change h*Λ ≤ 1/(65536*κ) at hstep
  have hcoeff := TechnicalLemmas.Analysis.ChebyshevLobattoQuadrature.chebyshev_lobatto_coefficients hJ hh
  rcases hcoeff with ⟨_,_,_,_,_,hΛ,_,_⟩
  change 1 ≤ Λ at hΛ
  have hk : 0 < κ := lt_of_lt_of_le zero_lt_one hκ
  have hi : 1/(65536*κ) ≤ (1:ℝ) := (div_le_one (by positivity)).mpr (by linarith)
  have hh1 : h ≤ 1 := by nlinarith
  have hs : h^2*Λ ≤ 1 := by
    have hm := mul_le_mul_of_nonneg_left (hstep.trans hi) (le_of_lt hh)
    nlinarith
  let a := Real.exp (-h / 2)
  let sigma := Real.sqrt (1 - Real.exp (-h))
  let P0 := fun (z ζ : E × E) => a • z.2 + sigma • ζ.1
  let Y0 := fun (z ζ : E × E) j => z.1 + t j • P0 z ζ
  let Y1 := fun (z ζ : E × E) i => Y0 z ζ i - ∑ j, ω i j • gradient f (Y0 z ζ j)
  let Φ := fun w : (E × E) × (E × E) =>
    (w.1.1 + h • P0 w.1 w.2 - ∑ j, c j • gradient f (Y1 w.1 w.2 j),
      a • (P0 w.1 w.2 - ∑ j, b j • gradient f (Y1 w.1 w.2 j)) + sigma • w.2.2)
  have hfirst := FirstOrderDifference.source_first_order_difference hκ hf hH hJ hh hs
  intro z z' ζ
  let H := h⁻¹ • ∑ j, b j •
    (∫ u in (0:ℝ)..1, InnerProductSpace.continuousLinearMapOfBilin
      (fderiv ℝ (fderiv ℝ f) (Y1 z' ζ j+u • (Y1 z ζ j-Y1 z' ζ j))))
  let d := WithLp.toLp 2 (z.1-z'.1,z.2-z'.2)
  let q := WithLp.toLp 2 ((Φ (z,ζ)).1-(Φ (z',ζ)).1,(Φ (z,ζ)).2-(Φ (z',ζ)).2)
  have hp := hfirst.2.2 z z' ζ
  change H.toLinearMap.IsSymmetric ∧ (∀ v, 1/(2*κ)*‖v‖^2 ≤ inner ℝ (H v) v ∧
    inner ℝ (H v) v ≤ ‖v‖^2) ∧ ‖H‖ ≤ 1 ∧
    ∃ R : WithLp 2 (E × E) →L[ℝ] WithLp 2 (E × E), ‖R‖ ≤ 8*Λ*h^2 ∧
      q = d+h • WithLp.toLp 2 (d.snd,-H d.fst-d.snd)+R d at hp
  rcases hp with ⟨hsym,hcurv,hHnorm,R,hR,heq⟩
  have hr : ‖R d‖ ≤ 8*Λ*h^2*‖d‖ :=
    (R.le_opNorm d).trans (mul_le_mul_of_nonneg_right hR (norm_nonneg d))
  have hsmall : 8*h*Λ ≤ 1 := by
    have hc : 8/(65536*κ) ≤ (1:ℝ) := (div_le_one (by positivity)).mpr (by linarith)
    have hm := mul_le_mul_of_nonneg_left hstep (by norm_num : (0:ℝ) ≤ 8)
    calc
      8*h*Λ = 8*(h*Λ) := by ring
      _ ≤ 8*(1/(65536*κ)) := hm
      _ = 8/(65536*κ) := by ring
      _ ≤ 1 := hc
  have hr' : ‖R d‖ ≤ h*‖d‖ := by
    have hc : 8*Λ*h^2 ≤ h := by
      have hm := mul_le_mul_of_nonneg_right hsmall (le_of_lt hh)
      nlinarith
    exact hr.trans (mul_le_mul_of_nonneg_right hc (norm_nonneg d))
  let A := WithLp.toLp 2 (d.snd,-H d.fst-d.snd)
  have hHx : ‖H d.fst‖ ≤ ‖d.fst‖ :=
    (H.le_opNorm _).trans (by simpa using mul_le_mul_of_nonneg_right hHnorm (norm_nonneg d.fst))
  have hAp : ‖-H d.fst-d.snd‖ ≤ ‖d.fst‖+‖d.snd‖ :=
    (norm_sub_le _ _).trans (by simpa using add_le_add_right hHx ‖d.snd‖)
  have hA : ‖A‖ ≤ 3*‖d‖ := by
    have ht := norm_add_le (WithLp.toLp 2 (d.snd,(0:E)))
      (WithLp.toLp 2 ((0:E),-H d.fst-d.snd))
    have hpairs : ‖A‖ ≤ ‖d.snd‖+‖-H d.fst-d.snd‖ := by
      simpa only [A, ← WithLp.toLp_add, Prod.mk_add_mk, add_zero, zero_add,
        WithLp.norm_toLp_fst, WithLp.norm_toLp_snd] using ht
    linarith [WithLp.norm_fst_le (p := 2) E d, WithLp.norm_snd_le (p := 2) E d]
  have hincr : q-d = h • A+R d := by rw [heq]; dsimp only [A]; abel
  have hn : ‖q-d‖ ≤ 4*h*‖d‖ := by
    rw [hincr]
    have ht := norm_add_le (h • A) (R d)
    rw [norm_smul, Real.norm_eq_abs, abs_of_pos hh] at ht
    nlinarith [mul_le_mul_of_nonneg_left hA (le_of_lt hh)]
  let Qd := phaseQuadraticForm κ (WithLp.ofLp d)
  let Qi := phaseQuadraticForm κ (WithLp.ofLp (q-d))
  change Real.sqrt Qi ≤ 12*h*Real.sqrt Qd
  have hl := ordinary_energy_le_phaseQuadraticForm hκ (WithLp.ofLp d)
  change ‖d.fst‖^2+‖d.snd‖^2 ≤ 6*Qd at hl
  rw [← WithLp.prod_norm_sq_eq_of_L2 d] at hl
  have hu := phaseQuadraticForm_le_ordinary_energy hκ (WithLp.ofLp (q-d))
  change Qi ≤ (3/2:ℝ)*(‖(q-d).fst‖^2+‖(q-d).snd‖^2) at hu
  rw [← WithLp.prod_norm_sq_eq_of_L2 (q-d)] at hu
  have hQd0 : 0 ≤ Qd := by nlinarith [sq_nonneg ‖d‖]
  have hQi0 : 0 ≤ Qi := by
    have hlo := ordinary_energy_le_phaseQuadraticForm hκ (WithLp.ofLp (q-d))
    change _ ≤ 6*Qi at hlo
    nlinarith [sq_nonneg ‖(q-d).fst‖,sq_nonneg ‖(q-d).snd‖]
  have hnsq : ‖q-d‖^2 ≤ (4*h*‖d‖)^2 :=
    (sq_le_sq₀ (norm_nonneg _) (by positivity)).mpr hn
  have hquad : Qi ≤ 144*h^2*Qd := by
    have hm := mul_le_mul_of_nonneg_left hl (by positivity : 0 ≤ 24*h^2)
    nlinarith
  have hsq : (Real.sqrt Qi)^2 ≤ (12*h*Real.sqrt Qd)^2 := by
    simpa only [mul_pow,Real.sq_sqrt hQd0,Real.sq_sqrt hQi0,
      show (12:ℝ)^2=144 by norm_num] using hquad
  exact (sq_le_sq₀ (Real.sqrt_nonneg _) (by positivity)).mp hsq

end
end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ActualIncrement
